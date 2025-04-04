from infoblox_client import connector
from infoblox_client.object_manager import InfobloxObjectManager
from infoblox_client import objects, exceptions
import yaml
import requests
from requests.auth import HTTPBasicAuth
import json
import csv
import time
requests.packages.urllib3.disable_warnings()
import colorama
from colorama import Fore, Style, init, Back
from datetime import date
import xmltodict

init(autoreset=True)
colorama.init()
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

# =============================================================
# editable fields
# =============================================================
# MAC needs to be in colon (or without delimiter), not dash notation
ipv4_subnet = "10.111.254."
public_ipv4_subnet = "6666666.666666.53."

# =============================================================
# non-editable, dynamic fields
# objectname = f"GamingConsole_{devicenumber}"
objectdescription = "This can be any gaming device needing a static NAT for online gameplay"

# natrulename = f"Housing_GamingDeviceNAT-ToInternet{devicenumber}"
natruledescription = (
    f"Allow gaming consoles used in the housing networks out to the internet for improved NAT scores in P2P games"
)


# =============================================================
# script start
# =============================================================


def Panorama_API_CALL(objectname, natrulename, next_private_ip_address, next_public_ip_address):
    nat_type = "ipv4"
    panorama_server = "panorama.net.sdf.sdfsfds"
    base_url = "https://" + panorama_server + "/"
    palo_username = "sdfaaddsf"
    palo_password = "sdfsdfsfwef!"

    panorama_fw_object = Panorama(panorama_server, palo_username, palo_password)
    panorama_device_group = DeviceGroup("Campus")
    panorama_fw_object.add(panorama_device_group)
    
    # panorama_fw_object.commit()

    def PaloRESTCONF_CreateAddressObject(objectname, next_private_ip_address):
        print(f"Creating the address object on Panorama ({panorama_server})...")
        panorama_createaddressobject = AddressObject(
            objectname, next_private_ip_address, description=objectdescription,
        )
            
        panorama_fw_object.add(panorama_createaddressobject)
        panorama_createaddressobject.create()
        print(
            f"...address object {Fore.YELLOW+panorama_createaddressobject.value+Style.RESET_ALL} created."
        )

    def PaloRESTCONF_CreateNATPolicy():
        rulebase = panorama_device_group.add(PostRulebase())
        
        print(
            f"Creating the NAT Policy on Panorama ({panorama_server}) in ({rulebase.vsys})..."
        )

        NATRuleParameters = {
            "name": natrulename,
            "description": natruledescription,
            "nat_type": nat_type,
            "fromzone": ["Guest_Wireless"],
            "tozone": ["Untrust"],
            "source": objectname,
            "tag": "Housing",
            "source_translation_type": "static-ip",
            "source_translation_static_translated_address": str(next_public_ip_address),
        }
        new_nat_rule = rulebase.add(NatRule(**NATRuleParameters))
        new_nat_rule.create()
        print("...rule created.")
        natruleabout_dict = new_nat_rule.about()
        # print(json.dumps(natruleabout_dict, indent=3))

    PaloRESTCONF_CreateAddressObject(objectname, next_private_ip_address)

    PaloRESTCONF_CreateNATPolicy()


if __name__ == "__main__":
    for i in range(220):
        starting_ip_address = 20
        next_private_ip_address = f"{ipv4_subnet}{starting_ip_address+int(i)}"
        next_public_ip_address = f"{public_ipv4_subnet}{starting_ip_address+int(i)}"
        
        
        objectname = f"GamingDeviceStaticNAT_{i}"
        
        
        natrulename = f"Housing_GamingDeviceStaticNAT-ToInternet{i}"
        
        print(f"{natrulename} -- {objectname} -- {str(next_private_ip_address)} -- {str(next_public_ip_address)} ")
        Panorama_API_CALL(objectname, natrulename, next_private_ip_address, next_public_ip_address)
        time.sleep(1)
