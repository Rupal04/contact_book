import logging

from contact.response import SuccessResponse, FailureResponse
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
            query_params =request.query_params

            phone_number = int(data.get("number",0))
            contact_name = data.get("name","")
            contact_email = data.get("email", "")

            create_contact_response = create_contact(phone_number = phone_number, contact_name = contact_name, contact_email = contact_email)

            if not create_contact_response:
                response = FailureResponse(msg = "Unable to create and add contact")
                return  Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            response = SuccessResponse(results = create_contact_response, msg = "Contact created and added to contact list.")
            return  Response(to_dict(response))

        except Exception as e:
            logger.error("Some Exception occured. Error is "+str(e), exc_info = True)
            response = FailureResponse()
            return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # retrieve all contact list
    def list(self,request):
        try:
            contact_list_response = get_contacts()

            if not contact_list_response:
                response = FailureResponse(msg="No contact for the particular search has been found.")
                return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(to_dict(SuccessResponse(results=contact_list_response)))
        except Exception as e:
            logger.error("Some Exception occured.Error is " + str(e), exc_info=True)
            response = FailureResponse()
            return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # update contact
    def update(self, request, pk=None):
        try:
            if not pk:
                logger.warn("Contact ID provided")
                response = SuccessResponse(msg="Missing Contact ID")
                return Response(to_dict(response), status=status.HTTP_400_BAD_REQUEST)

            data = request.data
            query_params = request.query_params

            c_id = pk
            phone_number = int(data.get("number", 0))
            contact_name = data.get("name", "")
            contact_email = data.get("email", "")

            update_contact_response = update_contact(c_id, phone_number=phone_number, contact_name=contact_name,
                                                     contact_email=contact_email)

            if not update_contact_response:
                response = FailureResponse(msg="Unable to update contact")
                return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            response = SuccessResponse(results=update_contact_response)
            return Response(to_dict(response))

        except Exception as e:
            logger.error("Some Exception occured.Error is " + str(e), exc_info=True)
            response = FailureResponse()
            return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # delete contact
    def destroy(self,request, pk=None):
        try:
            if not pk:
                logger.warn("Contact ID provided")
                response = SuccessResponse(msg="Missing Contact ID")
                return Response(to_dict(response), status=status.HTTP_400_BAD_REQUEST)


            delete_contact_response = delete_contact(pk)

            if not delete_contact_response:
                response = FailureResponse(msg="Unable to delete contact.Maybe No Contact with this ID exists.")
                return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            response = SuccessResponse(results=delete_contact_response)
            return Response(to_dict(response))

        except Exception as e:
            logger.error("Some Exception occured.Error is "+str(e), exc_info = True)
            response = FailureResponse()
            return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# search specific contact with name and email
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
            response = FailureResponse(msg="No contact for the particular search has been found.")
            return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(to_dict(SuccessResponse(results=contact_list_response)))

    except Exception as e:
        logger.error("Some Exception occured.Error is " + str(e), exc_info=True)
        response = FailureResponse()
        return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)






