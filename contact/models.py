from django.db import models

class ContactList(models.Model):
    class Meta:
        db_table = "contact_list"

    name = models.CharField(max_length=100, null=True)
    number = models.BigIntegerField(null=False, max_length=20, blank=False)
    email = models.CharField(max_length=100, null=True)

