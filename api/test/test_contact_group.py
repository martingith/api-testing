from api.pipedrive_utils import add_contact_group, get_contact_groups, count_contact_groups_by_name, rename_contact_group, delete_contact_group
from api.pipedrive_utils import add_person, add_organization
from api.pipedrive_utils import add_organization_to_contact_group, remove_organization_from_contact_group, find_organizations_from_ungrouped_group
from api.utils import do_request, get_time_in_milliseconds


def setup():
    # Do setup for before starting tests
    print("setup")


def teardown():
    # Clean up the state after tests
    print("teardown")


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



###############################
#add organization to contact group
def test_add_organization_to_contact_group():
    organization = add_organization("Test organization" + get_time_in_milliseconds())
    organization_id = organization.json['data']['id']

    contact_group = add_contact_group(group_name="group" + get_time_in_milliseconds(), group_type="organization",
                                      description="Test group description")
    contact_group_id = contact_group.json['data']['id']

    r=add_organization_to_contact_group(organization_id, contact_group_id)

    # Assert response code
    assert r.status_code == 200
    # Assert that in API response success==true
    assert r.json['success']


##################################
#remove organization from contact group; at first add group and then remove

def test_remove_organization_from_contact_group():
    organization = add_organization("Test organization" + get_time_in_milliseconds())
    organization_id = organization.json['data']['id']

    contact_group = add_contact_group(group_name="group" + get_time_in_milliseconds(), group_type="organization",
                                      description="Test group description")
    contact_group_id = contact_group.json['data']['id']

    add_organization_to_contact_group(organization_id, contact_group_id)


    r=remove_organization_from_contact_group (organization_id, contact_group_id)

    # Assert response code
    assert r.status_code == 200
    # Assert that in API response success==true
    assert r.json['success']
    # Assert that there will be organization's (that was removed) ID in response data
    assert organization_id in r.json['data']['item_ids']



########################
#rename contact group; test covers only renaming group of organizations
def test_rename_contact_group():
    my_group_name = "group" + get_time_in_milliseconds()
    r = add_contact_group(group_name=my_group_name, group_type="organization",
                          description="Test group description")
    contact_group_id = r.json['data']['id']

    new_name = "newname" + get_time_in_milliseconds()
    r=rename_contact_group(contact_group_id, new_name)


    # Assert response code
    assert r.status_code == 200
    # Assert that in API response success==true
    assert r.json['success']
    # Assert that new name is in the response data
    assert new_name == r.json['data']['name']



##############################
#add contact group with invalid values
#invalid value in this test case is group_name=" ";
#this test succeeds when group_name=None or group_name=""
#however this test should also pass when there are only whitespace characters, but it doesn't
#NB! it can be reproduced only in api, but not in user application

def test_add_contact_group_without_name():
    r = add_contact_group(group_name=" ", group_type="person",
                          description="Test group description")

    # Assert response code
    assert r.status_code == 400
    # Assert that in API response success==false
    assert r.json['success']==False



##############################
#contact is moved to “Ungrouped contacts” when the contact group is deleted
#test covers only deleting organization's group
def test_delete_contact_group():
    organization = add_organization("Test organization" + get_time_in_milliseconds())
    organization_id = organization.json['data']['id']

    my_group_name = "group" + get_time_in_milliseconds()
    contact_group = add_contact_group(group_name=my_group_name, group_type="organization",
                                      description="Test group description")
    contact_group_id = contact_group.json['data']['id']

    add_organization_to_contact_group(organization_id, contact_group_id)


    r = delete_contact_group (contact_group_id)

    # Assert response code
    assert r.status_code == 200
    # Assert that in API response success==true
    assert r.json['success']
    # Assert that there is a contact group ID in response data
    assert contact_group_id == r.json['data']['id']
    # Assert that group list doesn't contain the group that was deleted by the test
    assert count_contact_groups_by_name(my_group_name) == 0
    #Assert that organization is in Ungrouped contacts
    assert organization_id in find_organizations_from_ungrouped_group()
