# invoicing/models.py
from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from decimal import Decimal

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    # Add other fields as needed
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
     return self.name
    
@receiver(post_save, sender=Client)
def create_or_save_client_user(sender, instance, created, **kwargs):
    # Create or save the associated user when the client is saved
    if created:
        user = User.objects.create(username=instance.email, email=instance.email)
        instance.user = user
    instance.user.save()

# @receiver(post_save, sender=Client)
# def create_client_user(sender, instance, created, **kwargs):
    # if created:
        # Create a user for the client
        # User.objects.create(username=instance.email, email=instance.email)
# 
# @receiver(post_save, sender=Client)
# def save_client_user(sender, instance, **kwargs):
    # Save the associated user when the client is saved
    # instance.user.save()
# 
    
    

class Company(models.Model):
    name = models.CharField(max_length=100, default="AFRICA CALLING SAFARIS LTD")
    logo_url = models.URLField(default="https://example.com/default-logo.png")
    address = models.TextField(default="P.O. Box 12237-00100, Nairobi, Kenya.")

    def __str__(self):
        return self.name


    

class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    issue_date = models.DateField()
    due_date = models.DateField()
    invoice_number = models.CharField(max_length=20, unique=True, editable=False)
    trip_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_days = models.PositiveIntegerField(default=0)
    trip_description = models.TextField()
    quantity = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    currency_choices = [('KES', 'Kenyan Shilling'), ('USD', 'US Dollar'), ('EUR', 'Euro')]
    currency = models.CharField(max_length=3, choices=currency_choices, default='KES')
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    prepared_by = models.CharField(max_length=100)

    # Add a flag to avoid recursion
    _saving = False

    def save(self, *args, **kwargs):
        if not self._saving:
            self._saving = True
            self.number_of_days = (self.end_date - self.start_date).days + 1
            if not self.invoice_number:
                last_invoice = Invoice.objects.filter(company=self.company).order_by('-id').first()
                last_number = 0 if not last_invoice else int(last_invoice.invoice_number.split("/")[-1])
                new_number = last_number + 1
                self.invoice_number = f"ACS-N-0024/{new_number:03d}"
            self.total = self.quantity * self.number_of_days * self.rate
            self.amount = self.total  # Set amount to total

            super(Invoice, self).save(*args, **kwargs)

            self.prepared_by = User.objects.filter(is_superuser=True).first().get_full_name()
            self.save(update_fields=['prepared_by'])

            self._saving = False
        else:
            super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.client.name if self.client else self.new_client_name}"
    

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name