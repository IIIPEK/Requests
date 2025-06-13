from django.contrib.auth.models import AbstractUser
from django.db import models

class Department(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} — {self.description}"


class Right(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.username


class UserDepartmentRight(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    right = models.ForeignKey(Right, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'department', 'right')

    def __str__(self):
        return f"{self.user.username} / {self.department.code} / {self.right.name}"
