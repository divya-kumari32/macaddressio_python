# MAC Address Vendor lookup CLI
A simple script to query https://api.macaddress.io/

## Getting Started
This scripting utility has be written using the standard library included in python 3.x All you need to get started is sign up for an account [here](https://macaddress.io/signup) and obtain your API key.

## Prerequisites
You need a standard installation of Python3 that can be obtained [here](https://www.python.org/downloads/)

## Usage
Export the API key as an environment variable macaddrio_api_key before running the script.

On linux and MacOS

Example: (fake API Key used)

```bash
export  macaddrio_api_key=at_VKIvhPfcPffhywNDMx61r0E1gAhKW
```

```bash
 ./main.py E8-40-40-79-C8-60
 ```
 
 This should give output of the company name. For the above example it would show:

```bash
Cisco Systems, Inc
```

**NOTE** The script does partial matches of the query value as well. 

```text
usage: main.py [-h] [-o OUTPUT] [-q QUERY] [-r] [-v] macaddress

Query macaddress.io and fetch the vendor information associated with the mac address

positional arguments:
  macaddress               MAC Address of the device

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output format control, accepted values are json, csv,minimal
  -q QUERY, --query QUERY
                        query fields, one or multiple comma seperated eg. name,transmission,valid,blockfound
  -r, --rawjson         return raw json from the server that can be piped to jq for other fields
  -v, --verbose         make output more verbose sets to DEBUG
```

### Examples

`./main.py E8:40:40:79:C8:60 --query "name,valid"`

Output:

```text
name="Cisco Systems, Inc"
valid="True"
```

`./main.py E8:40:40:79:C8:60 --query "name,valid" --output csv`

Output:

```text
name,valid
"Cisco Systems, Inc","True"
```
## Running with Docker

For your convenience a Dockerfile has also been provided along with the code.

 docker run --env macaddrio_api_key=<your_api_key> <image_name> <MAC_ADDRESS> <OPTIONAL_PARAMS>

Either build it yourself or you can use the one below:

Example:

```bash
docker run --env macaddrio_api_key=at_2JZmaU1wWAO6U1Ro5jDITfsyuMuDK macaddressio E8-40-40-79-C8-60
```
## Security

While the docker image build process does have an optional argument to take the `macaddrio_api_key` key with the build process, it is not a good idea to use it non-local environments. This is only meant for image build on your local machine.

Relying on MAC address vendor information to detect atypical devices in your network by itself isn't a complete security guarantee. An attacker can easily change the MAC address of their machine to match the trusted MAC address value. Security features like DHCP Snooping can be used to reduce attacka like MitM(Man in the Middle), etc. 


