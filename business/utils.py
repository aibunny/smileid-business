from . models import BusinessAccount

def update_kyb_status(business_id : str):
    
    business_instance = BusinessAccount.objects.get(
        business_id = business_id
        )
    
    #set kyb_status == pending    
    business_instance.kyb_status = 'Pending'
    business_instance.save()
    