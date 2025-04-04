import paramiko
from fabric import Connection, Config
from invoke import Responder
import json
import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
from requests.auth import HTTPBasicAuth
import colorama
from colorama import Fore, Style, init, Back
# colorama needs to initialize for colored text to show in Windows
# after a colored text line appears, auto-reset to plain (white) text
# these colors add additional characters to the string, so the color values are concatenated
# into the string
init(autoreset=True)
colorama.init()
from dnacentersdk import api, ApiError
from infoblox_client import connector
from infoblox_client.object_manager import InfobloxObjectManager
from infoblox_client import objects, exceptions
import netmiko
from datetime import date
from panos import base
from panos import firewall
from panos import panorama
from panos import policies
from panos import objects
from panos import network
from panos import device
from panos.panorama import Panorama, DeviceGroup, PanoramaCommitAll
from panos.objects import *
from panos.firewall import Firewall
from panos.policies import NatRule, Rulebase, PostRulebase
from panos.device import Vsys

#========================
#Parameters that require changing on each script run
#========================
# newdevice_is_wired = True
newdevice_is_wired = False
newdevice_mac = "2C:54:91:A8:BC:5A"
gamingdevicenumber = "1"

if newdevice_is_wired:
    objectname = f"HousingGamingDevice{gamingdevicenumber}"
    newdevice_description = f"Gaming console used for Housing {date.today()}, MAC of device is {newdevice_mac}"
else:
    objectname = f"HousingGamingDevice{gamingdevicenumber}"
    newdevice_description = f"Wireless gaming console used for Housing {date.today()}, MAC of device is {newdevice_mac}"
#-------------------------------
#device (console or PC) on wired
newdevice_wired_ip = "10.1.3.21"
#-------------------------------
#Gaming Console on wireless
#WWUwireless-Guest
newdevice_wireless_ip = "10.111.192.21"
#-------------------------------


