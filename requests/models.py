from django.db import models
from accounts.models import CustomUser, Department
from django.utils import timezone
from common.notify import notify_status_change  # Заглушка

class RequestStatus(models.Model):
    code = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description


class Request(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField()
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    requester = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='requests')
    approver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='approvals')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    po_number = models.CharField("PO номер", max_length=50, blank=True, null=True)
    amount = models.DecimalField("Сумма из MG5", max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.month}/{self.year})"

    def current_status(self):
        return self.status_history.order_by('-changed_at').first()

    @property
    def total(self):
        return self.quantity * self.price


class RequestStatusHistory(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='status_history')
    status = models.ForeignKey(RequestStatus, on_delete=models.CASCADE)
    changed_at = models.DateTimeField(default=timezone.now)
    changed_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        notify_status_change(self.request)  # заглушка на будущее

    def __str__(self):
        return f"{self.request.title} → {self.status.code} @ {self.changed_at}"
