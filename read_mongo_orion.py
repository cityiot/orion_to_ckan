#pip3 install pymongo

import pymongo
from pymongo import MongoClient

c = MongoClient()
#MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True)
#c.admin.command('ismaster')

c.list_database_names()
#['admin', 'cep', 'iotagentul', 'local', 'orion', 'orion-testi', 'sth_testi']

d = c['orion']
d.list_collection_names()
#['entities']

pipeline = [
    {"$group": {"_id": "$_id.servicePath"}}
    ]

a = d.entities.aggregate(pipeline)
#<pymongo.command_cursor.CommandCursor object at 0x7fe502666470>
import pprint
pprint.pprint(list(a))
