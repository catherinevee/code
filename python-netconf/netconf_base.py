#! /usr/bin/env python
from ncclient import manager
import colorama
from colorama import Fore, Style, init, Back
# colorama needs to initialize for colored text to show in Windows
# after a colored text line appears, auto-reset to plain (white) text
# these colors add additional characters to the string, so the color values are concatenated
# into the string
init(autoreset=True)
colorama.init()
device = {
"host":"10.dsfds.110.81",
"port":"830",
"username":"sdfsdf",
"password":"sdfsdfsdf!",
}

def netconf_base_connection(device):
    try:
        print(f"\nTASK: [ATTEMPTING NETCONF CONNECTION TO {device['host']}]  **********************")
        with manager.connect(host=device["host"], port=device["port"],
                             username=device["username"],
                             password=device["password"],
                             hostkey_verify=False) as m:
            print(f"\n{Fore.GREEN}ok: [SUCCESSFUL CONNECTION TO {device['host']}]{Style.RESET_ALL}")
            for capability in m.server_capabilities:
                print(capability)
        return m
    except Exception as e:
        print(f"\n{Fore.YELLOW}requiresattention: [UNABLE TO CONNECT TO {device['host']}]")
        print(f"{Fore.YELLOW}       {e}{Style.RESET_ALL}")

 
def netconf_editconfig_fromyaml():
    print(f"\nTASK: [FROM FILE, EDITING CONFIG ON {device['host']}]  **********************")
    

if __name__ == '__main__':
    netconf_base_connection(device)