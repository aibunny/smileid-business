
from rest_framework import generics ,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


from smileid.tasks import handle_kyb_task
from . utils import update_kyb_status
from . serializers import *
from . models import *

class BusinessKYBView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        
        serializer = BusinessKYBDetails(data=request.data)

        if serializer.is_valid():
            # Create and save a BusinessJob instance
            business_job, created = BusinessJob.objects.get_or_create(
                registration_number=serializer.validated_data['registration_number'],
                postal_address=serializer.validated_data['postal_address'],
                postal_code=serializer.validated_data['postal_code'],
                kra_pin = serializer.validated_data['kra_pin'],
                business_name = serializer.validated_data['business_name'],
                business_id = serializer.validated_data['business_id'],                
            )
            
            business_job.save()

            job_id = business_job.job_id
            user_id = business_job.business_id 
            id_number = business_job.registration_number
            postal_address = business_job.postal_address
            postal_code = business_job.postal_code
            business_id = business_job.business_id
            
            update_kyb_status(
                business_id
                )#update the business kyb status as 'pending'
            
            handle_kyb_task.apply_async(
                (
                user_id,
                job_id,
                id_number,
                postal_address,
                postal_code
                )
                )
        
            
            return Response({"message": "KYB started"}, status=status.HTTP_200_OK)
        else:
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

