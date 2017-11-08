from api.pipedrive_utils import add_contact_group, get_contact_groups, count_contact_groups_by_name
from api.pipedrive_utils import add_person, add_organization
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

def test_add_organization_to_contact_group():
    organization = add_organization("Test organization" + get_time_in_milliseconds())
    organization_id = organization.json['data']['id']

    contact_group = add_contact_group(group_name="group" + get_time_in_milliseconds(), group_type="organization",
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



def test_remove_organization_from_contact_group():
    # creates a new group, adds a organization there and then removes the organization from the group

    organization = add_organization("Test organization" + get_time_in_milliseconds())
    organization_id = organization.json['data']['id']

    contact_group = add_contact_group(group_name="group" + get_time_in_milliseconds(), group_type="organization",
                                      description="Test group description")
    contact_group_id = contact_group.json['data']['id']

    endpoint = 'contactGroups/' + str(contact_group_id) + '/organizations'
    payload = {
        "item_ids": [organization_id]
    }

    r1 = do_request(method='POST', endpoint=endpoint, data=payload)
    # removes the organization from the group
    r2 = do_request(method='DELETE', endpoint=endpoint, data=payload)

    # Assert response code
    assert r1.status_code == 200
    # Assert that in API response success==true
    assert r1.json['success']

    assert r2.status_code == 200
    assert r2.json['success']

def test_rename_group():
    # adds a group and then renames it

    contact_group = add_contact_group(group_name="group" + get_time_in_milliseconds(), group_type="person",
                                      description="Test group description")
    contact_group_id = contact_group.json['data']['id']
    assert contact_group.status_code == 201

    endpoint = 'contactGroups/' + str(contact_group_id)
    payload = {
        "name": "renamed" + get_time_in_milliseconds()
    }
    r = do_request(method='PUT', endpoint=endpoint, data=payload)

    # Assert response code
    assert r.status_code == 200
    # Assert that in API response success==true
    assert r.json['success']

def test_add_contact_group_with_invalid_values():
    # tries adding a group with a blank name

    r1 = add_contact_group(group_name="", group_type="person", description="test description")
    assert r1.status_code == 400

def test_person_in_deleted_group_sent_to_ungrouped_contacts():
    # checks if a group is deleted, then the person who was in that group is
    # moved to the ungrouped contacts group

    # creates a new person
    person = add_person("Test person" + get_time_in_milliseconds())
    person_id = person.json['data']['id']

    # creates a new contact group
    contact_group = add_contact_group(group_name="group" + get_time_in_milliseconds(), group_type="person",
                                      description="Test group description")
    contact_group_id = contact_group.json['data']['id']
    assert contact_group.status_code == 201

    # adds the person to the group
    endpoint = 'contactGroups/' + str(contact_group_id) + '/persons'
    payload = {
        "item_ids": [person_id]
    }
    r1 = do_request(method='POST', endpoint=endpoint, data=payload)
    # Assert response code
    assert r1.status_code == 200
    # Assert that in API response success==true
    assert r1.json['success']

    endpoint = 'contactGroups/' + str(contact_group_id)
    payload = {
        "item_ids": [contact_group_id]
    }

    # deletes the contact group
    r2 = do_request(method='DELETE', endpoint=endpoint, data=payload)
    assert r2.status_code == 200
    assert r2.json['success']

    # ungrouped contacts id is 1
    endpoint = 'contactGroups/1/persons'
    r = do_request(method='GET', endpoint=endpoint)
    groups_list = r.json

    # checks if ungrouped contacts has the person that was created before
    for item in groups_list["data"]:
        if item["item_id"]["value"] == person_id:
            assert True
            return

    assert False
