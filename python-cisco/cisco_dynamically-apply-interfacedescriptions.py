def Playbook_UpdateInterfaceDescriptionForCDPNeighbor(devices):
    #cmdslist will have the Cisco IOS commands in it
    cmdslist = []


    #create the strings to turn them into Cisco IOS commands 
    #and return a list that gets sent to the device
    def Worker_ConstructInterfaceDescriptionCmds(task, localport, neighborport, neighborname):
        print(f"On {Fore.YELLOW+localport+Style.RESET_ALL}, connected to port {Fore.YELLOW+neighborport+Style.RESET_ALL} of {Fore.YELLOW+neighborname+Style.RESET_ALL}")    
        interfacecmd = f"interface {localport}"
        descriptioncmd = f"description To {neighborname} {neighborport}"
        cmdslist.append(interfacecmd)
        cmdslist.append(descriptioncmd)
        return cmdslist


    #send the commands using Netmiko, save the config with Netmiko
    def Worker_SendInterfaceDescriptionCmds(task, cmdslist):
        result = task.run(
            task=netmiko_send_config,
            config_commands=cmdslist,
            )        
        print_result(result)
        result = task.run(
            task=netmiko_save_config,
            )
        print_result(result)


    #parse out the output of a "show cdp neighbor" 
    #and truncate the interface descriptions to their global configuration
    #shortcuts ("tw", "gi", "fa", "hu")
    def Worker_ParseOutCDPNeighborOutput(task, cdpneighboroutput):
        print(f"\nvvvv CDP NEIGHBOR SEARCH: {Back.CYAN+str(task.host).split('.')[0]+Style.RESET_ALL}** vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
        print(f"has these CDP neighbors:")
        for line in cdpneighboroutput.splitlines():
            if "Device ID" in line:
                neighborname = str(line.split()[2]).split('.')[0]
            if "Port ID" in line:
                neighborport = line.split()[6]
                if "HundredGigE" in neighborport:
                    neighborport = neighborport.replace('HundredGigE', line.split()[6][:2])                
                elif "TwentyFiveGigE" in neighborport:
                    neighborport = neighborport.replace('TwentyFiveGigE', line.split()[6][:2])
                
                elif "TenGigabitEthernet" in neighborport:
                    neighborport = neighborport.replace('TenGigabitEthernet', line.split()[6][:2])
                elif "GigabitEthernet" in neighborport:
                    neighborport = neighborport.replace('GigabitEthernet', line.split()[6][:2])
                elif "FastEthernet" in neighborport:
                    neighborport = neighborport.replace('FastEthernet', line.split()[6][:2])
                
                localport = line.split()[1][:-1]

                cmdslist = Worker_ConstructInterfaceDescriptionCmds(task, localport, neighborport, neighborname)
        print(cmdslist)
        Worker_SendInterfaceDescriptionCmds(task,cmdslist)        
        cmdslist.clear()

        
    def Worker_UpdateInterfaceDescriptionForCDPNeighbor(task):
        cdpneighboroutput = task.run(
            task=netmiko_send_command,
            command_string="show cdp neighbor detail | i Device ID|Interface",
        )
        cdpneighboroutput = Play_SendCommand_ParseOutput(cdpneighboroutput)
        
        Worker_ParseOutCDPNeighborOutput(task, cdpneighboroutput)
    
        
    result = devices.run(
            task=Worker_UpdateInterfaceDescriptionForCDPNeighbor,
        )

