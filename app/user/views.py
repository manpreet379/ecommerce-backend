from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .serializers import UserSerializer, PasswordResetSerializer, ResetPasswordSerializer, AddressSerializer, UserProfileSerializer
from django.core.mail import send_mail
from utils.responder import ResponseBuilder
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Address

User = get_user_model()


class UserListCreateAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return ResponseBuilder.ok(code=100, data=serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseBuilder.created(code=101, data=serializer.data)
        return ResponseBuilder.bad_request(code=102, errors=serializer.errors)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return ResponseBuilder.accepted(code=103)
        except Exception as e:
            return ResponseBuilder.bad_request(code=104, errors=str(e))


class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = f"http://localhost:8000/reset-password/{uid}/{token}/"
                send_mail(
                    subject="Password Reset Request",
                    message=f"Click the link to reset your password: {reset_link}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email]
                )
                return ResponseBuilder.ok(code=105)
            except User.DoesNotExist:
                return ResponseBuilder.not_found(code=106)
        return ResponseBuilder.bad_request(code=107, errors=serializer.errors)


class ResetPasswordConfirmView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            token = serializer.validated_data['token']
            uid = serializer.validated_data['uid']

            try:
                user = User.objects.get(pk=urlsafe_base64_decode(uid).decode())
                token_generator = PasswordResetTokenGenerator()
                if token_generator.check_token(user, token):
                    user.set_password(password)
                    user.save()
                    return ResponseBuilder.ok(code=108)
                else:
                    return ResponseBuilder.bad_request(code=109)
            except User.DoesNotExist:
                return ResponseBuilder.not_found(code=106)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return ResponseBuilder.ok(code=110, data=serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ResponseBuilder.ok(code=111, data=serializer.data)
        return ResponseBuilder.bad_request(code=112, errors=serializer.errors)


class AddressListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        address = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(address, many=True)
        return ResponseBuilder.ok(code=113, data=serializer.data)

    def post(self, request):
        serializer = AddressSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return ResponseBuilder.created(code=114, data=serializer.data)
        return ResponseBuilder.bad_request(code=115, errors=serializer.errors)


class AddressDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Address.objects.get(pk=pk, user=user)
        except Address.DoesNotExist:
            return None

    def get(self, request, pk):
        address = self.get_object(pk, request.user)
        if address:
            serializer = AddressSerializer(address)
            return ResponseBuilder.ok(code=116, data=serializer.data)
        return ResponseBuilder.not_found(code=117)

    def put(self, request, pk):
        address = self.get_object(pk, request.user)
        if address:
            serializer = AddressSerializer(address, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return ResponseBuilder.ok(code=118, data=serializer.data)
            return ResponseBuilder.bad_request(code=119, errors=serializer.errors)
        return ResponseBuilder.not_found(code=117)

    def delete(self, request, pk):
        address = self.get_object(pk, request.user)
        if address:
            address.delete()
            return ResponseBuilder.accepted(code=120)
        return ResponseBuilder.not_found(code=117)
