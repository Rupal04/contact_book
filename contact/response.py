class SuccessResponse(object):
    def __init__(self, results=None, msg = "Successful"):
        if results is not None:
            self.results = results
        self.msg = msg
        self.success = True

class ErrorResponse(object):
    def __init__(self, msg = "Error"):
        self.msg = msg
        self.success = False


class PublishContactResponse(object):
    def __init__(self,contact_list):
        self.id = contact_list.id
