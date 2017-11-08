from api.pipedrive_utils import add_contact_group, get_contact_groups, count_contact_groups_by_name
from api.pipedrive_utils import add_person
from api.pipedrive_utils import add_organization
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
                                      description="Test group    description")
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


# TEST: add organization to contact group

def test_add_org_to_contact_group():
    # adding new organization
    organization = add_organization("Test organization" + get_time_in_milliseconds())
    organization_id = organization.json['data']['id']

    # adding new contact group
    contact_group = add_contact_group(group_name="Add org to contact group" + get_time_in_milliseconds(),
                                      group_type="organization",
                                      description="Test group description")
    contact_group_id = contact_group.json['data']['id']

    # adding organization to contact group
    endpoint = 'contactGroups/' + str(contact_group_id) + '/organizations'
    payload = {
        "item_ids": [organization_id]
    }
    r = do_request(method='POST', endpoint=endpoint, data=payload)

    # Assert response code
    assert r.status_code == 200
    # Assert that in API response success==true
    assert r.json['success']


# TEST: remove organization from contact group

def test_remove_org_from_contact_group():
    # Adding new organization
    organization = add_organization("Test organization" + get_time_in_milliseconds())
    organization_id = organization.json['data']['id']

    # Adding new contact group
    contact_group = add_contact_group(group_name="Deleting org from group" + get_time_in_milliseconds(),
                                      group_type="organization",
                                      description="Test group description")
    contact_group_id = contact_group.json['data']['id']

    # Adding organization to contact group
    endpoint = 'contactGroups/' + str(contact_group_id) + '/organizations'
    payload = {
        "item_ids": [organization_id]
    }
    r = do_request(method='POST', endpoint=endpoint, data=payload)

    assert r.status_code == 200
    assert r.json['success']

    # Remove organization from group
    remove_req = do_request(method='DELETE', endpoint=endpoint, data=payload)

    # Assert if removal is successful
    assert remove_req.status_code == 200
    assert remove_req.json['success']

    req = do_request(method='GET', endpoint=endpoint)
    assert req.json['data'] is None


# TEST: rename contact group

def test_rename_contact_group():
    # Create new contact group
    my_group_name = "group" + get_time_in_milliseconds()
    old_group = add_contact_group(group_name=my_group_name, group_type="person",
                                  description="Test group description")
    group_id = old_group.json['data']['id']

    # Assert group creation and it's unicity
    assert old_group.status_code == 201
    assert old_group.json['success']
    assert count_contact_groups_by_name(my_group_name) == 1

    # Renaming the group
    new_group_name = "Renamed_group" + get_time_in_milliseconds()
    payload = {"name": new_group_name}
    endpoint = 'contactGroups/' + str(group_id)
    new_group = do_request(method='PUT', endpoint=endpoint, data=payload)

    # Assert group renaming
    assert new_group.status_code == 200
    assert new_group.json["success"]
    assert count_contact_groups_by_name(my_group_name) == 0
    assert count_contact_groups_by_name(new_group_name) == 1


# TEST: add contact group with invalid values

def test_contact_group_with_invalid_values():
    # Add contact group without a name
    invalid_group = add_contact_group(group_name="", group_type="person", description="Invalid data group")

    # Assert that it's a bad request (status code 400)
    assert invalid_group.status_code == 400
    # Assert that in API response is false
    assert not invalid_group.json["success"]


# TEST: contact is moved to “Ungrouped contacts” when the contact group is deleted

def test_contact_moved_to_ungrouped():
    # Adding new organization
    organization = add_organization("Test organization" + get_time_in_milliseconds())
    organization_id = organization.json['data']['id']

    # Adding new contact group
    group_name = "Group deleting" + get_time_in_milliseconds()
    contact_group = add_contact_group(group_name=group_name,
                                      group_type="organization",
                                      description="Test group description")
    contact_group_id = contact_group.json['data']['id']

    # Adding organization to contact group
    endpoint = 'contactGroups/' + str(contact_group_id) + '/organizations'
    payload = {
        "item_ids": [organization_id]
    }
    r = do_request(method='POST', endpoint=endpoint, data=payload)
    assert r.status_code == 200
    assert r.json['success']

    # Remove contact group
    endpoint = 'contactGroups'
    payload = {
        "group_id": [contact_group_id]
    }

    remove_r = do_request(method='DELETE', endpoint=endpoint, data=payload)

    # Assert if removal was successful
    assert remove_r.status_code == 200
    assert remove_r.json['success']
    assert remove_r.json['data'] is None

    # Check if organization is in ungrouped contacts
    result = 'fail'

    req = do_request(method='GET', endpoint='organizations')
    data = req.json['data']

    for org in data:
        if org['id'] == organization_id:
            result = 'success'

    assert result == 'success'
