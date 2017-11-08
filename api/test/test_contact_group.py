from api.pipedrive_utils import add_contact_group, get_contact_groups, count_contact_groups_by_name
from api.pipedrive_utils import add_person, add_organization
from api.utils import do_request, get_time_in_milliseconds


def setup():
    # Do setup for before starting tests
    print("setup")


def teardown():
    # Clean up the state after tests
    print("teardown")

'''
def test_add_contact_group_with_only_name():
    my_group_name = "group" + get_time_in_milliseconds()
    r = add_contact_group(group_name=my_group_name, group_type="person",
                          description="Test group description")

    # Assert response code
    assert r.status_code == 201
    # Assert that in API response success==true
    assert r.json['success']
    # Assert that group list contains the group that was added by the test
    assert count_contact_groups_by_name(my_group_name) == 1
'''

'''
def test_add_person_to_contact_group():
    person = add_person("Test person" + get_time_in_milliseconds())
    person_id = person.json['data']['id']

    contact_group = add_contact_group(group_name="group" + get_time_in_milliseconds(), group_type="person",
                                      description="Test group description")
    contact_group_id = contact_group.json['data']['id']

    endpoint = 'contactGroups/' + str(contact_group_id) + '/persons'
    payload = {
        "item_ids": [person_id]
    }
    r = do_request(method='POST', endpoint=endpoint, data=payload)

    # Assert response code
    assert r.status_code == 200
    # Assert that in API response success==true
    assert r.json['success']
'''

#ex01
def test_add_organization_to_contact_group():
    organization = add_organization("Test_org" + get_time_in_milliseconds())
    organization_id = organization.json['data']['id']

    contact_group = add_contact_group(group_name="org_group" + get_time_in_milliseconds(), group_type="organization",
                                      description="Test group description")
    contact_group_id = contact_group.json['data']['id']

    endpoint = 'contactGroups/' + str(contact_group_id) + '/organizations'
    payload = {
        "item_ids": [organization_id]
    }
    r = do_request(method='POST', endpoint=endpoint, data=payload)

    # Assert response code
    assert r.status_code == 200
    # Assert that in API response success==true
    assert r.json['success']

#ex02
def test_remove_organization_from_contact_group():
    organization = add_organization("Test org" + get_time_in_milliseconds())
    organization_id = organization.json["data"]["id"]

    contact_group = add_contact_group(group_name="org_group" + get_time_in_milliseconds(), group_type="organization",
                                      description="Test group description")
    contact_group_id = contact_group.json["data"]["id"]

    endpoint = "contactGroups/" + str(contact_group_id) + "/organizations"
    payload = {
        "item_ids": [organization_id]
    }
    r = do_request(method="POST", endpoint=endpoint, data=payload)
    assert r.status_code == 200
    assert r.json["success"]

    #Removal of organization from group
    remove_req = do_request(method="DELETE", endpoint=endpoint, data=payload)
    assert remove_req.status_code == 200
    assert r.json["success"]


#ex03
def test_rename_contact_group():
    my_group_name = "group" + get_time_in_milliseconds()
    group = add_contact_group(group_name=my_group_name, group_type="person",
                          description="Test group description")
    group_id = group.json["data"]["id"]

    assert group.status_code == 201
    assert group.json['success']
    assert count_contact_groups_by_name(my_group_name) == 1

    #Renaming the group    
    payload = {"name": "group_renamed" + str(get_time_in_milliseconds())}
    endpoint = 'contactGroups/' + str(group_id)
    req = do_request(method='PUT', endpoint=endpoint, data=payload)
    assert req.status_code == 200
    assert req.json["success"]

#ex04
def test_add_contact_group_with_invalid_values():
    my_group_name = ""
    r = add_contact_group(group_name=my_group_name, group_type="person",
                          description="desc")
    assert r.status_code == 400 

