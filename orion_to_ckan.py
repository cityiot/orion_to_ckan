"""
Main program for automatic CityIoT Data Registry creation and update.

Reads FIWARE Orion DB info directly from Mongo, and
creates CKAN Data Set entries accordingly for publishing the IoT metadata on the Web
"""

import read_mongo_orion
import create_ckan_entries

def make_dataset_dict(name, notes):
    dataset_dict = {
        'name': name,
        'notes': notes,
        'owner_org': 'cityiot'
    }
    return dataset_dict

db2servicepaths = read_mongo_orion.get_infos()
for dbname, servicepaths in db2servicepaths.items():
    dsd = make_dataset_dict(dbname, "Service Paths: {}".format(servicepaths))
    create_ckan_entries.create_dataset(dsd)
