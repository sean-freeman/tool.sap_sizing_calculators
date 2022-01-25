# sap_sizing_calculators Python scripts

These Python scripts execute various calculations to assist SAP Technical Administrators in sizing decisions for designing and deploying SAP Landscapes.

Each is rudimentary self-contained Python script at this time.

## Functionality

These Python scripts perform the following:

| Python script | Description | Output |
| --- | --- | --- |
| `sap_benchmarks_bwh_directory.py` | Extract all benchmark records from SAP BWH Directory, and apply calculations for pro-rata comparisons of all records in running SAP BW and SAP BW/4HANA | CSV file |
| `sap_benchmarks_sd_directory.py` | Extract all benchmark records from SAP SD Directory | CSV file |
| `sap_hana_hardware_directory_iaas.py` | Extract all Cloud IaaS records from SAP HANA Hardware Directory, categorise and provide calculations for DRAM per CPU Thread and the CPU to DRAM (Memory) ratios | CSV file |
| `storage_sap_hana_scaleout.py` | Calculate storage requirements for SAP HANA in scale-`out` configuration, with Appliance or TDI calculations | Python variables with sizing |
| `storage_sap_hana_scaleup.py` | Calculate storage requirements for SAP HANA in scale-`up` configuration, with Appliance or TDI calculations | Python variables with sizing |
| `storage_sap_nwas.py` | Calculate storage requirements for SAP NetWeaver AS (ABAP), including swap partition/file | Python variables with sizing for SAP NetWeaver |

## Execution examples

Each can be called with `python3 ./filename.py`

## Requirements, Dependencies and Testing

### Python requirements

Python 3, with requests and json modules. See necessary install:
```
pip3 install requests json
```

### Testing

**Tests with Python release versions:**
- Python 3.9.7 (i.e. CPython distribution)

**Tests with Operating System release versions:**
- macOS 11.6.x (Big Sur), with Homebrew used for Python 3.x via PyEnv
- macOS 12.0.x (Monterey), with Homebrew used for Python 3.x via PyEnv

## License

- Apache 2.0


## Development notes

### SAP HANA Hardware Directory

SAP HANA Hardware Directory's `solutions.json` contains different solutionType:
- appliance, i.e. Certified Appliances
- storage, i.e. Certified Enterprise Storage
- hci, i.e. Certified HCI Solutions
- iaas, i.e. Certified IaaS Platforms
- intel, i.e. Supported Intel Systems
- power, i.e. Supported Power Systems

Logic applied:
- Filter anything that is not solutionType = iaas in hwd_solutions
- For each '_id' in hwd_solutions
  - find 've:*' in hwd_vendors
  - find valueIds 'v:*' in hwd_categories


### SAP SD Benchmark Directory

Logic applied:
- for each '_id' in benchmarks_sd
  - find 'v:*' in benchmarks_categories


### SAP BWH Benchmark Directory

Logic applied:
- for each '_id' in benchmarks_sd
  - find 'v:*' in benchmarks_categories