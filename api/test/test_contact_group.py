from api.pipedrive_utils import add_contact_group, get_contact_groups, count_contact_groups_by_name
from api.pipedrive_utils import add_person, add_organization
from api.utils import do_request, get_time_in_milliseconds


def setup():
    # Do setup for before starting tests
    print("setup")


def teardown():
    # Clean up the state after tests
    print("teardown")


# Cover the following flows:
# * add organization to contact group (check)
# * remove organization from contact group (check)
# * rename contact group (check)
# * add contact group with invalid values (check)
# * contact is moved to “Ungrouped contacts” when the contact group is deleted (check)

def test_remove_organization_from_contact_group():
    # create organization
    organization = add_organization("Test organization" + get_time_in_milliseconds())
    organization_id = organization.json['data']['id']

    # create group
    contact_group = add_contact_group(group_name="group" + get_time_in_milliseconds(), group_type="organization",
                                      description="Test group description")
    contact_group_id = contact_group.json['data']['id']

    # add organization to group
    endpoint = 'contactGroups/' + str(contact_group_id) + '/organizations'
    payload = {
        "item_ids": [organization_id]
    }
    do_request(method='POST', endpoint=endpoint, data=payload)

    # delete organization from group
    endpoint = 'organizations'

    payload = {
        "ids": [organization_id]
    }

    delete_r = do_request(method='DELETE', endpoint=endpoint, data=payload)

    # assert if deletion is successful
    assert delete_r.status_code == 200
    assert delete_r.json['success'] == True

    # assert if organization is removed from group
    result = 'success'

    get_orgs = do_request(method='GET', endpoint='organizations')

    data = get_orgs.json['data']
    for org in data:
        if org['id'] == organization_id:
            result = 'unsuccessful'

    assert result == 'success'


def test_contact_group_is_renamed():
    # add a group
    old_group_name = "group" + get_time_in_milliseconds()
    groups = add_contact_group(group_name=old_group_name, group_type="person", description="Test group description")
    old_group_id = groups.json['data']['id']

    new_group_name = "new_group" + get_time_in_milliseconds()

    endpoint = 'contactGroups/' + str(old_group_id)

    payload = {
        "name": new_group_name
    }

    r = do_request(method='PUT', endpoint=endpoint, data=payload)
    data = r.json['data']

    # assert if group is renamed
    assert data['name'] == new_group_name


def test_contact_is_moved_to_ungrouped_contacts_when_the_contact_group_is_deleted():
    # create person
    person = add_person("Test person" + get_time_in_milliseconds())
    person_id = person.json['data']['id']

    # create contact group
    contact_group = add_contact_group(group_name="group" + get_time_in_milliseconds(), group_type="person",
                                      description="Test group description")
    contact_group_id = contact_group.json['data']['id']

    # add person to contact group
    endpoint = 'contactGroups/' + str(contact_group_id) + '/persons'
    payload = {
        "item_ids": [person_id]
    }
    r = do_request(method='POST', endpoint=endpoint, data=payload)

    # assert if request was successful
    assert r.json['success'] == True

    # delete contact group
    endpoint2 = 'contactGroups'

    payload2 = {
        "group_id": [contact_group_id]
    }

    r2 = do_request(method='DELETE', endpoint=endpoint2, data=payload2)

    # Check if group was removed
    assert r2.json['data'] == None

    # check if person is in ungrouped contacts
    result = 'unsuccessful'

    r = do_request(method='GET', endpoint='persons')
    data = r.json['data']
    for person in data:
        if person['id'] == person_id:
            result = 'success'

    assert result == 'success'


def test_add_contact_group_with_invalid_values():
    # add a group with no value (how I interpreted it)
    r = add_contact_group(group_name='', group_type="person", description="Test group description")

    # Assert response code
    assert r.status_code == 400
    # Assert that API response success==false
    assert not r.json['success']


def test_add_contact_group_with_only_name():
    my_group_name = "group" + get_time_in_milliseconds()
    r = add_contact_group(group_name=my_group_name, group_type="person",
                          description="Test group description")

    # Assert response code
    assert r.status_code == 201
    # Assert that in API response success==true
    assert r.json['success']
    # Assert that group list contains the group that was added by the test
    # assert count_contact_groups_by_name(my_group_name) == 1


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
