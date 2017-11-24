from api.pipedrive_utils import add_contact_group, count_contact_groups_by_name, add_person, add_organization, \
    rename_contact_group, remove_contact_group, get_contact_groups
from api.utils import get_time_in_milliseconds, do_request


def setup():
    # Do setup for before starting tests
    print("setup")


def teardown():
    # Clean up the state after tests
    print("teardown")


def test_add_contact_group_with_only_name():
    my_group_name = "test"+ get_time_in_milliseconds()

    r = add_contact_group(group_name=my_group_name, group_type="person",
                          description="")

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
    organization = add_organization("Test111")
    organization_id = organization.json['data']['id']

    contact_group = add_contact_group(group_name="Test111_group", group_type="organization",
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
    organization = add_organization("Test222")
    organization_id = organization.json['data']['id']

    contact_group = add_contact_group(group_name="Test222_group", group_type="organization",
                                      description="Test group description")
    contact_group_id = contact_group.json['data']['id']

    endpoint = 'contactGroups/' + str(contact_group_id) + '/organizations'
    payload = {
        "item_ids": [organization_id]
    }
    r = do_request(method='DELETE', endpoint=endpoint, data=payload)

    # Assert response code
    assert r.status_code == 200
    # Assert that in API response success==true
    assert r.json['success']
    # Assert that group list contains the group that was added by the test
    assert count_contact_groups_by_name(organization) == 0


def test_rename_contact_group():
    r = add_contact_group(group_name="Test222_group", group_type="organization",
                                      description="Test group description")

    contact_group_id = r.json['data']['id']

    group_name = "uusGrupiNimi"

    r = rename_contact_group(group_name=group_name)

    payload = {
        "name": [group_name]
    }

    # Assert response code
    assert r.status_code == 200
    # Assert that in API response success==true
    assert r.json['success']


def test_add_contact_group_with_invalid_values():
     set_group_name = ""
     r = add_contact_group(group_name=set_group_name, group_type="person",
                          description="Test group description")

     #Assert response code
     assert r.status_code == 400
     # Assert that group list contains the group that was added by the test
     assert count_contact_groups_by_name(set_group_name) == 0

def test_contact_is_moved_to_Ungrouped_contacts_when_the_contact_group_is_deleted():

    organization = add_organization("Ungrouped Gruppi")
    organization_id = organization.json['data']['id']

    contact_group = add_contact_group(group_name="Ungrouped Grupi Test_group", group_type="organization",
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

    endpoint = 'contactGroups/' + str(contact_group_id) + '/organizations'
    payload = {
        "item_ids": [organization_id]
    }

    r = remove_contact_group("Ungrouped Grupi Test_group")

    # Assert response code
    assert r.status_code == 200
    assert r.status_code == 200
    # Assert that in API response success==true
    assert r.json['success']
    # Assert that group list contains the group that was added by the test
    assert count_contact_groups_by_name(organization) == 0
    # Assert that group list contains the group that was added by the test
    assert count_contact_groups_by_name("Ungrouped") == 1


















