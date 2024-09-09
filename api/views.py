# from django.urls import reverse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from yaml import serialize


from .services import generate_otp, send_otp_whatsapp
from .models import Customer, Metier, User
from .serializers import (
    CustomerRegisterSerializer,
    ArtisanRegisterSerializer,
    LoginSerializer,
    MetierSerializer,
    NoteSerializer,
)
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


User = get_user_model()


class RegisterCustomerView(generics.CreateAPIView):
    serializer_class = CustomerRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
            {
                "message": "Inscription réussie. Un code OTP vous sera envoyer pour validation "
            },
            status=status.HTTP_201_CREATED,
        )

class RegisterArtisanView(RegisterCustomerView):
    serializer_class = ArtisanRegisterSerializer


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            if user.is_otp_expired():
                otp = generate_otp()
                user.otp = otp
                user.otp_created_at = timezone.now()

                user.save()

            send_otp_whatsapp(str(user.phone), str(user.otp))

            return Response(
                {
                    "message": "Un OTP vous a été envoyé. Veuillez valider pour acceéder à votre compte"
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidateOTPView(APIView):

    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(phone=phone, otp=otp)
            if user.is_otp_expired():
                user.otp = None
                user.otp_created_at = None
                user.save()
                
                return Response(
                    {"error": "Code OTP expiré"}, status=status.HTTP_400_BAD_REQUEST
                )

            user.otp = None
            user.otp_created_at = None

            if not user.is_active:
                user.is_active = True

            user.last_login = timezone.now()

            user.save(force_update=True)

            jwt_token = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Code validé avec succès",
                    "token": str(jwt_token.access_token),
                    "refresh": str(jwt_token),
                }
            )
        except User.DoesNotExist:
            return Response(
                {"error": "Code OTP invalide"}, status=status.HTTP_400_BAD_REQUEST
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Recuperation du refresh token depuis le corp de la requete
        refresh_token = request.data.get("refresh")

        if refresh_token :
            try:
                # Creer un objet RefreshToken et le blacklister
                token = RefreshToken(refresh_token)
                # token.blacklist()
                
                return Response({'message': "Deconnexion"},
                    status=status.HTTP_205_RESET_CONTENT)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "Refresh Token not provided"}, status=status.HTTP_400_BAD_REQUEST
            )


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        user = request.user
        return Response(
            {
                "username": user.username,
                "phone": str(user.phone),
            },
            status=status.HTTP_200_OK,
        )


class MetierListCreateView(generics.ListCreateAPIView):
    serializer_class = MetierSerializer
    queryset = Metier.objects.all()


class ResendOTP(APIView):

    def post(self, request):
        phone = request.data.get("phone")

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response(
                {"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND
            )

        if user.otp_created_at and (timezone.now() - user.otp_created_at).seconds < 15:
            return Response(
                {"error": "Vous devez attendre avant de demander un nouvel OTP"},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        otp = generate_otp()
        user.otp = otp
        user.otp_created_at = timezone.now()
        user.save()

        send_otp_whatsapp(str(user.phone), str(user.otp))

        return Response({"message": "Un nouveau code OTP vous a été envoyé."})


class NoteAtelierView(CurrentUserView, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        client = request.user
        serializer.is_valid(raise_exception=True)
        serializer.save(client)
        
        print(client)
        
        
        return Response(serializer, status=status.HTTP_200_OK)
