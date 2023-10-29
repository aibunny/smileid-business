from django.db import models
from business.models import BusinessAccount


class BusinessVerificationResponse(models.Model):
    JSONVersion = models.CharField(max_length=10, blank=True, null=True)
    SmileJobID = models.CharField(max_length=255, blank=True, null=True)
    
    # PartnerParams
    job_id = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.CharField(max_length=255, blank=True, null=True)
    job_type = models.IntegerField(null=True)
    
    ResultType = models.CharField(max_length=100, blank=True, null=True)
    ResultText = models.CharField(max_length=255, blank=True, null=True)
    ResultCode = models.CharField(max_length=10, blank=True, null=True)
    IsFinalResult = models.BooleanField(null=True)
    
    # Actions
    Verify_Business = models.CharField(max_length=255, blank=True, null=True)
    Return_Business_Info = models.CharField(max_length=255, blank=True, null=True)
    
    # company_information
    company_type = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    search_number = models.CharField(max_length=100, blank=True, null=True)
    authorized_shared_capital = models.CharField(max_length=100, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    registration_date = models.DateTimeField(null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    legal_name = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    
    # Fiduciaries (as JSON)
    fiduciaries = models.JSONField(null=True, blank=True)
    
    # Proprietors (as JSON)
    proprietors = models.JSONField(null=True, blank=True)
    
    # Documents (as JSON)
    documents = models.JSONField(null=True, blank=True)
    
    # Directors (as JSON)
    directors = models.JSONField(null=True, blank=True)
    
    class Meta:
        db_table = 'kyb_details'
    
    @classmethod
    def save_response(cls, response_data):
        result_code = response_data.get('ResultCode')
        result_text = response_data.get('ResultText')
        if result_code == "1012" & result_text == 'Business Verified':
            try:
                business_id = response_data.get('user_id')
                business_instance = BusinessAccount.objects.get(
                    business_id =business_id
                )
                business_instance.kyb_verified = True
                business_instance.kyb_status = 'Completed'
                business_instance.save()
                                
            except BusinessAccount.DoesNotExist:
                pass
                            
            response_instance = cls(**response_data)
            response_instance.save()
    