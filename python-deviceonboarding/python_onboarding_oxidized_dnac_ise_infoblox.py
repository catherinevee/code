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


#=====================================
#Parameters needing to be changed after each script run
#=====================================

infoblox_comment = "IS433S31"
newdevice_mac = "aa:cc:bb:bb:cc:b2"
newdevice_ip = "10.56.101.13"


#=====================================
#Parameters NOT needing to be changed after each script run
#but these can be modified depending on the device
#=====================================

newdevice_devicename = infoblox_comment
newdevice_domain_name = ".net.asda.asda"
newdevice_fqdn = newdevice_devicename + newdevice_domain_name
newdevice_os = "ios"
newdevice_networkrole = "Access" #or Distribution



#add device to Oxidized inventory file for Git-driven backups on Netops2
#======================================
def AddToOxidized(newdevice_ip, newdevice_os, newdevice_devicename, newdevice_domain_name):
    #global Oxidized parameters needed to login to Netops2 and write to Inventory file
    oxidized_server = "qqweq.net.qqqw.qqq"
    oxidized_username = "fdgd"
    oxidized_password = "7!dfgfd!"
    root_password = "dgfd.!@"
    oxidized_directory = "/root/.config/oxidized/"
    oxidized_file = "router.db"

    #configuration required for Oxidized portion of the script 
    newdevice_string = f"{newdevice_fqdn}:{newdevice_ip}:{newdevice_os}"
    oxidized_fullpath = oxidized_directory+oxidized_file
    
    #handle Sudo prompts since the Oxidized Inventory file is root-owned
    sudoconfig = Config(overrides={'sudo': {'password': oxidized_password}}) 
    
    #Use Fabric library to establish the SSH connection to Netops2
    sshconnection = Connection(
            host = oxidized_server,
            user=oxidized_username,
            connect_kwargs= {
                "password":oxidized_password
            },
            config=sudoconfig
     
     )
    #send remote command to netops2 
    #print out the last 5 lines of the Oxidized Inventory file to terminal
    #======================================
    def PrintLastLinesOfOxidizedInventoryFile():
        print(f"{Back.MAGENTA}vvvv OXIDIZED INVENTORY FILE TAIL-5**vvvvvvvvvvvvvvvvvvvvvvv INFO  {Style.RESET_ALL}")
        cmd = f"tail -5 {oxidized_fullpath}"
        sshconnection_output = sshconnection.sudo(cmd, echo=False)   
    #send remote command to netops2 
    #write directly to the Inventory file and append the new device string to it      
    def WriteNewDeviceToOxidizedInventoryFile():
        print(f"{Back.MAGENTA}vvvv OXIDIZED INVENTORY FILE WRITE**vvvvvvvvvvvvvvvvvvvvvvv INFO {Style.RESET_ALL}")
        echocmd = f"sh -c 'echo '{newdevice_string}' >> {oxidized_fullpath}'"
        cmdsshconnection = sshconnection.sudo(echocmd, hide='stderr')        
        print(cmdsshconnection)
    #send remote command to netops2 
    #restart the Oxidized service so that the new device is recognized in the Inventory
    def RestartOxidizedService():
        print(f"{Back.MAGENTA}vvvv OXIDIZED SERVICE RESTART**vvvvvvvvvvvvvvvvvvvvvvv INFO  {Style.RESET_ALL}") 
        print("Restarting oxidized service...")
        restartservicescmd = f"systemctl restart oxidized"
        cmdsshconnection = sshconnection.sudo(restartservicescmd, hide='stderr')
        print(cmdsshconnection)
        #show the current status of Oxidized after restarting the service
        print(f"{Back.MAGENTA}vvvv OXIDIZED SERVICE STATUS**vvvvvvvvvvvvvvvvvvvvvvv INFO  {Style.RESET_ALL}") 
        restartservicescmd = f"systemctl status oxidized"
        cmdsshconnection = sshconnection.sudo(restartservicescmd, hide='stderr')
        print(cmdsshconnection)

    #run all three functions 
    #======================================
    PrintLastLinesOfOxidizedInventoryFile()
    WriteNewDeviceToOxidizedInventoryFile()
    RestartOxidizedService()


