from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .models import EmailOtp
from .serializers import EmailOTPSerializer
from user_profile.serializers import UserSerializer

from django.conf import settings
from django.contrib.auth import get_user_model
# from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email_otp(request):
    serializer = EmailOTPSerializer(data=request.data)
    if serializer.is_valid():
        otp = serializer.validated_data['otp']
        try:
            email_otp = EmailOtp.objects.get(email_otp=otp)
            if email_otp.is_valid():
                email_otp.delete()

                user_email = email_otp.email
                try:
                    user = User.objects.get(email=user_email)

                    if user.is_verified:
                        # User is already verified, redirect to login page
                        return Response({'detail': 'Email already verified. Please login.'}, status=status.HTTP_200_OK)
                    else:
                        # Verify the user and mark as verified
                        user.is_verified = True
                        user.save()
                        print('Email verified successfully.')
                        return Response({'detail': 'Email verified successfully!'}, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    # User does not exist, redirect to register page
                    return Response({'detail': 'User not found. Please register again.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Invalid or expired OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
        except EmailOtp.DoesNotExist:
            return Response({'detail': 'Invalid OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def verify_email_otp(request):
#     serializer = EmailOTPSerializer(data=request.data)
#     if serializer.is_valid():
#         otp = serializer.validated_data['otp']
#         try:
#             email_otp = EmailOtp.objects.get(email_otp=otp)
#             if email_otp.is_valid():
#                 email_otp.delete()
#                 user_data = request.session.get('user_data')
#                 if user_data:
#                     serializer = UserSerializer(data=user_data)
#                     if serializer.is_valid():
#                         # Check if 'username' is not provided or empty, set it to the 'email' value
#                         if not user_data.get('username'):
#                             user_data['username'] = user_data['email']
#                         user = User.objects.create_user(
#                             username=user_data['username'],
#                             email=user_data['email'],
#                             first_name=user_data['first_name'],
#                             last_name=user_data['last_name'],
#                             phone_number=user_data['phone_number'],
#                             password=user_data['password'],
#                         )
#                         user.is_verified = True
#                         user.save()
#                         return Response({'detail': 'User created and verified successfully!'}, status=status.HTTP_200_OK)
#                 return Response({'detail': 'Email verification successful!'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'detail': 'Invalid or expired OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
#         except EmailOtp.DoesNotExist:
#             return Response({'detail': 'Invalid OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def verify_email_otp(request):
#     serializer = EmailOTPSerializer(data=request.data)
#     if serializer.is_valid():
#         otp = serializer.validated_data['otp']
#         user_data = request.session.get('user_data')
#         user_email = user_data.get('email')
#         # user_email = "syntaxland@gmail.com"

#         try:
#             email_otp = EmailOtp.objects.get(email_otp=otp, email=user_email)
#             if email_otp.is_valid():
#                 email_otp.delete()
#                 user_serializer = UserSerializer(data=user_data)
#                 if user_serializer.is_valid():
#                     # Check if 'username' is not provided or empty, 
#                     # set it to the 'email' value
#                     if not user_data.get('username'):
#                         user_data['username'] = user_data['email']

#                     # Create the user with the provided data
#                     user = User.objects.create_user(**user_data)
#                     user.is_verified = True
#                     user.save()
#                     return Response({'detail': 'User created and verified successfully!'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'detail': 'Invalid or expired OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
#         except EmailOtp.DoesNotExist:
#             return Response({'detail': 'Invalid OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def verify_email_otp(request):
#     serializer = EmailOTPSerializer(data=request.data)
#     if serializer.is_valid():
#         otp = serializer.validated_data['otp']
#         user_email = "syntaxland@gmail.com"
#         # user_email = request.session.get('user_data').get('email')
#         try:
#             email_otp = EmailOtp.objects.get(email_otp=otp, email=user_email)
#             if email_otp.is_valid():
#                 email_otp.delete()
#                 serializer = UserSerializer(data=request.session.get('user_data'))
#                 if serializer.is_valid():
#                     # Check if 'username' is not provided or empty, set it to the 'email' value
#                     if not request.session.get('user_data').get('username'):
#                         request.session['user_data']['username'] = request.session.get('user_data')['email']
#                     user = User.objects.create_user(**request.session.get('user_data'))
#                     user.is_verified = True
#                     user.save()
#                     return Response({'detail': 'User created and verified successfully!'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'detail': 'Invalid or expired OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
#         except EmailOtp.DoesNotExist:
#             return Response({'detail': 'Invalid OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








# @csrf_exempt
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def verify_email_otp(request):
#     serializer = EmailOTPSerializer(data=request.data)
#     if serializer.is_valid():
#         otp = serializer.validated_data['otp']
#         try:
#             email_otp = EmailOtp.objects.get(email_otp=otp)
#             print(email_otp)
#             if email_otp.is_valid():
#                 email_otp.delete()
#                 data=request.data
#                 serializer = UserSerializer(data=data)
#                 if serializer.is_valid():
#                     # Check if 'username' is not provided or empty, set it to the 'email' value
#                     if not data.get('username'):
#                         data['username'] = data['email']
#                     # save the user data in the session
#                     request.session['user_data'] = data
#                     user = User.objects.create_user(
#                         username=data['username'],
#                         email=data['email'],
#                         first_name=data['first_name'],
#                         last_name=data['last_name'],
#                         phone_number=data['phone_number'],
#                         password=data['password'],
#                     )
#                     user.is_verified=True
#                     user.save()
#                     return Response({'detail': 'User status updated!'}, status=status.HTTP_200_OK)
#                 return Response({'detail': 'Email verification successful!'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'detail': 'Invalid or expired OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
#         except EmailOtp.DoesNotExist:
#             return Response({'detail': 'Invalid OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .forms import EmailOTPVerificationForm
# from .models import EmailOtp
# from django.conf import settings

# import sib_api_v3_sdk
# from sib_api_v3_sdk.rest import ApiException

# from django.contrib.auth import get_user_model

# User = get_user_model()


# @login_required
# def send_email_otp(request):
#     user = request.user

#     email_otp, created = EmailOtp.objects.get_or_create()
#     email_otp.generate_email_otp()

#     # Email Sending API Config
#     configuration = sib_api_v3_sdk.Configuration()
#     configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY
#     api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

#     # Sending email
#     subject = "OTP Email Verification"
#     html_content = f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <title>OTP Email Verification</title>
#         </head>
#         <body>
#             <p>Dear {user.username.title()},</p>
#             <p>Thank you for signing up with our service.
#             To complete your registration, please use the OTP provided below:</p><br/>
#             <h2>OTP: {email_otp.email_otp}</h2><br/>
#             <p>This OTP is valid for 15 minutes.</p>
#             <p>If you didn't request this verification email, please ignore it.</p>
#             <p>Best regards,<br>Softglobal Team</p>
#         </body>
#         </html>
#     """
#     sender_name = settings.EMAIL_SENDER_NAME
#     sender_email = settings.EMAIL_HOST_USER
#     sender = {"name": sender_name, "email": sender_email}
#     to = [{"email": user.email, "name": user.username}]
#     send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
#         to=to,
#         html_content=html_content,
#         sender=sender,
#         subject=subject
#     )

#     try:
#         api_response = api_instance.send_transac_email(send_smtp_email)
#         messages.success(request, f'Email verification OTP sent to: {user.email}')
#     except ApiException as e:
#         print(e)
#         messages.warning(request, 'Failed to send verification email.')

#     return redirect('verify_email_otp')


# @login_required
# def verify_email_otp(request):
#     form = EmailOTPVerificationForm()

#     if request.method == 'POST':
#         form = EmailOTPVerificationForm(request.POST)

#         if form.is_valid():
#             otp = form.cleaned_data['otp']
#             email_otp = EmailOtp.objects.filter(email_otp=otp).first()

#             if email_otp and email_otp.is_valid():
#                 email_otp.delete()
#                 user = User.objects.get(pk=request.user.pk)
#                 user.is_verified = True  # Update the is_verified field on the User model
#                 user.save()
#                 messages.success(request, 'Email verification successful!')
#                 return redirect('profile')
#             else:
#                 messages.warning(request, 'Invalid or expired OTP. Please try again.')

#     return render(request, 'myaccount/verify_email_otp.html', {'form': form})


# @login_required
# def resend_email_otp(request):
#     user = request.user

#     email_otp, created = EmailOtp.objects.get_or_create()
#     email_otp.generate_email_otp()

#     # Email Sending API Config
#     configuration = sib_api_v3_sdk.Configuration()
#     configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY
#     api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

#     # Sending email
#     subject = "OTP Email Verification"
#     html_content = f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <title>OTP Email Verification</title>
#         </head>
#         <body>
#             <p>Dear {user.username.title()},</p>
#             <p>Thank you for signing up with our service.
#             To complete your registration, please use the OTP provided below:</p><br/>
#             <h2>OTP: {email_otp.email_otp}</h2><br/>
#             <p>This OTP is valid for 15 minutes.</p>
#             <p>If you didn't request this verification email, please ignore it.</p>
#             <p>Best regards,<br>Softglobal Team</p>
#         </body>
#         </html>
#     """
#     sender_name = settings.EMAIL_SENDER_NAME
#     sender_email = settings.EMAIL_HOST_USER
#     sender = {"name": sender_name, "email": sender_email}
#     to = [{"email": user.email, "name": user.username}]
#     send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
#         to=to,
#         html_content=html_content,
#         sender=sender,
#         subject=subject
#     )

#     try:
#         api_response = api_instance.send_transac_email(send_smtp_email)
#         messages.success(request, f'Email verification OTP resent.')
#     except ApiException as e:
#         print(e)
#         messages.warning(request, 'Failed to send verification email.')

#     return redirect('verify_email_otp')
