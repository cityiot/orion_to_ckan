#pip3 install pymongo

import pprint
from pprint import pprint
import pymongo
from pymongo import MongoClient

c = MongoClient()
#MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True)
#c.admin.command('ismaster')

dbnames = c.list_database_names()
#['admin', 'cep', 'iotagentul', 'local', 'orion', 'orion-testi', 'sth_testi']
#pprint(dbnames)

#starting with orion-
orion_dbs = [n.split('orion-')[1] for n in dbnames 
             if n.startswith('orion-')]
#pprint(orion_dbs)

#check if matching STH DB exists to filter out orion-only tests (not real datasets i presume)
filtered = [n for n in orion_dbs
            if 'sth_'+n in dbnames]
pprint(filtered)

#mongo aggregate query to find FIWARE Service Paths in a Orion DB
pipeline = [
    {"$group": {"_id": "$_id.servicePath"}}
]

for n in filtered:
    d = c['orion-'+n]
    d.list_collection_names()
    #['entities']

    a = d.entities.aggregate(pipeline)
    #<pymongo.command_cursor.CommandCursor object at 0x7fe502666470>

    print("<--- Service Paths in DB {} ---".format(n)) #servers have py 3.5, f'' new format strings were only introduced in 3.6
    pprint(list(a))
    print("--->")
