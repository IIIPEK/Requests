from django.core.mail import send_mail
from django.conf import settings
from accounts.models import DepartmentNotificationRecipient, NotificationRole

def notify_status_change(request_obj):
    current_status = request_obj.current_status()
    subject = f"Статус заявки обновлён: {request_obj.title}"
    body = f"Заявка «{request_obj.title}» теперь в статусе: {request_obj.current_status().status.description}."

    recipients = set()

    # уведомить заявителя
    if request_obj.requester.email:
        recipients.add(request_obj.requester.email)

    # уведомить утверждающего
    if request_obj.approver and request_obj.approver.email:
        recipients.add(request_obj.approver.email)

    # при rejected и cancelled уведомить всех с ролью "notifier_rejected" / "notifier_cancelled"
    role_suffix = None
    if current_status.status.code == 'approved':
        role_suffix = 'notifier'
    elif current_status.status.code == 'rejected':
        role_suffix = 'notifier_rejected'
    elif current_status.status.code == 'cancelled':
        role_suffix = 'notifier_cancelled'

    if role_suffix:
        try:
            role = NotificationRole.objects.get(name=role_suffix)
            recipients.update(
                DepartmentNotificationRecipient.objects.filter(
                    department=request_obj.department,
                    role=role
                ).values_list('user__email', flat=True)
            )
        except NotificationRole.DoesNotExist:
            pass


    if recipients:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, list(recipients), fail_silently=False)
