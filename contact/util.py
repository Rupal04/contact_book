import logging

from contact.constants import ErrorConstants, SuccessConstants
from contact.keys import CacheNameSpace, get_contact_list
from contact.models import ContactList
from contact.response import PublishContactResponse, ErrorResponse, SuccessResponse
from django.core.cache import cache

from contact_book.settings import CACHE_TTL

logger = logging.getLogger(__name__)


def to_dict(obj):
    """Represent instance of a class as dict.
        Arguments:
        obj -- any object
        Return:
        dict
        """

    def serialize(obj):
        """Recursively walk object's hierarchy."""
        if isinstance(obj, (bool, int, float)):
            return obj
        elif isinstance(obj, dict):
            obj = obj.copy()
            for key in obj:
                obj[key] = serialize(obj[key])
            return obj
        elif isinstance(obj, list):
            return [serialize(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(serialize([item for item in obj]))
        elif hasattr(obj, '__dict__'):
            return serialize(obj.__dict__)
        else:
            return repr(obj)

    return serialize(obj)


def create_contact(**kwargs):
    try:
        number = kwargs["phone_number"]
        email = kwargs["contact_email"]
        if not ContactList.objects.filter(email=email):
            contact_obj = ContactList.objects.create(number=number, email=email)
        else:
            response = ErrorResponse(msg=ErrorConstants.CONTACT_WITH_PROVIDED_EMAIL_EXIST)
            return response

        if kwargs["contact_name"] != "":
            name = kwargs["contact_name"]
            contact_obj.name = name

        contact_obj.save()

        response = PublishContactResponse(contact_obj)
        return response

    except Exception as e:
        logger.error(ErrorConstants.CONTACT_CREATION_ERROR + str(e), exc_info=True)
        return None


def update_contact(c_id, **kwargs):
    try:
        contact_id = c_id
        contact_obj = ContactList.objects.get(id=contact_id)

        if kwargs['phone_number']:
            number = kwargs['phone_number']
            contact_obj.number = number

        if kwargs["contact_name"]:
            name = kwargs["contact_name"]
            contact_obj.name = name

        if kwargs["contact_email"]:
            email = kwargs["contact_email"]
            contact_obj.email = email

        contact_obj.save()

        response = SuccessResponse(msg=SuccessConstants.CONTACT_UPDATE_SUCCESS)
        return response

    except Exception as e:
        logger.error(ErrorConstants.CONTACT_UPDATE_ERROR + str(e), exc_info=True)
        return None


def delete_contact(c_id):
    try:
        contact_obj = ContactList.objects.filter(id=c_id).first()
        if not contact_obj:
            return None
        else:
            contact_obj.delete()
            response = SuccessResponse(msg=SuccessConstants.CONTACT_DELETE_SUCCESS)
            return response

    except Exception as e:
        logger.error(ErrorConstants.CONTACT_DELETE_ERROR + str(e), exc_info=True)
        return None


def get_contacts():
    try:
        if 'contact_list' in cache:
            contact_obj = cache.get('contact_list')
        else:
            contact_obj = ContactList.objects.all()
            cache.set(get_contact_list(), contact_obj, CacheNameSpace.CONTACT_LIST[1])

        contact_obj_list = []
        for contacts in contact_obj:
            contact_obj_dict = {"name": contacts.name, "number": contacts.number, "email": contacts.email}
            contact_obj_list.append(contact_obj_dict)
        return contact_obj_list

    except Exception as e:
        logger.error(ErrorConstants.CONTACT_LISTING_ERROR + str(e), exc_info=True)
        return None