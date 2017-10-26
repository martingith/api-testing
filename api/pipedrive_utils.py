from api.utils import do_request


# Helper method for adding new person
def add_person(name):
    endpoint = 'persons'

    payload = {
        "name": name,
    }
    r = do_request(method='POST', endpoint=endpoint, data=payload)
    return r


# Helper method for adding new organization
def add_organization(name):
    endpoint = 'organizations'

    payload = {
        "name": name,
    }
    r = do_request(method='POST', endpoint=endpoint, data=payload)
    return r


# Helper method for adding new contact group
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


# Helper method for getting list of all contact groups
def get_contact_groups():
    endpoint = 'contactGroups'
    r = do_request(method='GET', endpoint=endpoint)
    return r.json


# Count user contact groups by name
def count_contact_groups_by_name(group_name):
    groups_list = get_contact_groups()
    i = 0
    for item in groups_list["data"]:
        if item['name'] == group_name:
            i = i + 1

    return i
