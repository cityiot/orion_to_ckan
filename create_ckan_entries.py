#pip install ckanapi
import json
from ckanapi import RemoteCKAN
import pprint
from pprint import pprint

c = RemoteCKAN('http://pan0109.panoulu.net:5000/', apikey='555f89e9-2610-41c4-ae38-9148d1b4bba0')

def create_dataset(dataset_dict):
    #s = c.action.package_list()
    #pprint(s)

    #orgs = c.action.organization_list()
    #pprint(orgs)

    #https://docs.ckan.org/en/latest/api/index.html#ckan.logic.action.create.package_create
    package = c.action.package_create(**dataset_dict)
    #pprint(package)
    return package
    
def create_resource(package):
    #https://docs.ckan.org/en/latest/api/index.html#ckan.logic.action.create.resource_create
    resource_dict = {
        'package_id': package['id'],
        'url': 'http://pan0107.panoulu.net:8000/orion/v2/entities?type=WeatherObserved',
        'format': 'fiware-ngsi',
        'tenant': 'weather',
        'service_path': '/oulu',
        'auth_type': 'none'
        #'resource_type': 'fiware-ngsi' #is this same as 'format' in gui?
    }
    resource = c.action.resource_create(**resource_dict)
    #pprint(resource)

    c.action.resource_view_create(
        resource_id = resource['id'],
        title = 'NGSI View',
        description = 'This is a NGSI View',
        view_type = 'ngsi_view'
        )

def test_update():
    # Put the details of the dataset we're going to create into a dict.
    dataset_dict = {
        'name': 'autosync_test_name13',
        'notes': 'autosync test notes',
        'owner_org': 'cityiot'
    }

    #package = create_dataset(dataset_dict)
    package = {'id': '5077a989-3c66-4aa0-8031-ae832c46866e'} #'autosync_test_name13'
    create_resource(package)

if __name__ == '__main__':
    test_update()

    # Use the json module to load CKAN's response into a dictionary.
    #response_dict = json.loads(response.read())
    #assert response_dict['success'] is True

    # package_create returns the created package as its result.
    #created_package = response_dict['result']
    #pprint(created_package)
