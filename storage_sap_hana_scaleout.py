#!/bin/python

# SAP HANA scale-up configuration storage requirements

# SAP HANA storage requirements:
# https://www.sap.com/documents/2015/03/74cdb554-5a7c-0010-82c7-eda71af511fa.html

hana_scaleout_ram = 256
hana_type = "appliance" # appliance or tdi

hana_scaleout_node_controller = 1
hana_scaleout_node_worker = 6
hana_scaleout_node_standby = 1


hana_scaleout_node_total = hana_scaleout_node_controller + hana_scaleout_node_worker + hana_scaleout_node_standby
hana_scaleout_node_active = hana_scaleout_node_controller + hana_scaleout_node_worker

# Input RAM amount and whether SAP HANA is an Appliance or TDI
# then return /hana/data storage requirement
def hana_scaleout_storage_data_calc(input_ram, input_type):
    if input_type == "appliance":
        return input_ram*3
    elif input_type == "tdi":
        return input_ram*1.2

hana_scaleout_storage_log_max = 512

# Input RAM amount and whether SAP HANA is an Appliance or TDI
# then return /hana/data storage requirement
def hana_scaleout_storage_shared_calc(input_ram, input_node_worker):
    if 0 <= input_node_worker <= 4:
        return input_ram
    elif 5 <= input_node_worker <= 8:
        return input_ram*2
    elif 9 <= input_node_worker <= 12:
        return input_ram*3
    elif 13 <= input_node_worker <= 14:
        return input_ram*4
    else:
        print("check_support: 16 Total Nodes is maximum by default (i.e. 15 Active Nodes = 1 Controller + 14 Worker")

    
hana_scaleout_storage_shared_max = 1024
    
hana_scaleout_storage = {
    '/': 10,
    '/tmp:': 10,
    '/usr/sap': 50,
    '/sapmnt': 50,
    '/swap': 2,
    '/hana/data': hana_scaleout_storage_data_calc(hana_scaleout_ram,hana_type),
    '/hana/log': min(hana_scaleout_storage_log_max, hana_scaleout_ram*0.5),
    '/hana/shared': hana_scaleout_storage_shared_calc(hana_scaleout_ram,hana_scaleout_node_worker)
}
