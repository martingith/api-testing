from api.pipedrive_utils import *
from api.utils import do_request, get_time_in_milliseconds


def setup():
    # Do setup for before starting tests
    print("setup")


def teardown():
    # Clean up the state after tests
    print("teardown")


"""def test_add_contact_group_with_only_name():
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

def test_add_organization_to_group():
    group = add_contact_group("group1","organization","This is automatically generated")
    group_id = group.json['data']['id']
    organization = add_organization("org1")
    organization_id = organization.json['data']['id']

    endpoint = 'contactGroups/' + str(group_id) + '/organizations'
    payload = {
        "item_ids": [organization_id]
    }
    r = do_request(method='POST', endpoint=endpoint,data=payload)

    assert r.status_code == 200
    assert r.json['success'] 

def test_removing_org_from_contact_group():
    group = add_contact_group("group5", "organization", "This is automatically generated")
    group_id = group.json['data']['id']
    organization = add_organization("org1")
    organization_id = organization.json['data']['id']
    organization2 = add_organization("org2")
    organization2_id = organization2.json['data']['id']

    endpoint = 'contactGroups/' + str(group_id) + '/organizations'
    payload = {
        "item_ids": [organization_id,organization2_id]
    }
    r = do_request(method='POST', endpoint=endpoint, data=payload)
    assert r.status_code == 200

    k = do_request(method='DELETE',endpoint=endpoint+'/',data=payload)
    assert k.status_code == 200
    assert k.json['success'] 

def test_rename_a_group():
    group = add_contact_group("group5", "organization", "This is automatically generated")
    group_id = group.json['data']['id']
    endpoint = 'contactGroups/' + str(group_id)
    payload = {
        "name": "uus grupi nimi",
    }
    r = do_request('PUT',endpoint=endpoint,data=payload)
    assert r.status_code == 200
    assert r.json['success'] 

def test_add_contact_group_with_invalid_values():
    group = add_contact_group("","person","description")

    assert group.status_code == 400
    assert not group.json['success'] """

def test_after_deleting_group_does_organization_move_to_ungrouped():
    group = add_contact_group("group6", "organization", "This is automatically generated for deleting")
    group_id = group.json['data']['id']
    organization = add_organization("org1")
    organization_id = organization.json['data']['id']

    endpoint = 'contactGroups/' + str(group_id) + '/organizations'
    payload = {
        "item_ids": [organization_id]
    }
    r = do_request(method='POST', endpoint=endpoint, data=payload)
    k = do_request('GET',endpoint='contactGroups/1')

    algne = int(k.json['additional_data']['group_summary']['organization']['items_total'])

    payload2 = {
        "id":str(group_id)
    }

    o = do_request('DELETE',endpoint='contactGroups/',data=payload2)
    assert o.status_code == 200
    assert o.json['success']

    k = do_request('GET',endpoint='contactGroups/1')
    pärast = int(k.json['additional_data']['group_summary']['organization']['items_total'])

    assert pärast -1 == algne
