from api.pipedrive_utils import add_contact_group
from api.pipedrive_utils import add_person
from api.utils import do_request, get_time_in_milliseconds


def setup():
    print("setup")


def teardown():
    print("teardown")


def test_add_contact_group_with_only_name():
    r = add_contact_group(group_name="group" + get_time_in_milliseconds(), group_type="person",
                          description="Test group")
    assert r.json['success']


def test_add_person_to_contact_group():
    person = add_person("Test person" + get_time_in_milliseconds())
    person_id = person.json['data']['id']

    contact_group = add_contact_group(group_name="group" + get_time_in_milliseconds(), group_type="person",
                                      description="Test group")
    contact_group_id = contact_group.json['data']['id']

    endpoint = 'contactGroups/' + str(contact_group_id) + '/persons'
    payload = {
        "item_ids": [person_id]
    }
    r = do_request(method='POST', endpoint=endpoint, data=payload)

    assert r.json['success']
