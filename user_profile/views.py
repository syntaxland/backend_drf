
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException 

# from .models import UserProfile
from .serializers import (
    UserSerializer,
    UserSerializerWithToken,
    MyTokenObtainPairSerializer,
)
from send_email_otp.serializers import EmailOTPSerializer
from send_email_otp.models import EmailOtp
from send_email_otp.send_email_otp_sendinblue import send_email_otp, resend_email_otp
# from send_email_otp.views import verify_email_otp
from send_email_otp.models import EmailOtp

from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user_view(request):
    data = request.data
    serializer = UserSerializer(data=data)

    if serializer.is_valid():
        email = data.get('email')
        try:
            user = User.objects.get(email=email)
            if user.is_verified:
                return Response({'detail': 'User already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # User exists but is not verified. You can update the user's information here if needed
                user.first_name = data.get('first_name')
                user.last_name = data.get('last_name')
                user.phone_number = data.get('phone_number')
                user.password = make_password(data.get('password'))
                user.save()
        except User.DoesNotExist:
            # User does not exist, create the user and send verification OTP
            print('\nCreating user...')
            user = User.objects.create_user(
                username=email,  # Use email as the username
                email=email,
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                phone_number=data.get('phone_number'),
                password=data.get('password'),
            )
            print('\nUser created! Verify your email.')
            return Response({'detail': 'User created. Please verify your email.'}, status=status.HTTP_200_OK)
    else:
        print('Error creating user.')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=204)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=400)
        

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAccountDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



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

#                 email = email_otp.email
#                 try:
#                     user = User.objects.get(email=email)

#                     if user.is_verified:
#                         # User is already verified, redirect to login page
#                         return Response({'detail': 'Email already verified. Please login.'}, status=status.HTTP_200_OK)
#                     else:
#                         # Verify the user and mark as verified
#                         user.is_verified = True
#                         user.save()
#                         return Response({'detail': 'Email verified successfully!'}, status=status.HTTP_200_OK)
#                 except User.DoesNotExist:
#                     # User does not exist, redirect to register page
#                     return Response({'detail': 'User not found. Please register again.'}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response({'detail': 'Invalid or expired OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
#         except EmailOtp.DoesNotExist:
#             return Response({'detail': 'Invalid OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




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

#                 email = email_otp.email
#                 try:
#                     user = User.objects.get(email=email)

#                     if user.is_verified:
#                         # User is already verified, redirect to login page
#                         return Response({'detail': 'Email already verified. Please login.'}, status=status.HTTP_200_OK)
#                     else:
#                         # Verify the user and mark as verified
#                         user.is_verified = True
#                         user.save()
#                         return Response({'detail': 'Email verified successfully!'}, status=status.HTTP_200_OK)
#                 except User.DoesNotExist:
#                     # User does not exist, redirect to register page
#                     return Response({'detail': 'User not found. Please register again.'}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response({'detail': 'Invalid or expired OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
#         except EmailOtp.DoesNotExist:
#             return Response({'detail': 'Invalid OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_user(request):
#     data = request.data
#     print('\nregister data:', data)
#     serializer = UserSerializer(data=data)
#     # request.session['user_data'] = data

#     if serializer.is_valid():
#         request.session['user_data'] = data
#         # Create a new user object
#         user = User.objects.create_user(
#             username=data['username'],
#             email=data['email'],
#             first_name=data['first_name'],
#             last_name=data['last_name'],
#             phone_number=data['phone_number'],
#             password=data['password'],
#         )

#         user_data = request.session.get('user_data')
#         print('\nsend otp user_data:', user_data) 
#         if user_data:
#             email = user_data.get('email')
#             user_first_name = user_data.get('first_name')

#         email_otp, created = EmailOtp.objects.get_or_create(email=email)
#         email_otp.generate_email_otp()
#         # Email Sending API Config
#         configuration = sib_api_v3_sdk.Configuration()
#         configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY
#         api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

