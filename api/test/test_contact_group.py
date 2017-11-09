from api.pipedrive_utils import *
from api.utils import *


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
    organization = add_organization('test' + get_time_in_milliseconds())
    organization_id = organization.json['data']['id']
    contact_group = add_contact_group(group_name='test' + get_time_in_milliseconds(), group_type='organization',
                                      description='description')
    contact_group_id = contact_group.json['data']['id']
    endpoint = 'contactGroups/' + str(contact_group_id) + '/organizations'
    payload = {
        'item_ids': [organization_id]
    }
    r = do_request(method='POST', endpoint=endpoint, data=payload)

    assert r.status_code == 200  # response code
    assert r.json['success']  # API response success


def test_remove_organization_from_contact_group():
    organization = add_organization('test' + get_time_in_milliseconds())
    organization_id = organization.json['data']['id']
    contact_group = add_contact_group(group_name='test' + get_time_in_milliseconds(), group_type='organization',
                                      description='description')
    contact_group_id = contact_group.json['data']['id']
    endpoint = 'contactGroups/' + str(contact_group_id) + '/organizations'
    payload = {
        'item_ids': [organization_id]
    }
    r = do_request(method="POST", endpoint=endpoint, data=payload)

    assert r.status_code == 200
    assert r.json['success']

    remove = do_request(method="DELETE", endpoint=endpoint, data=payload)
    assert remove.status_code == 200
    assert remove.json['success']


def test_contact_group_is_renamed():
    old_group_name = 'group' + get_time_in_milliseconds()
    groups = add_contact_group(group_name=old_group_name, group_type='person', description='description')
    old_group_id = groups.json['data']['id']
    new_group_name = 'new_group' + get_time_in_milliseconds()
    endpoint = 'contactGroups/' + str(old_group_id)
    payload = {
        'name': new_group_name
    }
    r = do_request(method='PUT', endpoint=endpoint, data=payload)
    data = r.json['data']

    assert new_group_name == data['name']


def test_rename_contact_group():
    contact_group = 'group' + get_time_in_milliseconds()
    group = add_contact_group(group_name=contact_group, group_type='person', description='description')
    group_id = group.json['data']['id']
    assert count_contact_groups_by_name(group) == 1
    payload = {
        'name': 'group_renamed' + str(get_time_in_milliseconds())
    }
    endpoint = 'contactGroups/' + str(group_id)
    do_request(method='PUT', endpoint=endpoint, data=payload)
    assert count_contact_groups_by_name(group) == 0


def test_add_contact_group_with_invalid_values():
    r = add_contact_group(group_name='', group_type='person', description='description')

    assert r.status_code == 400
