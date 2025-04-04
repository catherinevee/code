def Playbook_SendIOSCommand(devices, commands):
    #for each device, run this
    try:
        result = devices.run(
            task=Play_SendCommand,
            commands = commands,
        )
        print_result(result)
        return result
    #this is to catch any devices that we can't authenticate into
    except NornirExecutionError as e:
        print("\n")
        print(f"{Back.MAGENTA}vvvv NORNIR SSH CONNECTION FAILURE**vvvvvvvvvvvvvvvvvvvvvvv VERIFY {Style.RESET_ALL}")
        print(e)

def NornirCreateConnection(device_or_group1, group2="null"):
    devicename_match = re.search(devicename_regex, device_or_group1)
    
    if bool(devicename_match) is True:
        if len(device_or_group1) >= 3:
            if device_or_group1[-3] == "A":
                device_or_group1 = str(device_or_group1)
                initialize_result = NornirInitializeWithLocalCredentials()
                nr = initialize_result[0]
                username = initialize_result[1]
                password = initialize_result[2] 
                print(username)
            else:   
                initialize_result = NornirInitialize()
                nr = initialize_result[0]
                username = initialize_result[1]
                password = initialize_result[2]             
                device_or_group1 = str(device_or_group1) + ".net"
            checkinventory_result = NornirCheckInventory(nr, device_or_group1)
            selectedhost = checkinventory_result[0]
            selecteddevice = checkinventory_result[1]   
        
        return selectedhost, selecteddevice
    elif group2=="null":
        initialize_result = NornirInitialize()
        nr = initialize_result[0]    
        print(f"\nvvvv FILTER INVENTORY BY ONE GROUP **vvvvvvvvvvvvvvvvvvvvvvv INFO")
        if len(device_or_group1) <=2:
            device_or_group1 = device_or_group1.upper()
        devices = nr.filter(F(groups__contains=device_or_group1))
        selectedinventory = devices.inventory.hosts.keys()
        if len(selectedinventory) == 0:
            print(f"[{Fore.YELLOW}NOTOK{Style.RESET_ALL}] {Fore.YELLOW+device_or_group1+Style.RESET_ALL+Style.RESET_ALL} 0 matches found.")
            exit()
        print(f"[{Fore.GREEN}OK{Style.RESET_ALL}] Found devices in inventory:") 
        for device in selectedinventory:
            print(Fore.YELLOW + device + Style.RESET_ALL)     
        return devices, selectedinventory
    else: 
        print(f"\nvvvv FILTER INVENTORY BY TWO GROUPS **vvvvvvvvvvvvvvvvvvvvvvv INFO")
        initialize_result = NornirInitialize()
        nr = initialize_result[0]
        username = initialize_result[1]
        password = initialize_result[2]  
        
        if len(device_or_group1) <=2:
            device_or_group1 = device_or_group1.upper()
        devices = nr.filter(F(groups__contains=device_or_group1) &
                            F(groups__contains=group2))
        selectedinventory = devices.inventory.hosts.keys()        
        if len(selectedinventory) == 0:
            print(f"[{Fore.YELLOW}NOTOK{Style.RESET_ALL}] {Fore.YELLOW+device_or_group1+Style.RESET_ALL+Style.RESET_ALL} 0 matches for {device_or_group1} nor {group2}")        
            exit()
        print(f"[{Fore.GREEN}OK{Style.RESET_ALL}] Found devices in inventory:") 
        for device in selectedinventory:
            print(Fore.YELLOW + device + Style.RESET_ALL)   
        return devices, selectedinventory
 
 