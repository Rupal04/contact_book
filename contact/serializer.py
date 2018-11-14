from rest_framework import serializers
from contact.models import ContactList


class SearchContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactList