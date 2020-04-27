# Brief Summary

Automatic creation of CKAN data views to live data from Orion

Reads FIWARE Orion DB info directly from Mongo, and creates CKAN Data Set entries accordingly for publishing the IoT metadata on the Web.

In use for the University of Oulu's CityIoT research platform, for Data Registry creation and update.

# Introduction

In CityIot, we have used FIWARE Context Broker's reference implementation, Orion, to relay IoT sensor data. Orion itself supports sending data to it, getting data, and subscribing to notifications for when certain data changes. However, it has little support for discoverability. Especially because in CityIoT, all data is under some FIWARE Service, which are separate namespaces. It's possible to query Orion for all entities, but only for the global namespace (undefined service), or a certain service. The names of the services are not visible anywhere. Likewise for Service-Path entries, which are used to further organize the data.

CKAN is an independent web site software for publishing data sets, made for publishing open data in form of e.g. JSON or CSV files. It suits also publishing descriptions of real-time IoT sensor data sets. Indeed, there is a ready made add-on for it which adds FIWARE Context Broker (NGSIv2) data sources as a data set type.

This tool automates the process of creating CKAN entries based on information in Orion. It examines Orion's Mongo DB directly, to find out which services and service paths are there. It then creates corresponding data sets in CKAN, following the logic of how data is organized in CityIoT. The code is simple and straightforward, and should be easy to adapt to different ways of mapping Orion entries to CKAN resources.

# What's in it

This simple tool consists of 3 small Python modules, each in their own file:

- read_mongo_orion.py	uses MongoDB Python client library to read FIWARE Service and ServicePath info

- create_ckan_entries.py creates, or updates, CKAN data sets and resources, using CKAN's HTTP API via the ckanapi library

- orion_to_ckan.py is the main program, which first gets the info from Orion, and then uses that info to call the creation of CKAN entries

It's possible to either run all the parts at once, to first read the Orion info and then create the CKAN entries in one go. Or, the information from Orion can be cached to a JSON file, which can be reused later to create or update the CKAN entries. This can be useful if the connection to Orion's Mongo is only available from a different machine, then the one from where you connect to CKAN. It's also handy for tweaking the structure and descriptions in CKAN, without needing to re-read the info from Orion. A snapshot our cached Orion information is in the repo in db2servicepaths.json
