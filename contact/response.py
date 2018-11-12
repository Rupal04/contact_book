class SuccessResponse(object):
    def __init__(self, results=None, msg = "Successfull"):
        if results is not None:
            self.results = results
        self.msg = msg
        self.success = True

class FailureResponse(object):
    def __init__(self, msg = "error"):
        self.msg = msg
        self.success = False


class PublishContactResponse(object):
    def __init__(self,contact_list):
        self.id = contact_list.id

class DeleteContactResponse(object):
    def __init__(self, msg = "Contact Deleted successfully"):
        self.msg = msg
        self.success = True

class UpdateContactResponse(object):
    def __init__(self, msg = "Contact Updated successfully"):
        self.msg = msg
        self.success = True