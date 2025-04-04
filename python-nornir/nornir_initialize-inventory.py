def NornirCheckInventory(nr, devicename):
    print(f"\nvvvv NORNIR INVENTORY CHECK**vvvvvvvvvvvvvvvvvvvvvvv INFO")
    # counter variables defined here to a quick inventory check of groups.yaml
    # and hosts.yaml
    hostcount = 0
    groupcount = 0
    # retrieve hosts and groups from Nornir object
    hosts = nr.inventory.hosts
    groups = nr.inventory.groups
    # for every host and group, increment their respective counters
    for key in hosts:
        hostcount += 1
    for key in groups:
        groupcount += 1
    # print out how many hosts and groups there are
    hostcount = str(hostcount)
    groupcount = str(groupcount)
    if hostcount == 0:
        print("---------------------------------------------------------------")    
        print(f"{Fore.YELLOW}notok: 0 hosts in the hosts.yaml file. Stopping.") 
        #if there are 0 hosts in the hosts file, exit
        exit()
    elif groupcount == 0:
        print("---------------------------------------------------------------")    
        print(f"{Fore.YELLOW}notok: 0 groups in the groups.yaml file. Stopping.") 
        #if there are 0 hosts in the hosts file, exit
        exit()    
    print(f"[{Fore.GREEN}OK{Style.RESET_ALL}] {Fore.YELLOW+hostcount+Style.RESET_ALL+Style.RESET_ALL} devices in inventory found")
    print(f"[{Fore.GREEN}OK{Style.RESET_ALL}] {Fore.YELLOW+groupcount+Style.RESET_ALL+Style.RESET_ALL} device groups found")
        
    # filter out devices (from the hosts.yaml), using the devicename parameter
    selectedhost = nr.filter(name=devicename)
    selecteddevice = selectedhost.inventory.hosts.keys()
    # print out results to terminal, stop script if there aren't any results
    if len(selecteddevice) == 0:
        print("---------------------------------------------------------------")
        print(f"[{Fore.YELLOW}NOTOK{Style.RESET_ALL}] {Fore.YELLOW+devicename+Style.RESET_ALL+Style.RESET_ALL} device not found")
        exit()
    # print out confirmation to terminal
    for device in selecteddevice:
        print(f"[{Fore.GREEN}OK{Style.RESET_ALL}] {Fore.YELLOW+device+Style.RESET_ALL+Style.RESET_ALL} device found in inventory")
    # return different values used in other functions
    print("\n")
    return [selectedhost, selecteddevice]



    
def NornirInitialize(): 
    print(f"\nvvvv INITIALIZING NORNIR **vvvvvvvvvvvvvvvvvvvvvvv INFO")
    # try to initialize Nornir, point towards a config YAML file
    try:
        nr = InitNornir(
            config_file=nornir_backupdefaults_file_location,
            logging={
                "enabled": True,
                "log_file": nornir_log_file_location,
                "level": "DEBUG"                
                },
            runner={"plugin": "threaded", "options": {"num_workers": 1}},    
            core={"raise_on_error": True}
            )
    except FileNotFoundError as e:
        print("---------------------------------------------------------------")    
        print(f"{Fore.YELLOW}notok:") #if the yaml file isn't found
        print(e)
        exit()
    # except KeyError as e:
        # print("---------------------------------------------------------------")    
        # print(f"{Fore.YELLOW}notok:") #usually a syntax error in the yaml file
        # print(str(e))
        # exit()
    print(f"[{Fore.GREEN}OK{Style.RESET_ALL}] config.yaml found")
    result = DeconstructNornirConfigurationFile(nr, nornir_config_file_location, nornir_backupdefaults_file_location) 
    nr = result[0]
    username = result[1]
    password = result[2]     
    return nr, username, password



def DeconstructNornirConfigurationFile(nr,nornir_config_file_location,nornir_defaults_file_location):
   # open the config.yaml YAML file, print out locations of parameters
    with open(nornir_config_file_location, "r") as file:
        documents = yaml.full_load(file)

        groupfile = documents.get("inventory").get("options").get("group_file")
        hostfile = documents.get("inventory").get("options").get("host_file")
        defaultsfile = documents.get("inventory").get(
            "options").get("defaults_file")
        print(f"[{Fore.GREEN}OK{Style.RESET_ALL}] {groupfile} found")
        print(f"[{Fore.GREEN}OK{Style.RESET_ALL}] {hostfile} found")
        print(f"[{Fore.GREEN}OK{Style.RESET_ALL}] {defaultsfile} found")
    # open the defaults.yaml YAML file, assign username and password variables
    # assign username and password parameters from file
    with open(nornir_defaults_file_location, "r") as file:
        documents = yaml.full_load(file)
        username = documents.get("username")
        password = documents.get("password")
    return nr, username, password
