from django.contrib import admin
from .models import Comment, User, Artisan, Customer, Metier, Category, Atelier


admin.site.site_header = "Administration de AllPro"
admin.site.site_title = "Admin AllPro"
admin.site.index_title = "Bienvenu dans l'interface d'administration"


# Register your models here.


class ArtisanMetierInline(admin.TabularInline):
    model = Artisan
    extra = 1

class MetierCategoryInline(admin.StackedInline):
    model = Metier
    extra = 1


class ArtianUserInline(admin.TabularInline):
    model = Artisan
    extra = 1
    
class ArtisanAtelier(admin.TabularInline):
    model = Atelier
    extra = 1

class CustomerUserInline(admin.StackedInline):
    model = Customer
    extra = 1


class MetierAdmin(admin.ModelAdmin):
    inlines = [ArtisanMetierInline]
    list_display = ("label_metier", "description_metier", "category", "created_at", "updated_at")
    list_filter = ("label_metier", "description_metier", "category")
    search_fields = ("label_metier",)
    ordering = ("label_metier",)
    fieldsets = (
        ("Catégorie", {"fields": ("category",)}),
        ("Métier", {"fields": ("label_metier", "description_metier")})
        )


class UserAdmin(admin.ModelAdmin):
    inlines = [ArtianUserInline, CustomerUserInline]
    list_display = ("username", "phone", "is_active", "date_joined", "last_login")
    list_filter = ("is_active", "date_joined")
    search_fields = ("username", "phone", "email")
    ordering = ("date_joined",)
    fieldsets = (
        (None, {"fields": ("username", "password", "otp", "otp_created_at")}),
        (
            ("Infos personnelles"),
            {"fields": ("phone", "email", "last_name", "first_name")},
        ),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_client",
                    "is_artisan",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (("Dates importantes"), {"fields": ("last_login", "date_joined")}),
    )

class CategoryAdmin(admin.ModelAdmin):
    inlines = [MetierCategoryInline]
    list_display = ("label_category", "description_category", "created_at", "updated_at")
    list_filter = ("label_category", "created_at")
    search_fields = ("label_category",)
    ordering = ("created_at", "label_category")



class ArtisanAdmin(admin.ModelAdmin):
    inlines = [ArtisanAtelier]
    list_display = ("user", "metier", "note", "get_phone")
    search_fields = ("metier", "user")
    list_filter = ('user__is_active', 'user__is_artisan')
    fieldsets = (
        (('Compte Utilisateur'), {'fields': ("user",)}),
        # (('Atelier'), {'fields': ("workshop_name", "quartier")}),
        (('Service Metier'), {'fields': ("metier",)})
    )
    
    def get_phone(self, obj):
        return obj.user.phone
    get_phone.short_description = "Numéro de téléphone"


admin.site.register(Metier, MetierAdmin)
admin.site.register(User, UserAdmin)

admin.site.register(Customer)
admin.site.register(Artisan, ArtisanAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)