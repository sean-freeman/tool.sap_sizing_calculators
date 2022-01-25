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



# SAP HANA Hardware Directory

solutionType_filter = 'iaas'

hwd_categories = requests.get("https://www.sap.com/dmc/exp/2014-09-02-hana-hardware/enEN/assets/categories.json")
hwd_vendors = requests.get("https://www.sap.com/dmc/exp/2014-09-02-hana-hardware/enEN/assets/vendors.json")
#hwd_storageConfigurations = requests.get("https://www.sap.com/dmc/exp/2014-09-02-hana-hardware/enEN/assets/storageConfigurations.json")
hwd_solutions = requests.get("https://www.sap.com/dmc/exp/2014-09-02-hana-hardware/enEN/assets/solutions.json")
#hwd_comments = requests.get("https://www.sap.com/dmc/exp/2014-09-02-hana-hardware/enEN/assets/comments.json")


with open('hwd_categories.json', 'w') as outfile:
    json.dump(hwd_categories.json(), outfile, indent=2)

with open('hwd_vendors.json', 'w') as outfile:
    json.dump(hwd_vendors.json(), outfile, indent=2)

#with open('hwd_storageConfigurations.json', 'w') as outfile:
#    json.dump(hwd_storageConfigurations.json(), outfile, indent=2)

with open('hwd_solutions.json', 'w') as outfile:
    json.dump(hwd_solutions.json(), outfile, indent=2)

#with open('hwd_comments.json', 'w') as outfile:
#    json.dump(hwd_comments.json(), outfile, indent=2)

with open('hwd_categories.json', 'w') as outfile:
    json.dump(hwd_categories.json(), outfile, indent=2)


### Find HANA HW Solutions

# Transform json input to python objects
hwd_solutions_dict = hwd_solutions.json()

# Filter python objects with list comprehensions
hwd_solutions_iaas_only = [x for x in hwd_solutions_dict if x['solutionType'] == solutionType_filter]

# Transform python object back into json
with open('hwd_solutions_iaas_only.json', 'w') as outfile:
    json.dump(hwd_solutions_iaas_only, outfile, indent=2)


### Find company names

# Transform json input to python objects
hwd_vendors_json_dict = hwd_vendors.json()

hwd_vendor_dict = {}

for vendor in hwd_vendors_json_dict:
    hwd_vendor_dict[vendor['_id']] = vendor['companyName']


### Merge datasets

# Transform json input to python objects
hwd_solutions_main_dict = copy.deepcopy(hwd_solutions_iaas_only)

# Find company names and append to dict
for item in hwd_solutions_main_dict:
    #find vendor id and append
    item['companyName'] = hwd_vendor_dict[item['vendorId']]

for item in hwd_solutions_main_dict:
    # for this item, loop through valueIds
    for valueId in item['valueIds']:
        #print(valueId)
        #find value id in hwd_categories.json()
        for category in hwd_categories.json():
            #print(category['values'])
            for category_values in category['values']:
                #print(category_values)
                if category_values['id'] == valueId:
                    #print(category['_id'])
                    #print(category_values['title'])
                    item[category['_id']] = category_values['title']
                    try:
                        item["memory_gb"] = category_values['sliderValue']
                    except KeyError:
                        break
    # for this item, loop through certifications
    for certification_val in item['certifications']:
        item["certification_start"] = certification_val['start']
        item["certification_end"] = certification_val['end']

    # for this item, run calculations if memory_gb has been set in dictionary
    if 'memory_gb' not in item:
        print('Skip due to missing memory value: ' + item['title'] + ' by ' + item['companyName'])

    else:

        if item["memory_gb"] <= 256 :
            item["calc:memory_category"] = 'Cat A. SAP HANA up to 256GB DRAM'
        elif item["memory_gb"] <= 1024 :
            item["calc:memory_category"] = 'Cat B. SAP HANA up to 1TB DRAM'
        elif item["memory_gb"] <= (1024*2) :
            item["calc:memory_category"] = 'Cat C. SAP HANA up to 2TB DRAM'
        elif item["memory_gb"] <= (1024*4) :
            item["calc:memory_category"] = 'Cat D. SAP HANA up to 4TB DRAM'
        elif item["memory_gb"] <= (1024*6) :
            item["calc:memory_category"] = 'Cat E. SAP HANA up to 6TB DRAM'
        elif item["memory_gb"] <= (1024*8) :
            item["calc:memory_category"] = 'Cat F. SAP HANA up to 8TB DRAM'
        elif item["memory_gb"] <= (1024*12) :
            item["calc:memory_category"] = 'Cat G. SAP HANA up to 12TB DRAM'
        elif item["memory_gb"] <= (1024*16) :
            item["calc:memory_category"] = 'Cat H. SAP HANA up to 16TB DRAM'
        elif item["memory_gb"] <= (1024*20) :
            item["calc:memory_category"] = 'Cat I. SAP HANA up to 20TB DRAM'
        elif item["memory_gb"] <= (1024*24) :
            item["calc:memory_category"] = 'Cat J. SAP HANA up to 24TB DRAM'

        item["c:cpu_sockets"] = item["c:iaasSockets"]
        item["c:cpu_threads"] = item["c:iaasVirtualCPUs"]
        item["calc:dram_per_cpu_thread"] = (item["memory_gb"] / int(item["c:iaasVirtualCPUs"]))
        item["calc:cpu_thread_to_dram_ratio"] = (int(item["c:iaasVirtualCPUs"]) / item["memory_gb"])

        if 'power' in item["c:cpuArchitecture"].lower():
            item["calc:cpu_core_to_dram_ratio"] = ((int(item["c:iaasVirtualCPUs"]) / 8) / item["memory_gb"])
        else:
            item["calc:cpu_core_to_dram_ratio"] = ((int(item["c:iaasVirtualCPUs"]) / 2) / item["memory_gb"])

    item.pop('c:iaasSockets',None)
    item.pop('c:iaasVirtualCPUs',None)
    item.pop('vendorId',None)
    item.pop('valueIds',None)
    item.pop('certifications',None)


### Begin export to CSV
import csv

# Link to Python Dictionary
hwd_csv_dict = hwd_solutions_main_dict

# Required to specify Python dictionary keys to export to CSV
hwd_csv_columns = ['_id', 'type', 'solutionType', 'status', 'title', 'deviceType', 'tdi', 'comments', 'website', 'activityId', 'instanceType', 'linkBenchmark1', 'linkBenchmark2', 'linkBenchmark3', 'linkLaunch', 'linkDocumentation', 'companyName', 'c:applicationType', 'c:cpuArchitecture', 'c:memorySize', 'c:certificationScenario', 'c:sizing', 'c:cpu_sockets', 'c:cpu_threads', 'c:operatingSystem', 'certification_start', 'certification_end', 'created', 'createdBy', 'modifiedBy', 'memory_gb', 'calc:memory_category', 'calc:dram_per_cpu_thread', 'calc:cpu_thread_to_dram_ratio', 'calc:cpu_core_to_dram_ratio']

# File to export to
hwd_csv_file = "output_hwd_" + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + ".csv"

try:
    with open(hwd_csv_file, 'w') as hwd_csvfile:
        writer = csv.DictWriter(hwd_csvfile, fieldnames=hwd_csv_columns)
        writer.writeheader()
        for data in hwd_csv_dict:
            writer.writerow(data)
except IOError:
    print("I/O error when creating CSV")

