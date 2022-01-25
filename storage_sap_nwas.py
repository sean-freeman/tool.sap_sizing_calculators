#!/bin/python

# NetWeaver Storage requirements are based on
# SAP Note 1597355 - Swap-space recommendation for Linux
### https://launchpad.support.sap.com/#/notes/1597355

nwas_ram = 128


# Input RAM amount, if RAM between minimum and maximum
# then return swap space storage requirement
def nwas_storage_swap_calc(input_ram):
    
    if 0 <= input_ram <= 9:
        return 20
    elif 10 <= input_ram <= 15:
        return 32
    elif 16 <= input_ram <= 31:
        return 64
    elif 32 <= input_ram <= 63:
        return 64
    elif 64 <= input_ram <= 127:
        return 96
    elif 128 <= input_ram <= 255:
        return 128
    elif 256 <= input_ram <= 511:
        return 160
    elif 512 <= input_ram <= 1023:
        return 192
    elif 1024 <= input_ram <= 2047:
        return 224
    elif 2048 <= input_ram <= 4095:
        return 256
    elif 4096 <= input_ram <= 8192:
        return 288
    else:
        return 320


nwas_storage_swap = nwas_storage_swap_calc(nwas_ram)

nwas_storage = {
    '/': 10,
    '/tmp:': 10,
    '/usr/sap': 50,
    '/sapmnt': 50,
    '/swap': nwas_storage_swap
}
