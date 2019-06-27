#pip install ckanapi
import json
from ckanapi import RemoteCKAN
import pprint
from pprint import pprint

def create_dataset(dataset_dict):
    c = RemoteCKAN('http://pan0109.panoulu.net:5000/', apikey='555f89e9-2610-41c4-ae38-9148d1b4bba0')
    #s = c.action.package_list()
    #pprint(s)

    #orgs = c.action.organization_list()
    #pprint(orgs)

    #https://docs.ckan.org/en/latest/api/index.html#ckan.logic.action.create.package_create
    c.action.package_create(**dataset_dict)

#def create_resource():
    #https://docs.ckan.org/en/latest/api/index.html#ckan.logic.action.create.resource_create
    resource_dict = {
        'package_id': dataset_dict['name'],
        'url': 'http://example.com/',
        'resource_type': 'fiware-ngsi' #is this same as 'format' in gui?
    }
    #c.action.resource_create(**resource_dict)


def test_update():
    # Put the details of the dataset we're going to create into a dict.
    dataset_dict = {
        'name': 'autosync_test_name',
        'notes': 'autosync test notes',
        'owner_org': 'cityiot'
    }

    create_dataset(dataset_dict)

if __name__ == '__main__':
    test_update()

    # Use the json module to load CKAN's response into a dictionary.
    #response_dict = json.loads(response.read())
    #assert response_dict['success'] is True

    # package_create returns the created package as its result.
    #created_package = response_dict['result']
    #pprint(created_package)
