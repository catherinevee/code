import re
from ciscoconfparse import CiscoConfParse
from jinja2 import *
import requests.packages.urllib3
import colorama
from colorama import Fore, Style, init, Back
# colorama needs to initialize for colored text to show in Windows
# after a colored text line appears, auto-reset to plain (white) text
# these colors add additional characters to the string, so the color values are concatenated
# into the string
init(autoreset=True)
colorama.init()
"""
---access-layer upgrades (GOOD)
4500_ALLSUP_to_9407_25GUPLINKS.txt
tested on:
    4506 + 6LE
    4506 + 7LE
    4506 + 8LE


---access-layer upgrades (GOOD)
3560G_to_9407_10GUPLINKS.txt
tested on:
    3560G
    3560X (sdfdsfs is a special-case, but still works)

-----distribution-layer upgrades (GOOD)
356012D_to_9500_25GUPLINKS.txt
tested on:
    3560E-12D

-----distribution-layer upgrades (GOOD)
4500X_to_9500_25GUPLINKS.txt
tested on:
    4500X-16

-----distribution-layer upgrades (GOOD)
GENERIC_9500_25GUPLINKS.txt
tested on:
    3750X

*not many interface changes, highly dependent on future changes to topology/purchased devices

"""
# define directory of jinja templates and the jinja template to use in
# this script
jinja_directory = "./jinja/"
jinja_template = "4500_ALLSUP_to_9407_25GUPLINKS.txt"
# load jinja directory and template
environment = Environment(loader=FileSystemLoader(jinja_directory))
template = environment.get_template(jinja_template)
# call SelectConfigFileDirectory function
result = SelectConfigFileDirectory()
# return the selected directory and the files in the directory (with an
# absolute path)
files_in_directory = result[0]
directory = result[1]

# sections will be ran against the find_all_children method
# these sections will have children
sections = [
    # begin covering Layer 3 configuration
    "access-list",
    "router eigrp",
    "ip",
    # begin covering Layer 2 configuration
    "vlan",
    "spanning-tree",
    # begin covering AAA/authentication configuration
    "aaa",
    "tacacs",
    "username",
    "line",
    # begin covering global configurations
    "archive",
    "logging",
    "ntp",
    "snmp-server",
    "banner motd",
    "no ip http",
    "hostname"
]