#         # Sending email
#         subject = "OTP Email Verification"
#         print('\n',"Sending email OTP...")
#         user_first_name = data['first_name'].title() if data.get('first_name') else 'User'
#         html_content = f"""
#             <!DOCTYPE html>
#             <html>
#             <head>
#                 <title>OTP Email Verification</title>
#             </head>
#             <body>
#                 <p>Dear {user_first_name.title()},</p>
#                 <p>Thank you for signing up with our service.
#                 To complete your registration, please use the OTP provided below:</p><br/>
#                 <h2>OTP: {email_otp.email_otp}</h2><br/>
#                 <p>This OTP is valid for 30 minutes.</p>
#                 <p>If you didn't request this verification email, please ignore it.</p>
#                 <p>Best regards,<br>McdofGlobal Team</p>
#             </body>
#             </html>
#         """ 
#         sender_name = settings.EMAIL_SENDER_NAME
#         sender_email = settings.EMAIL_HOST_USER
#         sender = {"name": sender_name, "email": sender_email}
#         to = [{"email": email, "name": user_first_name}]
#         send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
#             to=to,
#             html_content=html_content, 
#             sender=sender,
#             subject=subject
#         )

#         try:
#             api_response = api_instance.send_transac_email(send_smtp_email)
#             print('OTP sent:', email_otp.email_otp)
#             return Response({'detail': 'Email verification OTP sent successfully.'}, status=status.HTTP_200_OK)
#         except ApiException as e:
#             print(e)
#             # return Response({'detail': 'Failed to send verification email'}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = UserSerializer(user, many=False)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

#                 # Retrieve user data from session (already validated in register_user view)
#                 user_data = request.session.get('user_data')
#                 print('verify otp user_data:\n', user_data)
#                 if user_data:
#                     # Check if 'username' is not provided or empty, set it to the 'email' value
#                     if not user_data.get('username'):
#                         user_data['username'] = user_data['email']
#                     user = User.objects.create_user(
#                         username=user_data['username'],
#                         email=user_data['email'],
#                         first_name=user_data['first_name'],
#                         last_name=user_data['last_name'],
#                         phone_number=user_data['phone_number'],
#                         password=user_data['password'],
#                     )
#                     user.is_verified = True
#                     user.save()
#                     print('verify otp user saved:\n', user.first_name, user.email)
#                     return Response({'detail': 'User created and verified successfully!'}, status=status.HTTP_200_OK)
#                 else:
#                     # If user data is missing, return an error response
#                     return Response({'detail': 'User data not found in session.'}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response({'detail': 'Invalid or expired OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
#         except EmailOtp.DoesNotExist:
#             return Response({'detail': 'Invalid OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_user(request):
#     # Convert the rest_framework.request.Request object to HttpRequest
#     http_request = Request(request)._request

#     data = request.data
#     serializer = UserSerializer(data=data)

#     if serializer.is_valid():
#         # Save the user data in the session
#         http_request.session['user_data'] = data
#         # Send the email OTP
#         # return send_email_otp(http_request)
#         return send_email_otp(http_request, data['email'], data['first_name'])
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_user(request):
#     data = request.data
#     serializer = UserSerializer(data=data)

#     if serializer.is_valid():
#         # Save the user data in the session
#         request.session['user_data'] = data
#         # Send the email OTP
#         # return send_email_otp(request)
#         return send_email_otp(request, data['email'], data['first_name'])
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 






# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from rest_framework import status, generics
# from rest_framework.views import APIView

# from app.models import Product
# from app.serializer import ProductSerializer

# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.tokens import RefreshToken

# from .models import UserProfile
# from .serializers import (UserSerializer, 
#                           UserProfileSerializer, 
#                           UserSerializerWithToken,
#                           MyTokenObtainPairSerializer
#                           )

# from django.http import HttpRequest
# from django.contrib.auth.hashers import make_password
# # from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, get_user_model

# User = get_user_model() 


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_user(request):
#     data = request.data
#     print(data)

