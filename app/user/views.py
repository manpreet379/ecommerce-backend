from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .serializers import UserSerializer, PasswordResetSerializer,ResetPasswordSerializer, AddressSerializer,UserProfileSerializer
from django.core.mail import send_mail
from utils.responder import standard_response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Address

User=get_user_model()




class UserListCreateAPIView(APIView):
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return standard_response(
            status_code=status.HTTP_200_OK,
            message="User list fetched successfully.",
            data=serializer.data
        )
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return standard_response(
                status_code=status.HTTP_201_CREATED,
                message="User created successfully.",
                data=serializer.data
            )
        return standard_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            status="error",
            message="User creation failed.",
            data=serializer.errors
        )




class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            refresh_token=request.data['refresh']
            token=RefreshToken(refresh_token)
            token.blacklist()
            return standard_response(
                status_code=status.HTTP_205_RESET_CONTENT,
                message="Logout successful.",
                data=None
            )
        except Exception as e:
            return standard_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Logout failed.",
                data=str(e)
            )
            
class PasswordResetRequestView(APIView):
    
    def post(self,request):
        serializer=PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data['email']
            try:
                user=User.objects.get(email=email)
                token_generator=PasswordResetTokenGenerator()
                token=token_generator.make_token(user)
                uid=urlsafe_base64_encode(force_bytes(user.pk))
                reset_link=f"http://localhost:8000/reset-password/{uid}/{token}/"
                send_mail(
                    subject="Password Reset Request",
                    message=f"Click the link to reset your password: {reset_link}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email]
                )
                return standard_response(
                    status_code=status.HTTP_200_OK,
                    message="Password reset link sent to your email.",
                    data=None
                )
            except User.DoesNotExist:
                return standard_response(
                    status_code=status.HTTP_404_NOT_FOUND,
                    message="User with this email does not exist.",
                    data=None
                )
        return standard_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Invalid email address.",
            data=serializer.errors
        )
        
class ResetPasswordConfirmView(APIView):
    
    def post(self ,request):
        serializer=ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            password=serializer.validated_data['password']
            token=serializer.validated_data['token']
            uid=serializer.validated_data['uid']
            
            try:
                user=User.objects.get(pk=urlsafe_base64_decode(uid).decode())
                token_generator=PasswordResetTokenGenerator()
                if token_generator.check_token(user, token):
                    user.set_password(password)
                    user.save()
                    return standard_response(
                        status_code=status.HTTP_200_OK,
                        message="Password reset successfully.",
                        data=None
                    )
                else:
                    return standard_response(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        message="Invalid token.",
                        data=None
                    )
            except User.DoesNotExist:
                return standard_response(
                    status_code=status.HTTP_404_NOT_FOUND,
                    message="User does not exist.",
                    data=None
                )
                


class UserProfileView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        user=request.user
        serializer=UserProfileSerializer(user)
        return standard_response(
            status_code=status.HTTP_200_OK,
            message="User profile fetched successfully.",
            data=serializer.data
        )
        
    def put(self,request):
        user=request.user
        serializer=UserProfileSerializer(user,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return standard_response(
                status_code=status.HTTP_200_OK,
                message="User profile updated successfully.",
                data=serializer.data
            )
        return standard_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="User profile update failed.",
            data=serializer.errors
        )
    


                
class AddressListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        address=Address.objects.filter(user=request.user)
        serializer=AddressSerializer(address, many=True)
        return standard_response(
            status_code=status.HTTP_200_OK,
            message="Address list fetched successfully.",
            data=serializer.data
        )
        
    def post(self,request):
        serializer=AddressSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return standard_response(
                status_code=status.HTTP_201_CREATED,
                message="Address created successfully.",
                data=serializer.data
            )
        return standard_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Address creation failed.",
            data=serializer.errors
        )
        
class AddressDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk,user):
        try:
            return Address.objects.get(pk=pk,user=user)
        except Address.DoesNotExist:
            return None
    
    def get(self,request,pk):
        address=self.get_object(pk,request.user)
        if address:
            serializer=AddressSerializer(address)
            return standard_response(
                status_code=status.HTTP_200_OK,
                message="Address fetched successfully.",
                data=serializer.data
            )
        return standard_response(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Address not found.",
            data=None
        )
        
    def put(self,request,pk):
        address=self.get_object(pk,request.user)
        if address:
            serializer=AddressSerializer(address,data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return standard_response(
                    status_code=status.HTTP_200_OK,
                    message="Address updated successfully.",
                    data=serializer.data
                )
            return standard_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Address update failed.",
                data=serializer.errors
            )
        return standard_response(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Address not found.",
            data=None
        )
    
    def delete(self,request,pk):
        address=self.get_object(pk,request.user)
        if address:
            address.delete()
            return standard_response(
                status_code=status.HTTP_204_NO_CONTENT,
                message="Address deleted successfully.",
                data=None
            )
        return standard_response(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Address not found.",
            data=None
        )