from rest_framework import serializers
from .models import ContactList

class ContactListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =  ContactList
        fields = '__all__'