def InfobloxWork():
    infoblox_username = "dfgdfg"
    infoblox_password = "fdgdfgfdg!0"
    infoblox_ip = "10.249.12.135"
    #additional global parameters to provide to API calls
    #to check the WAPI version, go to https://10.249.12.135/wapidoc/
    infoblox_wapi_version = "2.11.3"
    
    def InfobloxAuth():
        print(f"{Fore.YELLOW}Compiling Infoblox connection data and payload options...{Style.RESET_ALL}")
        #define connection parameters here to connect to Infoblox

        dnsview = "InternalView"
        networkview = "sfdfs"
        base = f"https://{infoblox_ip}/wapi/v{infoblox_wapi_version}/"
        auth = HTTPBasicAuth(infoblox_username, infoblox_password)

        #define Dictionary containing parameters for the infoblox_client Library
        opts = {
        'host': infoblox_ip,
        'username': infoblox_username,
        'password': infoblox_password
        }
        #construct a Connector object, used to simplify API calls
        conn = connector.Connector(opts) 
        #construct the InfobloxObjectManager, used for particular tasks
        ibom = InfobloxObjectManager(conn)
        #define base URL, concatenate different URIs to it later
        #define headers which define the type of data to expect and send
        accept_header = "application/yang-data+json"
        content_type_header = "application/json"
        #create headers Dictionary, used to construct the URL
        headers = {
            "Accept": accept_header,
            "Content-Type": content_type_header
        }
        return auth, headers, dnsview, base
     

    def HandleStatusCodes(
        response,
        successfulmessage="Successful operation",
        printout=True,
        exitonerror=True,
    ):
        statuscode = response.status_code
        response_content = response.content.decode("UTF-8")
        if statuscode == 200 or statuscode == 201:
            print("\n============================")
            print(f"{Back.GREEN}{statuscode}{Style.RESET_ALL}: {successfulmessage}")
            if printout is True:
                print(response_content)
            else:
                pass
            print("============================")
        else:
            print("\n============================")
            if exitonerror is True:
                print(
                    f"{Back.MAGENTA}{statuscode}{Style.RESET_ALL}: Unsuccessful operation. Stopping script."
                )
                print(Back.MAGENTA + json.loads(response.text).get("text"))
                exit()
            elif exitonerror is False:
                print(
                    f"{Back.MAGENTA}{statuscode}{Style.RESET_ALL}: Unsuccessful operation. Suppressing error."
                )
                print(Fore.MAGENTA + json.loads(response.text).get("text"))
            print("============================")

    def RestartServices(
        ip=infoblox_ip, wapi_version=infoblox_wapi_version, username=infoblox_username, password=infoblox_password
    ):
        auth = HTTPBasicAuth(username, password)
        # define headers which define the type of data to expect and send
        accept_header = "application/yang-data+json"
        content_type_header = "application/json"
        # create headers Dictionary, used to construct the URL
        headers = {"Accept": accept_header, "Content-Type": content_type_header}
        base = f"https://{ip}/wapi/v{wapi_version}/"
        # ===================================
        # Get the Grid ID from Infoblox
        # ===================================
        # construct the base URL to access the Infoblox Grid reference
        # the Grid reference is a set of characters unique to an Infoblox instance
        url = f"{base}grid"

        # attempt to connect to the target with a GET request using pre-defined
        # connection variables and the URL to get the Grid ID
        try:
            response = requests.get(url, headers=headers, auth=auth, verify=False)
        # If a RESTCONF connection (i.e. HTTPS connection to the device can't be created) fails,
        # catch the exception, print out status, and stop script
        except requests.exceptions.ConnectionError:
            print(f"\n{Fore.RED}ConnectionError:")
            print(
                f"Unable to establish a RESTCONF / HTTPS connection with {Fore.YELLOW}{host}{Style.RESET_ALL}."
            )
            exit()
        # ===================================
        # Attempt to restart DHCP/DNS services
        # ===================================
        # If a RESTCONF connection (i.e. HTTPS connection to the device can't be created) returns a 404,
        # catch the exception, print out status, and stop script
        if response.status_code == 200:
            # convert the response to JSON
            reply = json.loads(response.text)
            # parse out the grid_id from the response
            # the response is initially a List (with one index), which returns a dictionary
            # get the value of the "_ref" key, which returns a string
            # the string is separated by a "/" and the second value is the actual grid_id
            grid_id = list(reply)[0].get("_ref").split("/")[1]
            # construct the URL with the function needed to restart DNS/DHCP services
            url = f"{base}grid/{grid_id}/?_function=restartservices"
            # construct the payload Python Dictionary that will become a JSON string in the request
            payload = {"member_order": "SIMULTANEOUSLY", "service_option": "ALL"}
            # try sending the POST request with the payload
            try:
                response = requests.post(
                    url, headers=headers, auth=auth, json=payload, verify=False
                )
            # If a RESTCONF connection (i.e. HTTPS connection to the device can't be created) fails,
            # catch the exception, print out status, and stop script
            except requests.exceptions.ConnectionError:
                print(f"\n{Fore.RED}ConnectionError:")
                print(
                    f"Unable to establish a RESTCONF / HTTPS connection with {Fore.YELLOW}{host}{Style.RESET_ALL}."
                )
                exit()
            # call on HandleStatusCodes to display certain terminal messages based on the status code
            # pass in the status code and the message to display when a 200 is received
            HandleStatusCodes(
                response, "DHCP/DNS Services successfully restarted.", printout=False
            )
        else:
            print(
                f"{Back.MAGENTA}{statuscode}{Style.RESET_ALL}: Failed operation. Stopping script."
            )
            print(response.text)
            exit() 


    result = InfobloxAuth()
    auth = result[0]
    headers = result[1]
    dnsview = result[2]
    base = result[3]
    # print(f"\nAttempting to create the Host record for {Fore.YELLOW+fqdn+Style.RESET_ALL} with below payload...")
    # print(addressesList)
    #construct URL for modifying Host records
    url = f"{base}fixedaddress"   

    print(f"{Fore.YELLOW}Contacting {url}...{Style.RESET_ALL}")
    if newdevice_is_wired:
        print(f"{Fore.YELLOW}Compiling payload for wired device...{Style.RESET_ALL}")
        payload = {
            "ipv4addr":newdevice_wired_ip,
            "restart_if_needed":True,
            "mac": newdevice_mac,
            "comment": newdevice_description
            }
    else:
        print(f"{Fore.YELLOW}Compiling payload for wireless device...{Style.RESET_ALL}")        
        payload = {
            "ipv4addr":newdevice_wireless_ip,
            "restart_if_needed":True,
            "mac": newdevice_mac,
            "comment": newdevice_description
            
            }
    print("\nUsing payload:")
    print(payload)
    
    #try sending the POST request with the payload
    try:
        response = requests.post(url, headers=headers, auth=auth, json = payload, verify=False)
    #If a RESTCONF connection (i.e. HTTPS connection to the device can't be created) fails,
    #catch the exception, print out status, and stop script
    except requests.exceptions.ConnectionError:
        print(f"\n{Fore.RED}ConnectionError:")
        print(f"Unable to establish a RESTCONF / HTTPS connection with {Fore.YELLOW}{host}{Style.RESET_ALL}.")
        exit()
        
    print(f"\nReturned status code: {Back.MAGENTA+str(response.status_code)+Style.RESET_ALL}")
    # print(response.text)
    RestartServices()




