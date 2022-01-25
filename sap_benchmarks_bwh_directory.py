#!/bin/python

# Generic HTTPS handlers

import copy
import json
import pprint

import requests


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



# SAP BWH Benchmark Directory

benchmarks_categories = requests.get("https://www.sap.com/dmc/exp/2018-benchmark-directory/assets/categories.json")
#benchmarks_content_elements = requests.get("https://www.sap.com/dmc/exp/2018-benchmark-directory/assets/content-elements.json")
#benchmarks_sd = requests.get("https://www.sap.com/dmc/exp/2018-benchmark-directory/assets/benchmarks-sd.json")
benchmarks_bw_bwh = requests.get("https://www.sap.com/dmc/exp/2018-benchmark-directory/assets/benchmarks-bwh.json")
#benchmarks_concurrent = requests.get("https://www.sap.com/dmc/exp/2018-benchmark-directory/assets/benchmarks-concurrent.json")
#benchmarks_bw_bwaml = requests.get("https://www.sap.com/dmc/exp/2018-benchmark-directory/assets/benchmarks-bwaml.json")


with open('benchmarks_categories.json', 'w') as outfile:
    json.dump(benchmarks_categories.json(), outfile, indent=2)

with open('benchmarks_bw_bwh.json', 'w') as outfile:
    json.dump(benchmarks_bw_bwh.json(), outfile, indent=2)


### Merge datasets


# Transform json input to python objects
bwh_dict = benchmarks_bw_bwh.json()
#print(bwh_dict)

# For items in Python Dictionary
for item in bwh_dict:
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
    item['calc:phase1_compare_1billion_secs_avg-low_is_best'] = round(float(item['phase1DL']) / float(item['c:initial-records']),2)
    item['calc:phase2_compare_query_records_parse_per_hr-high_is_best'] = round(int(item['phase2QE']) * int(item['phase2RS']),2)
    item['calc:phase2_compare_complex_query_records_parse_per_min-high_is_best'] = round((int(item['phase2RS']) / int(item['phase3RT'])) * 60,2)

# Rank Caculation
def rank(elements, reverse=False):
    sorted_elements = sorted(elements, reverse=reverse)
    return [sorted_elements.index(i)+1 for i in elements]

def avg(*nums):
    return round(sum(nums)/len(nums),2)

phases = [[],[],[]]
for i in bwh_dict:
    phases[0].append(i['calc:phase1_compare_1billion_secs_avg-low_is_best'])
    phases[1].append(i['calc:phase2_compare_query_records_parse_per_hr-high_is_best'])
    phases[2].append(i['calc:phase2_compare_complex_query_records_parse_per_min-high_is_best'])

ranks = [rank(phases[0]), rank(phases[1], True), rank(phases[2], True)]

averages = [avg(ranks[0][i], ranks[1][i], ranks[2][i]) for i, _ in enumerate(bwh_dict)]

consolidated_rank = rank(averages)

for index, item in enumerate(bwh_dict):
    for i, _ in enumerate(ranks):
        phase_name = 'Phase {} Compare Rank'.format(i+1)
        item[phase_name] = ranks[i][index]
    item['Average of all ranks'] = averages[index]
    item['Consolidated performance rank'] = consolidated_rank[index]

# Output
# pprint.pprint(bwh_dict)

# Output to file
with open('benchmarks_bwh_consolidated.json', 'w') as outfile:
    json.dump(bwh_dict, outfile, indent=2)



### Begin export to CSV
import csv

# Link to Python Dictionary
bwh_csv_dict = bwh_dict

# Required to specify Python dictionary keys to export to CSV
# FIND USING.... jq '.[] | keys' benchmarks_bwh_consolidated.json | sort -u
bwh_csv_columns = ['_id', 'type', 'benchmarkType', 'certificationNumber', 'certificationDate', 'pdfUrl', 'sapTechnologyRelease', 'operatingSystem', 'databaseRelease', 'nodesNumber', 'cpuArchitecture', 'cpuSpeed', 'cache', 'status', 'phase1DL', 'phase2QE', 'phase2RS', 'phase3RT', 'serverName', 'cores', 'threads', 'memory', 'additionalInfo', 'persistentMemory', 'serverMemory', 'c:benchmark-version', 'c:bwh-configuration', 'c:bwhconfiguration', 'c:cpu', 'c:database', 'c:environment', 'c:initial-records', 'c:memory-type', 'c:operating-system', 'c:processors', 'c:software-release', 'c:technology-partner','calc:phase1_compare_1billion_secs_avg-low_is_best','calc:phase2_compare_query_records_parse_per_hr-high_is_best','calc:phase2_compare_complex_query_records_parse_per_min-high_is_best', 'Phase 1 Compare Rank', 'Phase 2 Compare Rank', 'Phase 3 Compare Rank', 'Average of all ranks', 'Consolidated performance rank']

# File to export to
bwh_csv_file = "output_bwh_" + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + ".csv"

try:
    with open(bwh_csv_file, 'w') as bwh_csvfile:
        writer = csv.DictWriter(bwh_csvfile, fieldnames=bwh_csv_columns)
        writer.writeheader()
        for data in bwh_csv_dict:
            writer.writerow(data)
except IOError:
    print("I/O error when creating CSV")
