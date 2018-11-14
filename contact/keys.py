class CacheNameSpace(object):
    CONTACT_LIST = ["contact_list", 1800]
    SPECIFIC_CONTACT = ['specific_contact', 1800]

def get_contact_list():
    return CacheNameSpace.CONTACT_LIST[0]

def get_particular_contact():
    return CacheNameSpace.SPECIFIC_CONTACT[0]