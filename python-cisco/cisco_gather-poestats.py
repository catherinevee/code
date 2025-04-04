from napalm import get_network_driver
from netmiko import ConnectHandler
import paramiko
import smtplib
import os
import time
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import datetime
from napalm.base.exceptions import ConnectionException, MergeConfigException
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
import os.path
import os
import tkinter as tk
from tkinter import filedialog
import time
import re
import colorama
from colorama import Fore, Style, init, Back
# colorama needs to initialize for colored text to show in Windows
# after a colored text line appears, auto-reset to plain (white) text
# these colors add additional characters to the string, so the color values are concatenated
# into the string
init(autoreset=True)
colorama.init()
import os
import glob
import pandas as pd

def SendHTMLEmail():
    sender = "wwusystms@gmail.com"
    #recipients is a List filled with email addresses as strings
    msg = MIMEMultipart('alternative')
    msg['Subject'] = " PoE Util. Report - "+time.strftime("%Y-%m-%d", time.localtime())+""
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    # Create the body of the message (a plain-text and an HTML version).
    html = """\
    <html>
    <u> Automated PoE Utilization Report </u> <br>
    """
    html += "Script Start Time:<b>"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"</b><br>"
    html += "Displaying devices with the <b> 5 </b> highest utilization percentages:<br>"
    html += "<br>"
    #at the end of script, display the data
    #sort by the fourth element, the percentused variable
    print("Displaying device data for devices with 5 highest PoE util. percentages:")
    for device in sorted(Device_InlinePower_List, key=takeFourth,reverse=True)[:5]:
        hostname = device.split(",")[0].strip()
        model = device.split(",")[1].strip()
        available = device.split(",")[2].strip()
        used = device.split(",")[3].strip()
        percentused = device.split(",")[4].strip()
        #also append data to "html" variable, use to create HTML email
        html += "<b>"+hostname +"</b> (<i>"+model+"</i>) PoE Utilization: <b>"+str(percentused)+"%</b> used. (Available: <b>"+str(available)+"</b>, Used: <b>"+str(used)+"</b>)<br>"
        print(device.strip())
    print("\n")    
    html += "<br>====================================<br>"
    #print out the rest of the devices
    print("Displaying device data for other devices with lower PoE util. percentages:")
    for device in sorted(Device_InlinePower_List, key=takeFourth, reverse=True)[5:]:
        hostname = device.split(",")[0].strip()
        model = device.split(",")[1].strip()
        available = device.split(",")[2].strip()
        used = device.split(",")[3].strip()
        percentused = device.split(",")[4].strip()
        #also append data to html variable
        html += "<b>"+hostname +"</b> (<i>"+model+"</i>) PoE Utilization: <b>"+str(percentused)+"%</b> used. (Available: <b>"+str(available)+"</b>, Used: <b>"+str(used)+"</b>)<br>"
        print(device.strip())    

    #print out script results to terminal
    print("Preparing email body to send to recipients.")

    #begin construction of the HTML email
    # Record the MIME types of both parts - text/plain and text/html.
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part2)
    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    #html += """\
    #
    #</html>


    mail.login('@gmail.com', 'i42GRLdZbEDrYGq')
    mail.sendmail(sender, recipients, msg.as_string())
    mail.quit()

#function created to take fourth element of a "x,x,x,x" line
#used later to sort by this element
def takeFourth(elem):
    return int(elem.split(",")[4])


#define output file that will hold the script's results
outputfile_poeutil = 'Item_PoE_Utilization.csv'
outputfile_poeportcount = 'Item_PoE_PortCount.csv'
outputfile_nonpoeunusedportcount = 'Item_NonPoE_PortCount.csv'
outputfile_unreachable_devices = 'Item_unreachabledevices.csv'
outputfile_combineddata = "SwitchInventory.csv"

#list that holds retrieved data from devices
Device_InlinePower_List = []

Device_PoEPortCount_List = []

Device_NonPoEPortCount_List = []

Device_UnreachableDevices_List = []

def ReadFromIPAddressFile(IPAddressFile):
    with open(IPAddressFile, "r") as ReadFromFile:
        for line in ReadFromFile:
            line = line.strip()
            
            if "rsfd" in line: #skip 4500X
                continue
            elif "dfgd" in line: #skip 6509
                continue
            elif "dfgd" in line: #skip restek server switch
                continue
            elif "dfgfd" in line: #skip distribution switches
                continue
            line_onlyhostname = str(line).split(".")[0]
            line_lastthirdletter = list(line_onlyhostname)[-3]
            if line_lastthirdletter == "S":
                print(f"{Back.CYAN}S [Switch] {Style.RESET_ALL} -- {line}")
                fqdns.append(f"{line.strip()}")

            
