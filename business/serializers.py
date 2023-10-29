from rest_framework import serializers

class BusinessKYBDetails(serializers.Serializer):
    '''kyb details from user'''
    business_name = serializers.CharField(required=True)
    registration_number = serializers.CharField(required=True)
    kra_pin = serializers.CharField(required=True)
    postal_address = serializers.CharField(required=True)
    postal_code = serializers.CharField(required=True)
    business_id = serializers.CharField(required=True)