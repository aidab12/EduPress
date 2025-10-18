from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from root import settings


@shared_task
def custom_send_mail(new_user, full_name):
    subject = "Добро пожаловать на наш сайт!"
    from_email = settings.EMAIL_HOST_USER
    to_email = new_user
    html_content = render_to_string(
        "users/mail-register.html",
        context={
            "first_name": full_name,
            "email": to_email,

        },
    )

    msg = EmailMultiAlternatives(
        subject,
        html_content,
        from_email,
        [to_email],
        headers={
            "Reply-To": "support@example.com",
            "List-Unsubscribe": "<mailto:unsubscribe@example.com>, <https://example.com/unsubscribe>",
        },
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print(f"Письмо успешно отправлено на {to_email}")
