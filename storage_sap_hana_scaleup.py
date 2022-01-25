#!/bin/python

# SAP HANA scale-up configuration storage requirements

# SAP HANA storage requirements:
# https://www.sap.com/documents/2015/03/74cdb554-5a7c-0010-82c7-eda71af511fa.html

hana_scaleup_ram = 256
hana_type = "appliance" # appliance or tdi


# Input RAM amount and whether SAP HANA is an Appliance or TDI
# then return /hana/data storage requirement
def hana_scaleup_storage_data_calc(input_ram, input_type):
    if input_type == "appliance":
        return input_ram*3
    elif input_type == "tdi":
        return input_ram*1.2

hana_scaleup_storage_log_max = 512
hana_scaleup_storage_shared_max = 1024
    
hana_scaleup_storage = {
    '/': 10,
    '/tmp:': 10,
    '/usr/sap': 50,
    '/sapmnt': 50,
    '/swap': 2,
    '/hana/data': hana_scaleup_storage_data_calc(hana_scaleup_ram,hana_type),
    '/hana/log': min(hana_scaleup_storage_log_max, hana_scaleup_ram*0.5),
    '/hana/shared': min(hana_scaleup_storage_shared_max, hana_scaleup_ram*1)
}
