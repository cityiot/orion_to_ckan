#pip install ckanapi
import json
from ckanapi import RemoteCKAN
import pprint
from pprint import pprint

c = RemoteCKAN('http://localhost:5000/', apikey='***REMOVED***')

def get_packageinfos():
    package_list_with_resources = c.action.current_package_list_with_resources()
    #pprint(package_list_with_resources)
    
    packageinfos = {}
    for packageinfo in package_list_with_resources:
        #print(packageinfo['name'])
        name = packageinfo['name']
        packageinfos[name] = packageinfo

    return packageinfos

#global cache populated at start, to support get-or-create both for datasets (packages) and resources
packageinfos = get_packageinfos()

def get_or_create_dataset(dataset_dict):
    #datasets = c.action.package_list() #could cache but just re-get for simplicity and safety now, the load does not matter here
    #pprint(datasets)
    name = dataset_dict['name']
    print("[get_or_create_dataset] - {}".format(name))
    package = None
    if name in packageinfos: #datasets:        
        package = c.action.package_show(id=name)
    else:
        #print("{} not in {}".format(name, packageinfos))
        #pprint(packageinfos)
        #print(packageinfos[name])
        #https://docs.ckan.org/en/latest/api/index.html#ckan.logic.action.create.package_create
        package = c.action.package_create(**dataset_dict)
        #pprint(package)
    return package

def find_existing_resource(package_name, service_path):
    cached_package = packageinfos.get(package_name, False)
    if cached_package: #was on server at the start of this whole run (module import)
        existing_resources = cached_package['resources']
        for r in existing_resources: #is a list where our 'unique key' is just a value..
            if r['service_path'] == service_path:
                return r
    return None

def create_resource(package, url, tenant, service_path):
    #https://docs.ckan.org/en/latest/api/index.html#ckan.logic.action.create.resource_create
    
    name = "{} : {}".format(tenant, service_path)
    resource_dict = {
        'package_id': package['id'],
        'name': name,
        'url': url,
        'format': 'fiware-ngsi',
        'tenant': tenant,
        'service_path': service_path,
        'auth_type': 'none'
        #'resource_type': 'fiware-ngsi' #is this same as 'format' in gui?
    }

    package_name = package['name']
    resource = find_existing_resource(package_name, service_path)
    if resource is not None: #exists, let's patch
        print("Patching existing Resource: {}, {}".format(package_name, service_path))
        resource_dict['id'] = resource['id']
        resource = c.action.resource_patch(**resource_dict)        
    else:
        resource = c.action.resource_create(**resource_dict)
    
        c.action.resource_view_create(
            resource_id = resource['id'],
            title = 'NGSI View',
            description = 'This is a NGSI View',
            view_type = 'ngsi_view'
            )

    #pprint(resource)
    return resource

def test_update():
    # Put the details of the dataset we're going to create into a dict.
    dataset_dict = {
        'name': 'autosync_test_name',
        'notes': 'autosync test notes',
        'owner_org': 'cityiot'
    }

    package = get_or_create_dataset(dataset_dict)
    pprint(package)
    #package = {'id': '5077a989-3c66-4aa0-8031-ae832c46866e'} #'autosync_test_name13'
    resource = create_resource(package, "http://example.com/2", "tenant", "/servicepath")
    pprint(resource)

if __name__ == '__main__':
    test_update()

    # Use the json module to load CKAN's response into a dictionary.
    #response_dict = json.loads(response.read())
    #assert response_dict['success'] is True

    # package_create returns the created package as its result.
    #created_package = response_dict['result']
    #pprint(created_package)
