from django.conf import settings
from django.core.mail import send_mail


def send_account_activation_link(email,email_token,site_url):
    subject = "Your account needs to be verified."
    message = f'Hi click on this link to activate your account. http://{site_url}/accounts/activate/{email_token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)