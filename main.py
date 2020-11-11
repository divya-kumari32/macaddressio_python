#!/usr/bin/env python3

import json
import sys
import os
import re
import logging
import urllib.request
import argparse

""" Basic logging """
logging.basicConfig(
    level=logging.WARN,
    format="%(levelname)s %(asctime)s %(message)s",
    handlers=[logging.FileHandler("main.log"), logging.StreamHandler()],
)

def confirm_macaddr(macaddress):

    """ Function to validate MAC Address (returns boolean)"""
    return re.match("^([0-9A-Fa-f]{2}[:.-]?){5}([0-9A-Fa-f]{2})$", macaddress.strip())

def buildrequest(macaddress, api_key):

    requrl = "https://api.macaddress.io/v1"                                      
    auth_header = {"X-Authentication-Token": api_key}                            
    queryparams = {"output": "json","search": macaddress}                        
    encode_url = "{0}?{1}".format(requrl, urllib.parse.urlencode(queryparams))   
    req = urllib.request.Request(encode_url,headers = auth_header)                
    return req 

def sendrequest(req):

    try:
        res = urllib.request.urlopen(req)       
        output = res.read().decode("utf-8")     
        return output   

    except urllib.error.HTTPError:
        logging.error("status_code:{0} message: {1}".format(res.status,res.msg))  
        exit(res.status)

    finally:
        res.close()

def recursive_param_lookup(res_arr):
    
    for param, value in res_arr.items():
        if type(value) is dict:
            yield(param)
            yield from recursive_param_lookup(value)
        else:
            yield(param)


def match_param(res_arr,query):

    param_list = []

    for param in recursive_param_lookup(res_arr):
        param_list.append(param)
    
    for param in param_list:
        if query.lower() in param.lower():
            return param
    
    return None

def recursive_mac_lookup(param,res_arr):
    
    if param in res_arr:
        return res_arr[param]
    
    for val in res_arr.values():
        if isinstance(val, dict):
            nested_val = recursive_mac_lookup(param,val)
            if nested_val is not None:
                return nested_val
    
    return None


def formatted_Output(response,queries,output_type):

    output_array = {} 
    output_str = ""
    try:
        response_array = json.loads(response)
        for query in queries:
            for key in response_array.keys():
                if response_array[key].get(query):
                    output_array[query] = response_array[key].get(query)
                
            # search_param = match_param(response_array,query)
            # if search_param is not None:
            #     search_val = recursive_mac_lookup(search_param,response_array)
            #     output_array[query] = search_param
            # else:
            #     output_array[query] = None
    
    except ValueError as e:
        logging.error("Error in JSON Output")

    if output_type == "json":
        output_str = json.dumps(output_array)
    elif output_type == "csv":
        output_str = (
            ",".join(output_array.keys())
            +"\n"
            +",".join('"{0}"'.format(val) for val in output_array.values())
        )
    else:
        if len(output_array) == 1:
            output_str = next(iter(output_array.values()))
        else:
            output_str = "\n".join(
                "{!s}={!s}".format(key, val) for (key, val) in output_array.items()
            )

    return output_str


def main():

    parser = argparse.ArgumentParser( description = "Simple python script to query macaddress.io and fetch details of the respective Vendor")

    parser.add_argument("macaddress",help = "Mac Address of the Device",type = str)

    parser.add_argument("-o","--output",help = "Output Format, json or csv only",dest = "output",default="minimal",)

    parser.add_argument("-q","--query",help = "Query Fields",dest = "queryfields",default = "companyName")

    parser.add_argument("-r","--rawjson",help = "Return raw JSON",action = "store_true")

    parser.add_argument("-v","--verbose",help="make output more verbose sets to DEBUG",action="store_true")

    args = parser.parse_args()
    macaddress = args.macaddress
    queryfields = args.queryfields
    output_type = args.output

    if args.verbose:
        logging.basicConfig(level = logging.DEBUG)

    try:
        api_key = os.environ["macaddrio_api_key"]
        if api_key == "":
            logging.error("Please set environment variable with the name macaddrio_api_key")
            sys.exit(1)
    
    except KeyError:
        logging.error("Please set environment variable with the name macaddrio_api_key")
        sys.exit(1)
    
    if not confirm_macaddr(macaddress):
        logging.error("Please type valid MAC Address")
        sys.exit(1)
    
    response = sendrequest(buildrequest(macaddress, api_key))

    if args.rawjson:
        print(response)
        sys.exit(0)

    queries = [q.strip() for q in queryfields.split(",")]

    print(formatted_Output(response,queries,output_type))

if __name__ == "__main__":
    main()