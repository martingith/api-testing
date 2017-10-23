from api.utils import do_request


def add_person(name):
    endpoint = 'persons'

    payload = {
        "name": name,
    }
    r = do_request(method='POST', endpoint=endpoint, data=payload)
    return r;


def add_organization(name):
    endpoint = 'organizations'

    payload = {
        "name": name,
    }
    r = do_request(method='POST', endpoint=endpoint, data=payload)
    return r;


def add_contact_group(group_name, group_type, description):
    valid = {'person', 'organization'}

    if group_type not in valid:
        raise ValueError("results: group_type must be one of %r." % valid)

    endpoint = 'contactGroups'

    payload = {
        "name": group_name,
        "group_type": group_type,
        "description": description,
        "contact_interval": "none",
        "owner_as_contact_point": "false"
    }
    return do_request(method='POST', endpoint=endpoint, data=payload)