def WriteToFile(outputfile, data):
    print(f"            Appending to output file {outputfile}...")
    with open(outputfile, "a") as WriteToFile:
         for line in data:
            WriteToFile.write(line+"\n")


def SSHConnection(device_fqdn):
        adminusername = "fdgdf"
        adminpassword = "smesdfdsfrdyashchaya!"
        print(f"\nConnecting to {Back.CYAN+device_fqdn+Style.RESET_ALL}...")        
        net_connect = {
            'device_type': 'cisco_ios',
                'host': device_fqdn,
                'username': adminusername,
                'password': adminpassword,
                'port': 22,        
        }
        return net_connect


def GetPortCount(hostname, ssh):
    poe_portcount_used = 0
    poe_portcount_unused = 0
    print("             -----------------------------------------------------------")
    print(f"            Calculating the count of PoE-capable ports...")
    showpowerinlinecmd = ssh.send_command('show power inline | b -')
    for line in showpowerinlinecmd.splitlines():
        if "/" in line:
            if "off" in line:
                # print(f"{Fore.RED}PoE Off{Style.RESET_ALL}: {line}")
                poe_portcount_unused += 1
            elif "on" in line:
                # print(f"{Fore.GREEN}PoE On{Style.RESET_ALL}: {line}")
                poe_portcount_used += 1
    poe_portcount_total = poe_portcount_unused + poe_portcount_used
    print(f"            Calculating device model...")
    showvercmd_9k = ssh.send_command('show ver | i Model Number')
    if len(showvercmd_9k) == 0:
        print(f"                Model type: {Back.CYAN}Legacy{Style.RESET_ALL}")    
        showvercmd_legacy = ssh.send_command('show ver | i cisco WS-')
        legacymodel = showvercmd_legacy.split()[1]
        # print(f"            {Fore.YELLOW+legacymodel+Style.RESET_ALL}")
        Device_PoEPortCount_List.append(""+hostname+","+legacymodel+","+str(poe_portcount_total)+","+str(poe_portcount_used)+","+str(poe_portcount_unused))
    elif len(showvercmd_9k) > 0:
        print(f"                Model type: {Back.CYAN}9000 Series{Style.RESET_ALL}")    
        # print(f"            {Fore.YELLOW+showvercmd_9k+Style.RESET_ALL}")
        ninekmodel = showvercmd_9k.strip().split()[3]       
        Device_PoEPortCount_List.append(""+hostname+","+ninekmodel+","+str(poe_portcount_total)+","+str(poe_portcount_used)+","+str(poe_portcount_unused)+"")
        
    print(f"                  Down, PoE ports: {poe_portcount_unused}")
    print(f"                  Active, PoE ports: {poe_portcount_used}")
    print(f"                  Total PoE ports available: {poe_portcount_total}")
    return Device_PoEPortCount_List


