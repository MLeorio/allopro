from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    label_category = models.CharField(
        verbose_name="Libellé de la catégorie", max_length=100, unique=True, null=False
    )
    description_category = models.CharField(
        verbose_name="Description de la catégorie", max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Date de Modification"
    )

    def __str__(self) -> str:
        return self.label_category

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"


class Metier(models.Model):
    label_metier = models.CharField(
        max_length=100, verbose_name="Nom du métier", unique=True, null=False
    )
    description_metier = models.TextField(verbose_name="Description du métier")

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Date de Modification"
    )

    def __str__(self) -> str:
        return self.label_metier

    class Meta:
        verbose_name = "Métier"
        verbose_name_plural = "Métiers"


class User(AbstractUser):
    is_client = models.BooleanField(default=False, verbose_name="Est un Client")
    is_artisan = models.BooleanField(default=False, verbose_name="Est un Artisan")
    phone = PhoneNumberField(
        unique=True, verbose_name="Numéro de téléphone", null=False
    )
    is_active = models.BooleanField(
        default=False
    )  # Non actif jusqu'à la verification par email
    otp = models.CharField(max_length=7, blank=True, null=True, verbose_name="Code OTP")
    otp_created_at = models.DateTimeField(
        blank=True, null=True, verbose_name="Creation du code OTP"
    )

    def is_otp_expired(self):
        if self.otp_created_at:
            return timezone.now() > self.otp_created_at + timedelta(
                minutes=10
            )  # OTP valide pendant 10 minutes
        return True


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self) -> str:
        return str(self.user)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"


class Artisan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    metier = models.ForeignKey(Metier, on_delete=models.CASCADE, null=True)
    note = models.FloatField(
        verbose_name="Moyenne des notes de l'artisan", null=True, blank=True
    )


    def __str__(self) -> str:
        return f"{self.user} est dans le metier: {self.metier}"


class Atelier(models.Model):
    artisan = models.ForeignKey(Artisan, on_delete=models.CASCADE, null=False)
    nom_atelier = models.CharField(max_length=255, verbose_name="Nom de l'atelier")
    quartier = models.CharField(max_length=255, verbose_name="Quartier")

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Date de Modification"
    )

    def __str__(self) -> str:
        return f"{self.nom_atelier}, atelier de {self.artisan.user}"


class Comment(models.Model):
    artisan = models.ForeignKey(Artisan, on_delete=models.CASCADE, null=False)
    note = models.FloatField(verbose_name="Note de l'artisan", null=True, blank=True)
    comment = models.CharField(
        max_length=255, verbose_name="Commentaire sur l'artisan", null=True, blank=True
    )
    client = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False)

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Date de derniere modification"
    )

    def __str__(self) -> str:
        return f"{self.client.user} donne la note {self.note}"

    class Meta:
        verbose_name = "Commentaire & Note"
        verbose_name_plural = "Commentaires & Notes"