def ISEWork():
    endpointidentitygroup = "GamingConsoles"
    endpointidentitygroup_groupid = "8c5a6980-cbd9-11ec-91cb-d6a393c76533"
    
    def ISE_CreateEndpoint(newdevice_mac, newdevice_description):
        # ===========================
        # ===========================
        ise_server = "ise1.net.sdf.sdfsfsd"
        ers_port = "9060"
        ers_api_username = "sdfdsfs"
        ers_api_password = "0akf18dl4m5bc9s"

        auth = HTTPBasicAuth(ers_api_username, ers_api_password)
        accept_header = "application/json"
        content_type_header = "application/json"
        headers = {
            "Accept": accept_header,
            "Content-Type": content_type_header,
        }
        url_base = "https://{h}:{p}".format(h=ise_server, p=ers_port)
        url = url_base + "/ers/config/endpoint"
        # ===========================
        # ===========================

        def ConstructCreatePayload():
            payload = json.dumps(
                {
                    "ERSEndPoint": {
                        "newdevice_description": newdevice_description,
                        "mac": newdevice_mac,
                        "staticProfileAssignment": "false",
                        "staticGroupAssignment": "true",
                        "groupId": endpointidentitygroup_groupid,
                    }
                }
            )

            response = requests.post(
                url, data=payload, headers=headers, auth=auth, verify=False
            )
            return response

        print(f"Contacting ISE ERS and creating the endpoint {newdevice_mac}...")
        response = ConstructCreatePayload()
        print("Payload sent.\n")

        # if the status_code returns a 500 error, delete the endpoint by its endpoint ID, then
        # try adding the device again

        if int(response.status_code) == 500:
            print(
                f"{Fore.YELLOW}500 Status Code received{Style.RESET_ALL} - Endpoint already exists. Need to delete and re-create the Endpoint."
            )
            get_endpoint_url = url + "?filter=mac.EQ." + newdevice_mac
            response = requests.get(
                get_endpoint_url, headers=headers, auth=auth, verify=False
            )

            device_id = str(
                response.json().get("SearchResult").get("resources")[0].get("id")
            )
            delete_endpoint_url = url + "/" + device_id

            response = requests.delete(
                delete_endpoint_url, headers=headers, auth=auth, verify=False
            )
            print(
                f"\n{Fore.CYAN}Deleted Endpoint {Style.RESET_ALL} ({newdevice_mac}) ({delete_endpoint_url})"
            )

            ConstructCreatePayload()
            print(
                f"\n{Fore.CYAN}Re-created Endpoint {Style.RESET_ALL} ({newdevice_mac}) + placed into group {endpointidentitygroup}."
            )
            print(f"({str(response.status_code)})")

        else:
            print(
                f"\n{Fore.CYAN}Created Endpoint {Style.RESET_ALL} ({newdevice_mac}) + placed into group {endpointidentitygroup}."
            )

            print(f"({str(response.status_code)})")

        return

    ISE_CreateEndpoint(newdevice_mac, newdevice_description)



def PanoramaWork():

    nat_type = "ipv4"



    panorama_server = "panorama.net.sdfs.sdfsdf"
    base_url = "https://" + panorama_server + "/"
    palo_username = "sdfsd"
    palo_password = "dsfdsf!"

    panorama_fw_object = Panorama(panorama_server, palo_username, palo_password)
    # panorama_fw_object.commit()

    def PaloRESTCONF_CreateAddressObject(objectname, ipaddress):
        print(f"Creating the address object on Panorama ({panorama_server})...")
        panorama_createaddressobject = AddressObject(
            objectname, ipaddress, description=newdevice_description
        )
        panorama_fw_object.add(panorama_createaddressobject)
        panorama_createaddressobject.create()
        print(
            f"...address object {Fore.YELLOW+panorama_createaddressobject.value+Style.RESET_ALL} created."
        )
        # ipaddress = f"{ipaddress}/32" delete if not needed?

    def PaloRESTCONF_CreateNATPolicy():
        rulebase = panorama_fw_object.add(PostRulebase())
        print(
            f"Creating the NAT Policy on Panorama ({panorama_server}) in ({rulebase.vsys})..."
        )

        NATRuleParameters = {
            "name": natrulename,
            "newdevice_description": natrulenewdevice_description,
            "nat_type": nat_type,
            "fromzone": ["Guest_Wireless"],
            "tozone": ["Untrust"],
            "source": objectname,
            "source_translation_type": "dynamic-ip",
            "source_translation_translated_addresses": publicipaddress,
        }
        new_nat_rule = rulebase.add(NatRule(**NATRuleParameters))
        new_nat_rule.create()
        print("...rule created:")
        natruleabout_dict = new_nat_rule.about()
        print(json.dumps(natruleabout_dict, indent=3))
    if newdevice_is_wired:
        PaloRESTCONF_CreateAddressObject(objectname, newdevice_wired_ip)
    else:
        PaloRESTCONF_CreateAddressObject(objectname, newdevice_wireless_ip)





#run all modules together
if __name__ == "__main__":
    ISEWork()
    InfobloxWork()
    PanoramaWork()




