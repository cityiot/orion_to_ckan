"""
Main program for automatic CityIoT Data Registry creation and update.

Reads FIWARE Orion DB info directly from Mongo, and
creates CKAN Data Set entries accordingly for publishing the IoT metadata on the Web
"""

import read_mongo_orion
import create_ckan_entries

import json #here only for working with snapshot data, instead of reading live mongo db

READ_MONGO = True #else use snapshot from json stored from a previous Mongo DB read

def make_dataset_dict(name, notes):
    dataset_dict = {
        'name': name,
        'notes': notes,
        'owner_org': 'cityiot'
    }
    return dataset_dict

db2servicepaths = None

if READ_MONGO:
    db2servicepaths = read_mongo_orion.get_infos()

    #save snapshot of db read
    with open('db2servicepaths.json', 'w') as outfile:  
        json.dump(db2servicepaths, outfile)

else: #use snapshot of db read
    with open('db2servicepaths.json', 'r') as json_file:  
        db2servicepaths = json.load(json_file)

for dbname, servicepaths in db2servicepaths.items():
    dsd = make_dataset_dict(dbname, "Service Paths: {}".format(servicepaths))
    create_ckan_entries.create_dataset(dsd)
