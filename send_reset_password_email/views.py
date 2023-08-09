from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.http import Http404
from django.views import View

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from .forms import PasswordResetRequestForm, PasswordResetForm
from .models import PasswordResetToken

User = get_user_model()





def send_password_reset_email(request):
    form = PasswordResetRequestForm()
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # messages.warning(request, 'No Profile matches the given query.')
                raise Http404('No Profile matches the given query.')

            token = PasswordResetToken(user=user)
            token.generate_token()
            token.save()

            # Email Sending API Config
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

            # Sending email
            subject = 'Password Reset'
            reset_url = request.build_absolute_uri(reverse('password_reset', kwargs={'token': token.token}))

            # Update the context data for the email template
            context = {
                'user': user,
                'reset_url': reset_url,
            }
            html_content = render_to_string('myaccount/password_reset_email.html', context)

            sender_name = settings.EMAIL_SENDER_NAME
            sender_email = settings.EMAIL_HOST_USER
            sender = {"name": sender_name, "email": sender_email}
            to = [{"email": email}]
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=to,
                html_content=html_content,
                sender=sender,
                subject=subject
            )
            try:
                api_response = api_instance.send_transac_email(send_smtp_email)
                messages.success(request, 'An email with instructions to reset your password has been sent.')
                return redirect('login')
            except ApiException as e:
                messages.warning(request, 'Failed to send password reset email.')
                return redirect('password_reset_request')

    return render(request, 'myaccount/password_reset_request.html', {'form': form})


class PasswordResetView(View):
    def get(self, request, token):
        token_obj = get_object_or_404(PasswordResetToken, token=token)
        if token_obj.is_valid():
            form = PasswordResetForm(user=token_obj.user)
            return render(request, 'myaccount/password_reset.html', {'form': form})
        else:
            messages.warning(request, 'The password reset link has expired or is invalid.')
            return redirect('password_reset_request')

    def post(self, request, token):
        token_obj = get_object_or_404(PasswordResetToken, token=token)
        if token_obj.is_valid():
            form = PasswordResetForm(user=token_obj.user, data=request.POST)
            if form.is_valid():
                form.save()
                token_obj.delete()
                messages.success(request, 'Your password has been reset successfully. You can now log in with your new password.')
                return redirect('login')
        else:
            messages.warning(request, 'The password reset link has expired or is invalid.')
        return render(request, 'myaccount/password_reset.html', {'form': form})


