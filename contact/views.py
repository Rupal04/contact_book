import logging

from contact.constants import ErrorConstants, SuccessConstants, Warn
from contact.response import SuccessResponse, ErrorResponse, ContactListResponse
from contact.util import create_contact, to_dict, delete_contact, get_contacts, update_contact, search_contact
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import api_view

logger = logging.getLogger(__name__)

class ContactViewSet(viewsets.ViewSet):

    # add contact
    def create(self,request):
        try:
            data = request.data

            phone_number = int(data.get("number",0))
            contact_name = data.get("name","")
            contact_email = data.get("email")

            if contact_email is None:
                response = ErrorResponse(msg= ErrorConstants.EMAIL_NOT_PROVIDED)
                return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            create_contact_response = create_contact(phone_number = phone_number, contact_name = contact_name, contact_email = contact_email)

            if not create_contact_response:
                response = ErrorResponse(msg = ErrorConstants.CONTACT_CREATION_ERROR)
                return  Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            elif create_contact_response.success is False :
                response = ErrorResponse(msg=create_contact_response.msg)
                return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return  Response(to_dict(create_contact_response))

        except Exception as e:
            logger.error(ErrorConstants.EXCEPTIONAL_ERROR + str(e), exc_info=True)
            response = ErrorResponse()
            return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # retrieve all contact list
    def list(self,request):
        try:
            contact_list_response = get_contacts()

            if not contact_list_response:
                response = ErrorResponse(msg= ErrorConstants.CONTACT_NOT_FOUND)
                return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(to_dict(ContactListResponse(results=contact_list_response)))
        except Exception as e:
            logger.error(ErrorConstants.EXCEPTIONAL_ERROR + str(e), exc_info=True)
            response = ErrorResponse()
            return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # update contact
    def update(self, request, pk=None):
        try:
            if not pk:
                logger.warn(Warn.CONTACT_ID_REQUIRED)
                response = SuccessResponse(msg= ErrorConstants.CONTACT_ID_MISSING)
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

            return Response(to_dict(update_contact_response))
        except Exception as e:
            logger.error(ErrorConstants.EXCEPTIONAL_ERROR + str(e), exc_info=True)
            response = ErrorResponse()
            return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # delete contact
    def destroy(self,request, pk=None):
        try:
            if not pk:
                logger.warn(Warn.CONTACT_ID_REQUIRED)
                response = SuccessResponse(msg= ErrorConstants.CONTACT_ID_MISSING)
                return Response(to_dict(response), status=status.HTTP_400_BAD_REQUEST)

            delete_contact_response = delete_contact(pk)

            if not delete_contact_response:
                response = ErrorResponse(msg=ErrorConstants.CONTACT_DELETE_ERROR)
                return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(to_dict(delete_contact_response))

        except Exception as e:
            logger.error(ErrorConstants.EXCEPTIONAL_ERROR + str(e), exc_info=True)
            response = ErrorResponse()
            return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# search specific contact with name/email
@api_view(['GET'])
def search_particular_contact(request):
    try:
        query_params = request.query_params
        contact_name = ""
        contact_email = ""

        if 'name' in query_params:
            contact_name = query_params["name"]

        if 'email' in query_params:
            contact_email = query_params["email"]

        contact_list_response = search_contact(contact_name=contact_name, contact_email=contact_email)

        if not contact_list_response:
            response = ErrorResponse(msg=ErrorConstants.CONTACT_NOT_FOUND)
            return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(to_dict(ContactListResponse(results=contact_list_response)))

    except Exception as e:
        logger.error(ErrorConstants.EXCEPTIONAL_ERROR + str(e), exc_info=True)
        response = ErrorResponse()
        return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)






