from contact.constants import SuccessConstants, ErrorConstants


class SuccessResponse(object):
    def __init__(self, results=None, msg = SuccessConstants.SUCCESS_RESPONSE):
        if results is not None:
            self.results = results
        self.msg = msg
        self.success = True

class ErrorResponse(object):
    def __init__(self, msg = ErrorConstants.ERROR_RESPONSE):
        self.msg = msg
        self.success = False


class PublishContactResponse(object):
    def __init__(self,contact_list , msg = SuccessConstants.CONTACT_CREATION_SUCCESS):
        self.msg = msg
        self.contact_id = contact_list.id
        self.success = True

class ContactListResponse(object):
    def __init__(self, results=None, msg = SuccessConstants.SUCCESSFUL_RESPONSE):
        if results is not None:
            self.results = results
        self.msg = msg
        self.success = True
