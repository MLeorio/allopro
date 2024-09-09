from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

from .services import generate_otp, send_otp_whatsapp, send_otp_vonage
from .models import Comment, User, Artisan, Customer, Metier
from django.utils import timezone

User = get_user_model()


class MetierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metier
        fields = ["id", "label_metier", "description_metier"]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    mode = serializers.ChoiceField(choices=["sms", "whatsapp"])

    class Meta:
        model = User
        fields = ["username", "phone", "password", "password_confirm", "mode"]

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError(
                "Les mots de passe ne correspondent pas !"
            )
        return data

    def create(self, validate_data):

        otp = generate_otp()  # Generer le code OTP

        validate_data.pop("password_confirm")
        user = User.objects.create_user(
            username=validate_data["username"], phone=validate_data["phone"]
        )
        user.set_password(validate_data["password"])
        user.is_active = False  # Desactive le compte jusqu'a la verification par email
        user.otp = otp
        user.otp_created_at = timezone.now()

        user.save()

        if validate_data["mode"] == "sms":
            send_otp_vonage(number=validate_data["phone"], otp=otp)
        elif validate_data["mode"] == 'whatsapp':
            send_otp_whatsapp(number=validate_data["phone"], otp=otp)

        return user


class CustomerRegisterSerializer(UserRegisterSerializer):

    def create(self, validated_data):
        user = super().create(validated_data)
        user.is_client = True
        user.save()
        Customer.objects.create(user=user)
        return user


class ArtisanRegisterSerializer(UserRegisterSerializer):

    metier = serializers.PrimaryKeyRelatedField(queryset=Metier.objects.all())

    class Meta(UserRegisterSerializer.Meta):
        fields = UserRegisterSerializer.Meta.fields + ["metier"]

    def create(self, validated_data):
        metier = validated_data.pop("metier")
        user = super().create(validated_data)
        user.is_artisan = True
        user.save()
        Artisan.objects.create(user=user, metier=metier)
        return user


class LoginSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["phone", "password"]
    
    def validate(self, data):
        phone = data["phone"]
        password = data["password"]

        if phone and password:
            user = authenticate(
                request=self.context.get("request"),
                username=phone, password=password
            )
            if not user or not user.is_active:
                raise serializers.ValidationError("Les identifiants sont incorrects.")
        else:
            raise serializers.ValidationError(
                "Le numéro de téléphone et le mot de passe sont requis."
            )
            
        data["user"] = user
        return data

class NoteSerializer(serializers.ModelSerializer):
    artisan = serializers.PrimaryKeyRelatedField(queryset=Artisan.objects.all())
    client = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    
    class Meta:
        model = Comment
        fields = ['note', 'comment']
        
    def create(self, validated_data):
        return super().create(validated_data)
        # rate.artisan = validated_data['artisan']
        # rate.client = validated_data['client']