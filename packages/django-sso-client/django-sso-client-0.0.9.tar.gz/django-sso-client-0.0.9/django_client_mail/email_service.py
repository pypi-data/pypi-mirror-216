from django.core.mail import send_mail

def send_notification_email(mail_from,mail_to, subject, message):
    send_mail(
        subject,
        message,
        mail_from,
        [mail_to],
        fail_silently=False,
    )