#     # Extract the phone_number from the data
#     phone_number = data.get('phone_number', '')

#     try:
#         # Check if 'username' is not provided or empty, set it to the 'email' value
#         if not data.get('username'):
#             data['username'] = data['email']
 
#         # Create a new user object
#         user = User.objects.create(
#             username=data['username'],
#             email=data['email'],
#             first_name=data['first_name'],
#             last_name=data['last_name'],
#             password=make_password(data['password']),
#         )

#         # Create the associated UserProfile with the phone_number
#         UserProfile.objects.create(
#             user=user,
#             phone_number=phone_number,
#         )

#         serializer = UserSerializerWithToken(user, many=False)
#         # if not serializer.is_valid():
#         #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.data)
#         # return Response({'details': 'User created successfully.'}, status=status.HTTP_201_CREATED)
#     except Exception as e:
#         return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)





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
#                 user = UserProfile.objects.get(pk=request.user.pk)
#                 user.is_verified = True
#                 user.save()
#                 return Response({'detail': 'Email verification successful!'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'detail': 'Invalid or expired OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
#         except EmailOtp.DoesNotExist:
#             return Response({'detail': 'Invalid OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def toggle_favorite(request, product_id):
#     product = Product.objects.get(pk=product_id)
#     user_profile = UserProfile.objects.get(user=request.user)

#     if product in user_profile.favorites.all():
#         user_profile.favorites.remove(product)
#     else:
#         user_profile.favorites.add(product)

#     return Response(ProductSerializer(product).data)



# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_user(request):
#     data = request.data

#     # Validate data
#     serializer = UserSerializer(data=data)
#     if not serializer.is_valid():
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # Extract the phone_number from the data
#     phone_number = data.get('phone_number', '')

#     try:
#         # Check if 'username' is not provided or empty, set it to the 'email' value
#         if not data.get('username'):
#             data['username'] = data['email']
 
#         # Create a new user object
#         user = User.objects.create(
#             username=data['username'],
#             email=data['email'],
#             first_name=data['first_name'],
#             last_name=data['last_name'],
#             password=make_password(data['password']),
#         )

#         # Create the associated UserProfile with the phone_number
#         UserProfile.objects.create(
#             user=user,
#             phone_number=phone_number,
#         )

#         # Generate access token
#         request._request.method = 'POST'
#         token_obtain_pair_view = TokenObtainPairView.as_view()
#         response = token_obtain_pair_view(request)
#         return response

#     except Exception as e:
#         return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)





# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_user(request):
#     data = request.data
#     username = data.get('username', None)
#     password = data.get('password', None)
    
#     try:
#         user = User.objects.get(username=username)
#         if user.check_password(password):
#             refresh = RefreshToken.for_user(user)
#             access_token = str(refresh.access_token)
#             return Response({'access': access_token, 'user': user.id}, status=status.HTTP_200_OK)
#         else:
#             return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#     except User.DoesNotExist:
#         return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)





# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_user(request):
#     data = request.data

#     username = data.get('username', None)
#     password = data.get('password', None)
#     user = User.objects.get(username=username)
#     user = authenticate(username=username, password=password)

#     if user is not None:
#         if user.is_active:
#             refresh = RefreshToken.for_user(user)
#             # refresh = TokenRefreshView()
#             # refresh.token = refresh.get_token(user)
#             data = {
#                 'access': str(refresh.access_token),
#                 'refresh': str(refresh),
#             }
#             return Response(data, status=200)
#         else:
#             return Response({'error': 'User is not active.'}, status=401)
#     else:
#         return Response({'error': 'Invalid credentials.'}, status=401)


# @api_view(['GET', 'PUT'])
# @permission_classes([IsAuthenticated])
# def user_profile_view(request):
#     user_profile = UserProfile.objects.get_or_create(user=request.user)[0]

#     if request.method == 'GET':
#         serializer = UserProfileSerializer(user_profile)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
