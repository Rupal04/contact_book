class CacheNameSpace(object):
    CONTACT_LIST = ["contact_list", 1800]


def get_contact_list():
    return CacheNameSpace.CONTACT_LIST[0]
