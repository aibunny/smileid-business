import time
from celery import shared_task
from django.conf import settings
from smile_id_core import BusinessVerification
from smile_id_core import ServerError
#local
from .models import BusinessVerificationResponse
from business.models import BusinessAccount


@shared_task
def handle_kyb_task(user_id, job_id, id_number, postal_address, postal_code):
    partner_id = settings.PARTNER_ID
    api_key = settings.API_KEY
    sid_server = settings.SID_SERVER

    connection = BusinessVerification(partner_id, api_key, sid_server)

    # Create partner_params
    partner_params = {
        "user_id": str(user_id),
        "job_id": str(job_id),
        "job_type": 7,
    }

    max_retries = 2  # Maximum number of retries

    for retry_count in range(max_retries + 1):  # Include the initial attempt
        # Create id params
        id_params = {
            "country": "KE",
            "id_type": "BUSINESS_REGISTRATION",
            "id_number": id_number, 
            "postal_address": postal_address,    
            "postal_code": postal_code,  
        }

        # Submit the job
        try:
            response = connection.submit_job(partner_params, id_params)
        except ValueError:
            # Some params for a job are not valid or missing
            try:
                business_instance = BusinessAccount.objects.get(business_id=user_id)
                business_instance.kyb_status = 'Failed'
                business_instance.save()
            except BusinessAccount.DoesNotExist:
                pass
            break
        except ServerError:
            # SmileID Server returned an error
            if retry_count < max_retries:
                time.sleep(5)  # Wait for 5 seconds before resubmitting the job
            else:
                break  # Break out of the loop after all retries are exhausted
        else:
            BusinessVerificationResponse.save(response)
            break