#add device to DNAC for appliance-provided inventory        
#======================================
def AddToDNAC(newdevice_ip):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    dnac = "dnac.net.dfgdfg.dfgd"
    baseurl_intent_api = f"https://{dnac}/dna/intent/api/v1"
    dnac_user = "dfgfd"
    dnac_password = "7!fgdfg!"
    dnac_api_userNameValue = "cisco_dnac"
    dnac_api_passwordValue = "zKdQqzrqECNyUNVkLjzGDTwC7fR2"
    dnac_api_snmpphraseValue = "SNMPR3ad!"
    #the software version determines what methods are available in the dnacentersdk
    dnac_software_version = "2.2.3.3"
    #add the device to DNA Center via a DNAC SDK built in Python (dnacentersdk)
    #this includes SNMPv3 and SSH credentials so DNAC can poll the device
    def AddDeviceToDNAC(newdevice_ip):
        print(f"{Back.MAGENTA}vvvv ADD DEVICE TO DNAC INVENTORY**vvvvvvvvvvvvvvvvvvvvvvv INFO {Style.RESET_ALL}")
        payload = {
        "ipAddress": [newdevice_ip],
        "password": dnac_api_passwordValue,
        "enablePassword": dnac_api_passwordValue,
        "userName": dnac_api_userNameValue,
        "type" : "NETWORK_DEVICE",
        "computeDevice" : False,
        "cliTransport" : "SSH",
        "snmpVersion" : "V3",
        "snmpUserName" : dnac_api_userNameValue,
        "snmpMode" : "RW",
        "snmpAuthProtocol" : "SHA",
        "snmpAuthPassphrase" : dnac_api_snmpphraseValue,
        "snmpPrivProtocol" : "AES128",
        "snmpPrivPassphrase" : dnac_api_snmpphraseValue,
        "snmpRetry" : 3,
        "snmpTimeout" : 10,
        }
        #construct the DNACenterAPI object for the connection
        api_ = api.DNACenterAPI(
            base_url=f'https://{dnac}:443',
            version=dnac_software_version, 
            username = dnac_user,
            password = dnac_password,
            verify = False
            )
        #make the POST request to add the device to DNAC    
        try:
            devices = api_.devices.add_device(**payload)
            print(f"[{Fore.GREEN}x{Style.RESET_ALL}] DNA Center Task created to add device to inventory.")
            print(f"        [{Fore.YELLOW}o{Style.RESET_ALL}]Next step: Manually assign the device to a site and a role!")
        except ApiError as e:
            print(e)    
   
    AddDeviceToDNAC(newdevice_ip)   


#add device to ISE as a network device for TACACS+ to work        
#======================================
def AddToISE(newdevice_devicename, newdevice_ip):
    ise_pan_server = "ise1.net.asda.qweq"
    ise_pan_server_ers_port = "9060"
    ise_ss = "qweweq@qweqw"
    ers_api_username = "dfgdgdf"
    ers_api_password = "0akf18ddfgfdgdfgdfgdl4m5bc9s"

    ise_auth = HTTPBasicAuth(ers_api_username, ers_api_password)
    accept_header = "application/json"
    content_type_header = "application/json"
    headers = {
        "Accept": accept_header,
        "Content-Type": content_type_header,
    }

    def AddDeviceToISE(newdevice_devicename, newdevice_ip):
        print(f"{Back.MAGENTA}vvvv ADD NETWORK DEVICE TO ISE**vvvvvvvvvvvvvvvvvvvvvvv INFO {Style.RESET_ALL}")
        #kind of a tricky payload to construct
        payload = json.dumps({
            "NetworkDevice" : {
                "name" : newdevice_devicename,
                "description" : newdevice_devicename,
                "authenticationSettings" : {
                    "networkProtocol" : "RADIUS",
                    "radiusSharedSecret" : ise_ss,                
                },
                "tacacsSettings" : {    
                    "connectModeOptions": "ON_LEGACY",
                    "sharedSecret" : ise_ss,
                },
                "NetworkDeviceIPList" : [
                {
                    "ipaddress" : newdevice_ip,
                    "mask" : 32
                } ],
                "NetworkDeviceGroupList" : [ "Location#All Locations#Weqweq - Campus", "IPSEC#Is IPSEC Device#No", f"Device Type#All Device Types#Wired#{newdevice_networkrole}" ]
                }
            })
        url_base = "https://{h}:{p}".format(h=ise_pan_server, p=ise_pan_server_ers_port)
        url = url_base + "/ers/config/networkdevice"
        response = requests.post(
            url,
            verify=False,
            auth=ise_auth,
            headers=headers,
            data=payload)
            
        if "20" in str(response.status_code):
            print(f"[{Fore.GREEN}x{Style.RESET_ALL}] Successful ERS call to ISE to create {Fore.GREEN+newdevice_devicename+Style.RESET_ALL}/{Fore.GREEN+newdevice_ip+Style.RESET_ALL} as a network device.")
        else:
            print(response)
    AddDeviceToISE(newdevice_devicename, newdevice_ip)


