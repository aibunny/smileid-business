from django.db import models
import uuid
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here
class BusinessAccount(models.Model):
    
    KYC_STATUS_CHOICES = (
        ("Failed", "Failed"),
        ("Pending", "Pending"),
        ("Not Started", "Not Started"),
        ("Completed", "Completed"),
    )
    business_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
        )    
    legal_name = models.CharField(max_length=100,null=True )
    business_tax_id = models.CharField(max_length=20,null=True )
    country = models.CharField(max_length=20,default='Kenya')
    postal_address = models.CharField(max_length=50,null=True)
    postal_code = models.CharField(max_length=15)
    kyb_verified = models.BooleanField(default=False)
    kyb_status = models.CharField(
        max_length=20,
        choices=KYC_STATUS_CHOICES,
        default="Not Started"
        )    
    kyc_job = models.ForeignKey(
        'BusinessJob',
        on_delete=models.PROTECT,
        null=True
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Business Accounts'
        
        
class BusinessJob(models.Model):
    job_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
        )
    country = models.CharField(max_length=5, default='KE')
    id_type = models.CharField(max_length=25, default='BUSINESS_REGISTRATION')
    registration_number = models.CharField(max_length=55)
    kra_pin = models.CharField(max_length=55)
    postal_address = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=15)
    business_name = models.CharField(max_length=150)
    business_id = models.CharField(max_length=150)
    
    class Meta:
        db_table = 'kyb_jobs'

@receiver(post_save, sender = BusinessJob)
def fill_business_details_post_save(sender, instance, created, **kwargs):
    if created:
        try:
            business_instance = BusinessAccount.objects.get(
                business_id = instance.business_id
                )
            
            business_instance.legal_name = instance.business_name
            business_instance.business_tax_id = instance.kra_pin
            business_instance.postal_address = instance.postal_address 
            business_instance.postal_code = instance.postal_code
            business_instance.kyc_status = 'Pending'
            business_instance.kyc_job = instance
            
            business_instance.save()
        except BusinessAccount.DoesNotExist:
            pass
post_save.connect(fill_business_details_post_save, sender=BusinessJob)