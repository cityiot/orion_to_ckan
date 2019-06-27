"""
Main program for automatic CityIoT Data Registry creation and update.

Reads FIWARE Orion DB info directly from Mongo, and
creates CKAN Data set enties accordingly for publishing the iot metadata on the Web
"""

import read_mongo_orion
import create_ckan_entries