#add a DNS entry for the device in Infoblox        
#======================================
def AddToInfoblox(newdevice_ip, newdevice_mac, newdevice_fqdn):
    #define connection parameters here to connect to Infoblox
    infoblox_username = "qweq"
    infoblox_password = "7!qwqweqw!"
    infoblox_ip = "10.249.12.135"
    #additional global parameters to provide to API calls
    #to check the WAPI version, go to https://10.249.12.135/wapidoc/
    infoblox_wapi_version = "2.11.3"
    dnsview = "InternalView"
    networkview = "qweqw"

    #define Dictionary containing parameters for the infoblox_client Library
    opts = {
    'host': infoblox_ip,
    'username': infoblox_username,
    'password': infoblox_password
    }
    #construct a Connector object, used to simplify API calls
    conn = connector.Connector(opts) 
 
    print(f"{Back.MAGENTA}vvvv CREATE HOST RECORD FOR DEVICE IN INFOBLOX**vvvvvvvvvvvvvvvvvvvvvvv INFO {Style.RESET_ALL}")

    #Function of functions that will accomplish the API call, handling of response code,
    #and the restarting of the Infoblox service
    def ModifyHostRecord(ipaddress, mac="", fqdn="", comment="default", conn=conn, operation="create", dnsview="InternalView"):
        #function to provide terminal output depending on the success of the API call
        def HandleStatusCodes(response, successfulmessage="Successful operation", printout=True, exitonerror=True):
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
                    print(f"{Back.MAGENTA}{statuscode}{Style.RESET_ALL}: Unsuccessful operation. Stopping script.")
                    print(Back.MAGENTA+json.loads(response.text).get("text"))
                    exit()
                elif exitonerror is False:
                    print(f"{Back.MAGENTA}{statuscode}{Style.RESET_ALL}: Unsuccessful operation. Suppressing error.")
                    print(Fore.MAGENTA+json.loads(response.text).get("text"))
                print("============================")

        #function to make a POST call and restart Infoblox services for changes to take effect
        def RestartServices(ip=infoblox_ip, wapi_version=infoblox_wapi_version, username=infoblox_username, password=infoblox_password):
            auth = HTTPBasicAuth(username, password)
            #define headers which define the type of data to expect and send
            accept_header = "application/yang-data+json"
            content_type_header = "application/json"
            #create headers Dictionary, used to construct the URL
            headers = {
                "Accept": accept_header,
                "Content-Type": content_type_header
            }
            base = f"https://{ip}/wapi/v{wapi_version}/"
            #===================================
            #Get the Grid ID from Infoblox
            #===================================
            #construct the base URL to access the Infoblox Grid reference
            #the Grid reference is a set of characters unique to an Infoblox instance
            url = f"{base}grid"

            #attempt to connect to the target with a GET request using pre-defined
            #connection variables and the URL to get the Grid ID
            try:
                response = requests.get(url, headers=headers, auth=auth, verify=False)
            #If a RESTCONF connection (i.e. HTTPS connection to the device can't be created) fails,
            #catch the exception, print out status, and stop script
            except requests.exceptions.ConnectionError:
                print(f"\n{Fore.RED}ConnectionError:")
                print(f"Unable to establish a RESTCONF / HTTPS connection with {Fore.YELLOW}{host}{Style.RESET_ALL}.")
                exit()
            #===================================
            #Attempt to restart DHCP/DNS services
            #===================================
            #If a RESTCONF connection (i.e. HTTPS connection to the device can't be created) returns a 404,
            #catch the exception, print out status, and stop script        
            if response.status_code == 200:
                #convert the response to JSON
                reply = json.loads(response.text)
                #parse out the grid_id from the response
                #the response is initially a List (with one index), which returns a dictionary
                #get the value of the "_ref" key, which returns a string
                #the string is separated by a "/" and the second value is the actual grid_id
                grid_id = list(reply)[0].get("_ref").split("/")[1]
                #construct the URL with the function needed to restart DNS/DHCP services
                url = f"{base}grid/{grid_id}/?_function=restartservices"
                #construct the payload Python Dictionary that will become a JSON string in the request
                payload = {
                    "member_order" : "SIMULTANEOUSLY", 
                    "service_option": "ALL"        
                }
                #try sending the POST request with the payload
                try:
                    response = requests.post(url, headers=headers, auth=auth, json = payload, verify=False)
                #If a RESTCONF connection (i.e. HTTPS connection to the device can't be created) fails,
                #catch the exception, print out status, and stop script
                except requests.exceptions.ConnectionError:
                    print(f"\n{Fore.RED}ConnectionError:")
                    print(f"Unable to establish a RESTCONF / HTTPS connection with {Fore.YELLOW}{host}{Style.RESET_ALL}.")
                    exit()
                #call on HandleStatusCodes to display certain terminal messages based on the status code
                #pass in the status code and the message to display when a 200 is received
                HandleStatusCodes(response, "DHCP/DNS Services successfully restarted.", printout=False)
            else:
                print(f"{Back.MAGENTA}{statuscode}{Style.RESET_ALL}: Failed operation. Stopping script.")
                print(response.text)
                exit()
 
 
        #construct the InfobloxObjectManager, used for particular tasks
        ibom = InfobloxObjectManager(conn)
        #define base URL, concatenate different URIs to it later
        base = f"https://{infoblox_ip}/wapi/v{infoblox_wapi_version}/"
        #define authentication
        auth = HTTPBasicAuth(infoblox_username, infoblox_password)
        #define headers which define the type of data to expect and send
        accept_header = "application/yang-data+json"
        content_type_header = "application/json"
        #create headers Dictionary, used to construct the URL
        headers = {
            "Accept": accept_header,
            "Content-Type": content_type_header
        }

        #addressesList is a list that is populated with the MAC address and 
        #IP address(es) thatwould be used to create the hostrecord
        #addressesList will be passed into the request's payload
        addressesList = []
        #strip off any leading whitespaces
        mac = mac.strip()
        ipaddress = ipaddress.strip()
        addressesList.append(
            {"ipv4addr":ipaddress,
            "mac":mac}
        )
        if operation.upper() == "CREATE":
            #print out status to terminal
            print(f"\nAttempting to create the Host record for {Fore.YELLOW+fqdn+Style.RESET_ALL} with below payload...")
            print(addressesList)
            #construct URL for modifying Host records
            url = f"{base}record:host"   
            #define payload to create the Host record
            payload = {
                "name":fqdn,
                "ipv4addrs":addressesList,
                "restart_if_needed":True,
                "view":dnsview,
                "comment": comment
            }
            print(url)
            #try sending the POST request with the payload
            try:
                response = requests.post(url, headers=headers, auth=auth, json = payload, verify=False)
            #If a RESTCONF connection (i.e. HTTPS connection to the device can't be created) fails,
            #catch the exception, print out status, and stop script
            except requests.exceptions.ConnectionError:
                print(f"\n{Fore.RED}ConnectionError:")
                print(f"Unable to establish a RESTCONF / HTTPS connection with {Fore.YELLOW}{host}{Style.RESET_ALL}.")
                exit()
            HandleStatusCodes(response, successfulmessage="Created Host Record.",exitonerror=False,printout=False)
            #Infoblox DHCP/DNS services need to be restarted for changes to apply
            RestartServices()
     
    ModifyHostRecord(
        ipaddress=newdevice_ip,
        mac = newdevice_mac,
        fqdn=newdevice_fqdn,
        comment=infoblox_comment,
        operation="create" 
    )
   

#run all modules together
if __name__ == "__main__":
    AddToOxidized(newdevice_ip, newdevice_os, newdevice_devicename, newdevice_domain_name)
    AddToDNAC(newdevice_ip)
    AddToISE(newdevice_devicename, newdevice_ip)
    AddToInfoblox(newdevice_ip, newdevice_mac, newdevice_fqdn)    



    
