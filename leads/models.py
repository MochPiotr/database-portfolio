from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver


class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

class Contact(models.Model):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(_("email"), max_length=254, blank=True, null=True)
    job_position = models.CharField(max_length=40, blank=True, null=True)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True) 
    name = models.ForeignKey("Lead", on_delete=models.CASCADE, null=True, blank=True) 
    agent = models.ForeignKey("Agent", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Lead(models.Model):
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", on_delete=models.SET_NULL, null=True, blank=True)
    class Status(models.TextChoices):
        HIGH = 'New', 'New'
        REGULAR = 'Regular', 'Regular'
        LOW = 'Key', 'Key'
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.REGULAR
    )

    name = models.CharField(max_length=40, default=None, blank=True, null=True)
    primary_contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="primary_leads",
    )

    contacts = models.ManyToManyField(
        Contact,
        related_name="leads",
        blank=True,
    )

    def __str__(self):
        
        return self.name


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Znajdź profil admina (organizację, do której mają należeć wszyscy)
        try:
            admin_user = User.objects.filter(is_superuser=True).first()
            organisation_profile = admin_user.userprofile
        except Exception:
            organisation_profile = None

        # Tworzymy UserProfile nowego użytkownika i przypisujemy do tej samej organizacji
        UserProfile.objects.create(user=instance, organisation=organisation_profile)

class Deal(models.Model):
    name = models.CharField(max_length=40) #title for deal
    lead = models.ForeignKey("Lead", on_delete=models.SET_NULL, null=True, blank=True, related_name="deals") #name of company from Leads
    value = models.DecimalField(max_digits=10, decimal_places=2)
    close_date = models.DateField()
    agent = models.ForeignKey("Agent", on_delete=models.SET_NULL, null=True, blank=True)

    class Probability(models.TextChoices):
        LOW = '0-30', '0-30%'
        MEDIUM = '30-50', '30-50%'
        HIGH = '50-70', '50-70%'
        VERY_HIGH = '75-100', '75-100%'

    probability = models.CharField(
        max_length=10,
        choices=Probability.choices,
        default=Probability.LOW
        )
    class Status(models.TextChoices):
        CREATED = 'Created'
        IN_PROGRESS = 'In Progress'
        LOST = 'Lost'
        WON = 'Won'

    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.CREATED
    )
    contact = models.ForeignKey(
        "Contact",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="deals"
    )
    
    
    def __str__(self):
        return f"{self.name} ({self.get_probability_display()})"


class Category(models.Model):
    name = models.CharField(max_length=30)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def post_user_create_signal(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

post_save.connect(post_user_create_signal, sender=User)

