import requests
from requests.auth import HTTPBasicAuth
import os
import sys
requests.packages.urllib3.disable_warnings()
from dnacentersdk import api, ApiError


DNAC_URL = ""
DNAC_USER = ""
DNAC_PASS = ""

def get_auth_token():
    """
    Building out Auth request. Using requests.post to make a call to the Auth Endpoint
    """
    url = 'https://{}/dna/system/api/v1/auth/token'.format(DNAC_URL)                      # Endpoint URL
    hdr = {'content-type' : 'application/json'}                                           # Define request header
    resp = requests.post(url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASS), headers=hdr)      # Make the POST Request
    token = resp.json()['Token']                                                          # Retrieve the Token
    print("Token Retrieved: {}".format(token))                                            # Print out the Token
    return token    # Create a return statement to send the token back for later use


def GetSitesFromDNAC():
    print(f"{Back.MAGENTA}vvvv RETRIEVING SITE DATA FROM DNAC INVENTORY**vvvvvvvvvvvvvvvvvvvvvvv INFO {Style.RESET_ALL}")
  
    api_ = api.DNACenterAPI(
        base_url=f'https://{dnac}:443',
        version='2.2.3.3', 
        username = dnac_user,
        password = dnac_password,
        verify = False
        )
    try:
        devices = api_.sites.get_site()
        for device in devices.response:
            siteNameHierarchy = device.get("siteNameHierarchy")
            if "Floor" in siteNameHierarchy:
                continue
            else:
                siteid = device.get("id")
                sitename = device.get("name")
                print(sitename, siteid)
            
    except ApiError as e:
        print(e)  


def GetDevices():
    print(f"{Back.MAGENTA}vvvv GET DNAC DEVICES**vvvvvvvvvvvvvvvvvvvvvvv INFO {Style.RESET_ALL}")
        
    api_ = api.DNACenterAPI(
        base_url=f'https://{dnac}:443',
        version='2.2.3.3', 
        username = dnac_user,
        password = dnac_password,
        verify = False
        )
    try:
        devices = api_.devices.get_device_detail(identifier="nwDeviceName", search_by="AC_Test_4503.net.wwu.edu")
        print(devices.response)
        print(devices.response.get("nwDeviceName"))
        print(devices.response.get("nwDeviceId"))
    except ApiError as e:
        print(e)    




if __name__ == "__main__":
    get_auth_token()