def CalculatePoEUtilization(hostname, ssh):
    print("             -----------------------------------------------------------")
    print(f"            Calculating PoE utilization...")
    showvercmd_9k = ssh.send_command('show ver | i Model Number')
    if len(showvercmd_9k) == 0:
        showvercmd_legacy = ssh.send_command('show ver | i cisco WS-')
        legacymodel = showvercmd_legacy.split()[1]
        if '2960' in legacymodel:
            powerregex = r'\d\s+(\d+\.\d)\s+(\d+\.\d)\s+(\d+\.\d)'
        elif '3750' in legacymodel:
            powerregex = r'\d\s+(n\/a|\d+\.\d)\s+(n\/a|\d+\.\d)\s+(n\/a|\d+\.\d)'
        elif '3650' in legacymodel:
            powerregex = r'\d\s+(\d+\.\d)\s+(\d+\.\d)\s+(\d+\.\d)'
        else:
            powerregex = r'Available:(\d+\.\d|\d+)\(w\)\s+Used:(\d+\.\d|\d+)\(w\)\s+Remaining:(\d+\.\d|\d+)'
        showpowerinlinecmd = ssh.send_command('show power inline')
        powerregex_matches = re.search(powerregex, showpowerinlinecmd)
        #parse out the data from command output, organize into three values
        try:
            available = powerregex_matches.group(1)
            used = powerregex_matches.group(2)
            remaining = powerregex_matches.group(3)
        except AttributeError:
            print(f"Unable to get complete PoE data for {hostname}")
            return
        try:
            percentused = float(remaining)/float(available)
            percentused = str(percentused).split(".")[1][:2]
        except ZeroDivisionError:
            percentused = "0"
        showpowerinlinecmd = ssh.send_command('show power inline | i Available')            
        print(f"                Actual PoE values: {showpowerinlinecmd}")
        print(f"                Calculated Values: {Back.CYAN+available+Style.RESET_ALL}, {Back.CYAN+used+Style.RESET_ALL}, {Back.CYAN+remaining+Style.RESET_ALL}")
        print(f"                Percentage Free: {Back.CYAN+percentused+Style.RESET_ALL}%")
        Device_InlinePower_List.append(""+hostname+","+legacymodel+","+str(available)+","+str(used)+","+str(percentused))
        
    elif len(showvercmd_9k) > 0:
        if '9300' in showvercmd_9k:
            powerregex = r'\d\s+(\d+\.\d)\s+(\d+\.\d)\s+(\d+\.\d)'
        else:
            powerregex = r'Available:(\d+\.\d|\d+)\(w\)\s+Used:(\d+\.\d|\d+)\(w\)\s+Remaining:(\d+\.\d|\d+)'
        ninekmodel = showvercmd_9k.strip().split()[3]
        showpowerinlinecmd = ssh.send_command('show power inline')
        powerregex_matches = re.search(powerregex, showpowerinlinecmd)
        #parse out the data from command output, organize into three values
        try:
            available = powerregex_matches.group(1).split(".")[0]
            used = powerregex_matches.group(2).split(".")[0]
            remaining = powerregex_matches.group(3).split(".")[0]
        except AttributeError:
            print(f"Unable to get complete PoE data for {hostname}")
            return
        try:
            percentused = float(remaining)/float(available)
            percentused = str(percentused).split(".")[1][:2]
        except ZeroDivisionError:
            percentused = "0"

        showpowerinlinecmd = ssh.send_command('show power inline | i Available')            
        print(f"                Actual PoE values: {showpowerinlinecmd}")
        print(f"                Calculated Values: {Back.CYAN+available+Style.RESET_ALL}, {Back.CYAN+used+Style.RESET_ALL}, {Back.CYAN+remaining+Style.RESET_ALL}")
        print(f"                Percentage Free: {Back.CYAN+percentused+Style.RESET_ALL}%")
        Device_InlinePower_List.append(""+hostname+","+ninekmodel+","+str(available)+","+str(used)+","+str(percentused)+"")
    return Device_InlinePower_List



def CalculateDeviceModel_LegacyDevices(ssh):
    showvercmd = ssh.send_command('show ver | i cisco WS-')
    for line in showvercmd.splitlines():
        if "cisco" in line:
            devicemodel = line.split()[1].strip()
    return devicemodel
    
def CalculateDeviceModel(hostname, ssh):    
    print("             -----------------------------------------------------------")
    print(f"            Calculating the device model...")
    showmodcmd = ssh.send_command('show mod | i Chassis Type')
    if len(showmodcmd) == 0:
        showvercmd = ssh.send_command('show ver | i cisco C')
        for line in showvercmd.splitlines():
            if "cisco" in line:
                devicemodel = line.split()[1].strip()        
                break        
    for line in showmodcmd.splitlines():
        if "Invalid input" in line:
            devicemodel = CalculateDeviceModel_LegacyDevices(ssh)
            break
        elif len(line) == 0:
            showvercmd = ssh.send_command('show ver | i cisco C')
            for line in showvercmd.splitlines():
                if "cisco" in line:
                    devicemodel = line.split()[1].strip()        
                    break
        elif "Chassis Type" in line:
            devicemodel = line.split(":")[1].strip()
            break
    # print(f"{       Fore.YELLOW+hostname+Style.RESET_ALL} is a {Fore.YELLOW+devicemodel+Style.RESET_ALL}")
    return devicemodel