# interfacesList is a List that will be populated with dictionaries containing
# interface information
# interfacesList will be cleared after each file iteration
interfacesList = []
# iterate through the files in the files_in_directory variable
for file in files_in_directory:
    # define CiscoConfParse function, passing in the file
    parse = CiscoConfParse(file, factory=True)
    # generate output file name, concatenate in the directory and the filename
    # (with a modification)
    outputfile = directory + "/m_" + file.split("/")[-1]
    # open the output file with a blank string, to clear out the file of any
    # contents
    with open(outputfile, "w") as f:
        f.write("")
    with open(outputfile, "a") as f:
        f.write("\n!===========================================================\n")
        f.write(
            "!====================STARTING KEYWORD: INTERFACE====================\n")
        f.write("!===========================================================\n")
    # run a CiscoConfParse find_all_children method on the section
    # use CiscoConfParse's find_objects function to find all the interfaces
    interfacelookup = parse.find_objects("^interface")
    # iterate through each interface found, parse out interface configurations
    for interface in interfacelookup:
        # get string from CiscoConfParse object
        interface = interface.text
        print(interface)
        # define defaults here
        # have default state of an interface be Layer 2
        layer3 = False
        # some interface commands have blank strings for defaults
        cdpstatus = "cdp enable"
        shutdownstatus = "no shutdown"
        description = ""
        switchportmode = ""
        switchportvlan = ""
        switchportvoicevlan = ""
        trunkencapsulation = ""
        trunknative = ""
        ipaddresses = []
        pim_mode = ""
        igmp_version = ""
        portchannel = ""
        svl = ""
        speed = ""
        ipdhcpsnooping = ""
        vrf = ""
        portfast = ""
        eigrp_hello_interval = ""
        eigrp_hold_time = ""
        # an interface can have multiple objects of the same kind,
        # e.g. allowed vlans on a trunk, secondary/primary IP addresses, VIPs
        trunkallowedvlans = []
        access_groups = []
        standby_vips = []
        # for each interface, find all children
        interface_details = parse.find_all_children("^" + interface + "$")
        # go through the interface details and assign values to variables
        for detail in interface_details:
            # strip out whitespace
            detail = detail.strip()
            # ==========================
            # Identify any "unique" parameters like VRFs, access-groups, etc.
            if "no cdp enable" in detail:
                cdpstatus = detail
            if "ip access-group" in detail:
                access_groups.append(detail)
            if "ip vrf forwarding " in detail:
                vrf = detail
            # ==========================
            # Identify any port/interface descriptions
            if "description" in detail:
                description = detail

            # ==========================
            # Identify any static speed commands on interface
            if "speed" in detail:
                speed = detail

            # ==========================
            # Identify any interfaces that are in a portchannel
            if "channel-group" in detail:
                portchannel = detail

            # ==========================
            # Identify any interfaces in a SVL
            if "stackwise-virtual link" in detail:
                svl = detail

            # ==========================
            # Identify IP DHCP Snooping Trust
            if "ip dhcp snooping trust" in detail:
                ipdhcpsnooping = detail

            # ==========================
            # if the interface was shutdown previously
            if "shutdown" in detail:
                shutdownstatus = detail

            # ==========================
            # Identify any EIGRP interface-level parameters
            if "ip hello-interval" in detail:
                eigrp_hello_interval = detail
            if "ip hold-time" in detail:
                eigrp_hold_time = detail

            # ==========================
            # ignore any particular SVI configurations
            # used for VLAN 1, or other legacy SVIs
            if interface == "interface Vlan1":
                cdpstatus = ""
                continue
            elif interface == "interface Vlan999":
                continue
            elif interface == "interface Vlan2999":
                continue
            # ==========================
            # Identify any SVIs
            if "Vlan" in interface:
                layer3 = True

            # ==========================
            # Identify any interfaces (or SVIs) with an IP address
            # if an interface has an IP address, append to ipaddresses List
            # this is handy in parsing out secondary IP addresses on an
            # interface
            if "no ip address" in detail:
                ipaddresses.append(detail)
            elif "ip address" in detail:
                layer3 = True
                ipaddresses.append(detail)

            # ==========================
            # Identify any L2 ports, if it is access or trunk
            if "switchport mode trunk" in detail:
                switchportmode = detail
                trunkencapsulation = "switchport trunk encapsulation dot1q"
            elif "switchport mode access" in detail:
                switchportmode = detail
                portfast = "spanning-tree portfast"
            elif "no switchport" in detail:
                switchportmode = detail
            elif "switchport trunk native vlan" in detail:
                trunknative = detail
            # ==========================
            # Identify any pruned VLANs
            if "switchport trunk allowed vlan" in detail:
                trunkallowedvlans.append(detail)
            # ==========================
            # Identify any access VLANs, in case an access mode isn't defined
            if "switchport access vlan" in detail:
                switchportvlan = detail
                portfast = "spanning-tree portfast"
            # ==========================
            # Identify any voice VLANs on a port
            if "switchport voice vlan" in detail:
                switchportvoicevlan = detail

            # ==========================
            # Identify the VIP address in HSRP
            # this is used to verify that the VIP becomes the actual IP of the
            # SVI
            if "standby" in detail and "ip" in detail:
                standby_vips.append(detail)

            # ==========================
            # if the interface is Layer 3, add values for helper-addresses,
            # PIM, and IGMP
            if layer3:
                # ignore Port-channels, since they shouldn't have helpers
                if "Port-channel" in interface:
                    pass
                # ignore Loopbacks, since they shouldn't have helpers
                elif "Loopback" in interface:
                    pass
                else:
                    # iterate through each IP address that is in ipaddresses
                    # List
                    for ipaddress in ipaddresses:
                        # regex out the equipment SVI (10.x.101.x)
                        # it is Layer 3, but doesn't require any helpers or
                        # PIM/IGMP
                        equipment_svi_regex = r"10\.\d{0,3}\.101.\d{0,3}"
                        regexp = re.compile(equipment_svi_regex)
                        # if equipment SVI is found, don't add anything else,
                        # call it good
                        if regexp.search(ipaddress):
                            iphelper1 = ""
                            iphelper2 = ""
                            iphelper3 = ""
                        else:
                            # otherwise, if the interface is an SVI, add
                            # helpers
                            if "Vlan" in interface:
                                iphelper1 = "ip helper-address sdfds.dfs.245.135"
                                iphelper2 = "ip helper-address sdf.sdf.244.135"
                                iphelper3 = "ip helper-address sdf.sdfs.248.16"
                            else:
                                # if the interface is a Layer 3 switchport,
                                # don't add helpers
                                iphelper1 = ""
                                iphelper2 = ""
                                iphelper3 = ""
                            # for all Layer 3 interfaces, except for MGMT SVIs,
                            # add PIM and IGMP setting
                            pim_mode = "ip pim sparse-mode"
                            igmp_version = "ip igmp version 3"
            # ==========================
            # if the interface is Layer 2, don't add values for
            # helper-addresses, PIM, or IGMP
            elif not layer3:
                iphelper1 = ""
                iphelper2 = ""
                iphelper3 = ""
        # ==========================
        # add all variable data to a dictionary that contains the interface data
        # then append that dictionary to the interfacesList list
        interfacesList.append(
            {
                "interface": interface,
                "shutdown": shutdownstatus,
                "svl": svl,
                "cdp_status": cdpstatus,
                "description": description,
                "port_channel": portchannel,
                "speed": speed,
                "layer_3": layer3,
                "ip_address": ipaddresses,
                "ip_helper_1": iphelper1,
                "ip_helper_2": iphelper2,
                "ip_helper_3": iphelper3,
                "pim_mode": pim_mode,
                "igmp_version": igmp_version,
                "ip_dhcp_snooping": ipdhcpsnooping,
                "switchport_mode": switchportmode,
                "switchport_vlan": switchportvlan,
                "switchport_voice_vlan": switchportvoicevlan,
                "portfast": portfast,
                "trunk_encapsulation": trunkencapsulation,
                "trunk_native_vlan": trunknative,
                "trunk_allowed": trunkallowedvlans,
                "vrf": vrf,
                "access_groups": access_groups,
                "eigrp_hello_interval": eigrp_hello_interval,
                "eigrp_hold_time": eigrp_hold_time,
                "standby_vips": standby_vips
            }
        )

    # with all the interface_dict dicionaries appended to interfacesList,
    # iterate through them and apply them to the designated jinja template
    for interface_dict in interfacesList:
        print("\n=================================\n")
        # print(pprint(interface_dict))
        interface_template_output = template.render(interface=interface_dict)
        # print(interface_template_output)
        # write out template-d result to the outputfile
        with open(outputfile, "a") as f:
            f.write(interface_template_output + "\n!")
    # clear out the interfacesList
    interfacesList.clear()
    # iterate through the sections List, which contains regex-d strings
    # (r"^interface")
    for section in sections:
        # print out status to terminal, as a divider between segments
        print(
            "\n====================" +
            section.upper() +
            "====================\n")
        # write out the section to the file, with a divider between segments
        with open(outputfile, "a") as f:
            f.write(
                "\n!===========================================================\n")
            f.write("!====================STARTING KEYWORD: " +
                    section.upper() + "====================\n")
            f.write("!===========================================================\n")
        # run a CiscoConfParse find_all_children method on the section
        section_lookup = parse.find_all_children("^" + section)
        # generate the len() of the section_lookup variable, to detect any
        # empty matches
        number_of_children = len(section_lookup)
        # if a section doesn't have any children, print + write out to file that
        # no children were found and continue to next section
        if number_of_children == 0:
            print("NO_CHILDREN_FOUND")
            with open(outputfile, "a") as f:
                f.write("[[ NO_CHILDREN_FOUND OR RESULTS_WERE_FILTERED ]]")
            continue
        # iterate through each child in the section_lookup, certain sections
        # have children that need to be parsed out
        # if no children need to be parsed out, print out the child to the
        # output file
        for child in section_lookup:
            if section == "snmp-server":
                if "LMS-" in child:
                    print(Fore.RED + "REMOVED: " + Style.RESET_ALL, child)
                    continue
                elif "ReadUser" in child:
                    print(Fore.RED + "REMOVED: " + Style.RESET_ALL, child)
                    continue
                elif "FFFF" in child:
                    print(Fore.RED + "REMOVED: " + Style.RESET_ALL, child)
                    continue
            if section == "ip":
                if "QOS" in child:
                    print(Fore.RED + "REMOVED: " + Style.RESET_ALL, child)
                    continue
                elif "remark workstation source ports" in child:
                    print(Fore.RED + "REMOVED: " + Style.RESET_ALL, child)
                    continue
                elif "permit udp any range 50000 50019" in child:
                    print(Fore.RED + "REMOVED: " + Style.RESET_ALL, child)
                    continue
                elif "permit udp any range 50020 50059" in child:
                    print(Fore.RED + "REMOVED: " + Style.RESET_ALL, child)
                    continue
            print(child)
            with open(outputfile, "a") as f:
                f.write(child + "\n")
