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

#Helper method for adding organization to contact group
def add_organization_to_contact_group(organization_id, contact_group_id):
    endpoint = 'contactGroups/' + str(contact_group_id) + '/organizations'
    payload = {
        "item_ids": [organization_id]
    }
    r = do_request(method='POST', endpoint=endpoint, data=payload)
    return r



# Helper method for removing organization from contact group
def remove_organization_from_contact_group(organization_id, contact_group_id):
    endpoint = 'contactGroups/' + str(contact_group_id) + '/organizations/'

    payload = {
        "item_ids": [organization_id],
    }
    r = do_request(method='DELETE', endpoint=endpoint, data=payload)
    return r


# Helper method for renaming contact group; payload includes fixed values for other properties (except name) that the service endpoint might require from the payload
def rename_contact_group(contact_group_id, name):
    endpoint = 'contactGroups/' + str(contact_group_id)

    payload = {
        "name": name,
        "contact_interval":	"week",
        "description":	None,
        "display_only_owner_contacts":	True,
        "owner_as_contact_point":	False,
    }
    r = do_request(method='PUT', endpoint=endpoint, data=payload)
    return r


## Helper method for deleting contact group
def delete_contact_group(contact_group_id):
    endpoint = 'contactGroups/' + str(contact_group_id)

    r = do_request(method='DELETE', endpoint=endpoint)
    return r

#Helper method for finding organizations' ID from Ungrouped group
def find_organizations_from_ungrouped_group():
    endpoint = 'contactGroups/1/organizations/'

    r = do_request(method='GET', endpoint=endpoint)
    list_of_organizations=set()
    for key, item in r.json["related_objects"]["organization"].items():
        list_of_organizations.add(item["id"])
    return list_of_organizations
