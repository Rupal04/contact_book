import logging

import django_filters

from contact.constants import ErrorConstants, Warn
from contact.models import ContactList
from contact.response import SuccessResponse, ErrorResponse, ContactListResponse
from contact.serializer import SearchContactSerializer
from contact.util import create_contact, to_dict, delete_contact, get_contacts, update_contact
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

logger = logging.getLogger(__name__)


class ContactViewSet(viewsets.ViewSet):
    # add contact
    def create(self, request):
        try:
            data = request.data

            phone_number = int(data.get("number", 0))
            contact_name = data.get("name", "")
            contact_email = data.get("email")

            if contact_email is None:
                response = ErrorResponse(msg=ErrorConstants.EMAIL_NOT_PROVIDED)
                return Response(to_dict(response), status=status.HTTP_400_BAD_REQUEST)

            create_contact_response = create_contact(phone_number=phone_number, contact_name=contact_name,
                                                     contact_email=contact_email)

            if not create_contact_response:
                response = ErrorResponse(msg=ErrorConstants.CONTACT_CREATION_ERROR)
                return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            elif create_contact_response.success is False:
                response = ErrorResponse(msg=create_contact_response.msg)
                return Response(to_dict(response), status=status.HTTP_202_ACCEPTED)

            return Response(to_dict(create_contact_response), status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(ErrorConstants.EXCEPTIONAL_ERROR + str(e), exc_info=True)
            response = ErrorResponse()
            return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # retrieve all contact list
    def list(self, request):
        try:
            contact_list_response = get_contacts()

            if not contact_list_response:
                response = ErrorResponse(msg=ErrorConstants.CONTACT_NOT_FOUND)
                return Response(to_dict(response), status=status.HTTP_404_NOT_FOUND)

            return Response(to_dict(ContactListResponse(results=contact_list_response)), status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(ErrorConstants.EXCEPTIONAL_ERROR + str(e), exc_info=True)
            response = ErrorResponse()
            return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # update contact
    def update(self, request, pk=None):
        try:
            if not pk:
                logger.warning(Warn.CONTACT_ID_REQUIRED)
                response = SuccessResponse(msg=ErrorConstants.CONTACT_ID_MISSING)
                return Response(to_dict(response), status=status.HTTP_400_BAD_REQUEST)

            data = request.data

            c_id = pk
            phone_number = int(data.get("number", 0))
            contact_name = data.get("name", "")
            contact_email = data.get("email", "")

            update_contact_response = update_contact(c_id, phone_number=phone_number, contact_name=contact_name,
                                                     contact_email=contact_email)

            if not update_contact_response:
                response = ErrorResponse(msg=ErrorConstants.CONTACT_UPDATE_ERROR)
                return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(to_dict(update_contact_response), status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(ErrorConstants.EXCEPTIONAL_ERROR + str(e), exc_info=True)
            response = ErrorResponse()
            return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # delete contact
    def destroy(self, request, pk=None):
        try:
            if not pk:
                logger.warning(Warn.CONTACT_ID_REQUIRED)
                response = SuccessResponse(msg=ErrorConstants.CONTACT_ID_MISSING)
                return Response(to_dict(response), status=status.HTTP_400_BAD_REQUEST)

            delete_contact_response = delete_contact(pk)

            if not delete_contact_response:
                response = ErrorResponse(msg=ErrorConstants.CONTACT_DELETE_ERROR)
                return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(to_dict(delete_contact_response), status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(ErrorConstants.EXCEPTIONAL_ERROR + str(e), exc_info=True)
            response = ErrorResponse()
            return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# search contact with name/email
class SearchContactViewSet(viewsets.ModelViewSet):
    serializer_class = SearchContactSerializer

    def get_queryset(self):
        queryset = ContactList.objects.all()
        name = self.request.query_params.get('name', None)
        email = self.request.query_params.get('email', None)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        if email is not None:
            queryset = queryset.filter(email__icontains=email)

        return queryset