def CalculateUnusedPorts(hostname, ssh):
    nonpoeblade_List = []
    port_up_count = 0
    port_down_count = 0
    port_admindown_count = 0
    regex_modulenumber = r'^\s(\d)'
    print(f"            Calculating the count of unused, non-PoE ports...")
    showmodcmd = ssh.send_command('show mod | ex POE|to')
    devicemodel = CalculateDeviceModel(hostname, ssh)
    if "Invalid input" in showmodcmd:
        nonpoeblade_List.append("0")
    else:    
        for line in showmodcmd.splitlines():
            regex_modulenumber_match = re.search(regex_modulenumber, line)
            if regex_modulenumber_match is not None:
                non_poe_blade = regex_modulenumber_match.group(0).strip()
                if "9300" in devicemodel:
                    print(f"                {Back.CYAN+line.strip()+Style.RESET_ALL}")
                    print(f"                {Fore.GREEN}[{non_poe_blade}]{Style.RESET_ALL}PoE blade detected. Not added to port count.")
                elif "Sup" in devicemodel:
                    print(f"                {Back.CYAN+line.strip()+Style.RESET_ALL}")
                    print(f"                {Fore.GREEN}[{non_poe_blade}]{Style.RESET_ALL}Supervisor blade detected. Not added to port count.")            
                else:
                    nonpoeblade_List.append(non_poe_blade)            
                    print(f"                {Back.CYAN+line.strip()+Style.RESET_ALL}")
                    print(f"                {Fore.RED}[{non_poe_blade}]{Style.RESET_ALL}Non-PoE blade detected")

    for blade in nonpoeblade_List:
        showinterfacecmd = ssh.send_command(f"show ip int brief | i {blade}/")
        for cmd_output in showinterfacecmd.splitlines():
            if "/" not in cmd_output:
                continue
                
            port = cmd_output.split()[0]
            linkstatus = cmd_output.split()[-1]
            if "administratively" in cmd_output:
                # print(f"{port} {linkstatus} is {Fore.RED}admin down{Style.RESET_ALL}")            
                port_admindown_count += 1
            elif linkstatus == "up":
                # print(f"{port} {linkstatus} is {Fore.GREEN}up{Style.RESET_ALL}")
                port_up_count += 1
            elif linkstatus == "down":
                # print(f"{port} {linkstatus} is {Fore.RED}down{Style.RESET_ALL}")
                port_down_count += 1
             
    print(f"                Active, non-PoE port count: {port_up_count}")
    print(f"                Down, non-PoE port count: {port_down_count}")
    print(f"                Admin Down, non-PoE port count: {port_admindown_count}")
    Device_NonPoEPortCount_List.append(f"{hostname},{devicemodel},{port_up_count},{port_down_count},{port_admindown_count}")
    return Device_NonPoEPortCount_List




def CombineThreeFilesIntoOne():
    extension = 'csv'
    all_filenames = [i for i in glob.glob('Item_*.{}'.format(extension))]    
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #export to csv
    combined_csv.to_csv(outputfile_combineddata, index=False, encoding='utf-8-sig')


if __name__ == "__main__":
    fqdns = [
    ]
    ReadFromIPAddressFile("dnac_nd_onlynames.txt")





    #iterate through each ip in ips List
    for hostname in fqdns:
        with open(outputfile_poeutil, "w") as WriteHeaderToFile:
            WriteHeaderToFile.write("Hostname,Model,PoE_Available(W),PoE_Used(W),PoE_Unused(%)\n")
        with open(outputfile_poeportcount, "w") as WriteHeaderToFile:
            WriteHeaderToFile.write("Hostname,Model,PoE_PortsTotal,PoE_PortsUsed,PoE_PortsUnused\n")
        with open(outputfile_nonpoeunusedportcount, "w") as WriteHeaderToFile:
            WriteHeaderToFile.write("Hostname,Model,NonPoE_UpPorts,NonPoE_DownPorts,NonPoE_AdminDownPorts\n")
        with open(outputfile_unreachable_devices, "w") as WriteHeaderToFile:
            WriteHeaderToFile.write("Hostname,Status\n")

        net_connect = SSHConnection(hostname)
        try:
            ssh = ConnectHandler(**net_connect)
        except Exception as e:
            print(f"NetmikoTimeoutException to {hostname} raised, retrying login...")
            try:
                ssh = ConnectHandler(**net_connect)
            except Exception as e:
                print(f"NetmikoTimeoutException to {hostname} raised, skipping device.")
                Device_UnreachableDevices_List.append(f"{hostname},unreachable")                
                continue
        poedata = CalculatePoEUtilization(hostname, ssh)
        WriteToFile(outputfile_poeutil, poedata)
        
        portcountdata = GetPortCount(hostname, ssh)
        WriteToFile(outputfile_poeportcount, portcountdata)
        
        nonpoeportcountdata = CalculateUnusedPorts(hostname, ssh)
        WriteToFile(outputfile_nonpoeunusedportcount, nonpoeportcountdata)
        WriteToFile(outputfile_unreachable_devices, Device_UnreachableDevices_List)
        
        
    CombineThreeFilesIntoOne()    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    