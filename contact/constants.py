class SuccessConstants(object):
    CONTACT_UPDATE_SUCCESS = "Contact updated successfully."
    CONTACT_DELETE_SUCCESS = "Contact Deleted successfully."
    CONTACT_CREATION_SUCCESS = "Contact Created successfully."

class ErrorConstants(object):
    EXCEPTIONAL_ERROR = "Some Exception occured.Error is "
    CONTACT_CREATION_ERROR = "Unable to create contact."
    CONTACT_UPDATE_ERROR = "Unable to update contact."
    CONTACT_DELETE_ERROR = "Unable to delete contact.Maybe No Contact with this ID exists."
    CONTACT_NOT_FOUND = "No contact for the particular search has been found."
    CONTACT_ID_MISSING = "Missing Contact ID"


class Warn(object):
    CONTACT_ID_REQUIRED = "Contact ID required "

