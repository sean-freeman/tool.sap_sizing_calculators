#!/bin/python

# Generic HTTPS handlers

import requests
import json
import pprint
import copy

# urllib3 DEBUG output of GET request to ndpoint connection and HTTP Status Code
def http_logging_debug():
    import logging
    logging.basicConfig(level=logging.DEBUG)

# http.client TRACE low level of any request and response dump
def http_logging_trace():
    from http.client import HTTPConnection
    HTTPConnection.debuglevel = 1

from datetime import datetime
now = datetime.now(tz=None)



# SAP SD Benchmark Directory

benchmarks_categories = requests.get("https://www.sap.com/dmc/exp/2018-benchmark-directory/assets/categories.json")
#benchmarks_content_elements = requests.get("https://www.sap.com/dmc/exp/2018-benchmark-directory/assets/content-elements.json")
benchmarks_sd = requests.get("https://www.sap.com/dmc/exp/2018-benchmark-directory/assets/benchmarks-sd.json")
#benchmarks_bw_bwh = requests.get("https://www.sap.com/dmc/exp/2018-benchmark-directory/assets/benchmarks-bwh.json")
#benchmarks_concurrent = requests.get("https://www.sap.com/dmc/exp/2018-benchmark-directory/assets/benchmarks-concurrent.json")
#benchmarks_bw_bwaml = requests.get("https://www.sap.com/dmc/exp/2018-benchmark-directory/assets/benchmarks-bwaml.json")


with open('benchmarks_categories.json', 'w') as outfile:
    json.dump(benchmarks_categories.json(), outfile, indent=2)

with open('benchmarks_sd.json', 'w') as outfile:
    json.dump(benchmarks_sd.json(), outfile, indent=2)


### Merge datasets

# Transform json input to python objects
sd_dict = benchmarks_sd.json()
#print(benchmark_dict)

# For items in Python Dictionary
for item in sd_dict:
    #print(item)
    #loop through valueIds
    for valueId in item['valueIds']:
        #print(valueId)
        #find value id in benchmarks_categories.json()
        for category in benchmarks_categories.json():
            #print(category['values'])
            for category_values in category['values']:
                #print(category_values)
                if category_values['id'] == valueId:
                    #print(category['_id'])
                    #print(category_values['title'])
                    item[category['_id']] = category_values['title']
    item.pop('valueIds',None)

# Output
#print(sd_dict)

# Output to file
with open('benchmarks_sd_consolidated.json', 'w') as outfile:
    json.dump(sd_dict, outfile, indent=2)



### Begin export to CSV
import csv

# Link to Python Dictionary
sd_csv_dict = sd_dict

# Required to specify Python dictionary keys to export to CSV
# FIND USING.... jq '.[] | keys' benchmarks_sd_consolidated.json | sort -u
sd_csv_columns = ['_id', 'type', 'benchmarkType', 'certificationNumber', 'certificationDate', 'operatingSystem', 'cpuArchitecture', 'catCpuArchitecture', 'cpuSpeed', 'processors', 'cores', 'threads', 'memory', 'cache', 'ranConcurrentWith', 'additionalInfo', 'status', 'saps', 'benchmarkUsers', 'applicationServersAmount', 'averageDbDialogTime', 'averageDbUpdateTime', 'averageResponseTime', 'databaseServer', 'dialogSteps', 'serverName', 'pdfUrl', 'sapBusinessSuite', 'databaseRelease', 'lineItems', 'c:configuration', 'c:cpu', 'c:database', 'c:environment', 'c:operating-system', 'c:processors', 'c:software-release', 'c:technology-partner']

# File to export to
sd_csv_file = "output_sd_" + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + ".csv"

try:
    with open(sd_csv_file, 'w') as sd_csvfile:
        writer = csv.DictWriter(sd_csvfile, fieldnames=sd_csv_columns)
        writer.writeheader()
        for data in sd_csv_dict:
            writer.writerow(data)
except IOError:
    print("I/O error when creating CSV")

