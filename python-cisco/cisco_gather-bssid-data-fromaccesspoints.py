def Playbook_GetBSSIDValuesFromAccessPoints(filter="none"):

    outputfile = f"MakeChangesToAll9KAPs_{date.today()}.txt"


    def Play_GetCDPNeighborsAndBSSIDValues(listofaccesspoints):
        regex_to_parse_out_bssid_value = r"\s{1,3}([A-F0-9][A-F0-9][A-F0-9][A-F0-9]|[A-F0-9][A-F0-9][A-F0-9]|[A-F0-9][A-F0-9])\s{1,3}\d"
        listof_aps = listofaccesspoints
        showcmds = [
        "show controllers dot11Radio 0 | i DIS",
        "show controllers dot11Radio 1 | i DIS",
        "show controllers dot11Radio 2 | i DIS",
        ]
        showcdpcmd = "show cdp neighbors"
        
        data_bssid_cdpneighbors = []
        for ap_data in listof_aps:
            ap_hostname = str(ap_data.split(",")[0])
            ap_hostname = ap_hostname.split(".")[0]
            ap_baseradiomac = str(ap_data.split(",")[1])
            ap_location = str(ap_data.split(",")[2])        
            ap_ip = str(ap_data.split(",")[3])
            net_connect = Play_SSHConnectionToAP(ap_hostname,ap_ip)
            
            try:
                ssh = ConnectHandler(**net_connect)
            except NetmikoTimeoutException as e:
                print(f"NetmikoTimeoutException to {ap_hostname}/{ap_ip} raised, retrying login...")
                try:
                    ssh = ConnectHandler(**net_connect)
                except NetmikoTimeoutException as e:
                    print(f"NetmikoTimeoutException to {ap_hostname}/{ap_ip} raised, skipping device.")
                
            time.sleep(2)
            
            ssh.enable()
            result = ssh.send_command(showcdpcmd)
            for line in result.splitlines():
                if "wired0" in line:
                    cdpneighbor_switch_name = line.split()[0].split(".")[0]
                    cdpneighbor_switch_location = line.split()[0].split(".")[0][:-3]              
                    cdpneighbor_chassis = line.split()[-2]
                elif "Gig 0" in line:
                    if "WS-C3" in line.split()[-3]:
                        if line.split()[-3][-1] == "-":
                            cdpneighbor_chassis = line.split()[-3][:-1]
                        else:
                            cdpneighbor_chassis = line.split()[-3]  
                    elif "C4503" in line:
                        if line.split()[-3][-1] == "-":
                            cdpneighbor_chassis = line.split()[-3][:-1]  
                        else:
                            cdpneighbor_chassis = line.split()[-3]
                    elif "C450" in line:
                        if line.split()[-3][-1] == "-":
                            cdpneighbor_chassis = line.split()[-3][:-1]  
                        else:
                            cdpneighbor_chassis = line.split()[-3]

                    else:
                        cdpneighbor_chassis = line.split()[-3][:-1]
                elif "net.wwu.edu" in line:
                    cdpneighbor_switch_name = line.split()[0].split(".")[0]
                    cdpneighbor_switch_location = line.split()[0].split(".")[0][:-3]            
                else:
                    continue
            print(f"     CDP Neighbor found: [{Fore.YELLOW+cdpneighbor_switch_name+Style.RESET_ALL}] ({cdpneighbor_chassis}/{cdpneighbor_switch_location})")
        
            
            for cmd in showcmds:
                result = ssh.send_command(cmd)
                for line in result.splitlines():
                    if "0n" in line:  
                        continue
                    bssid_value_match = re.search(regex_to_parse_out_bssid_value, line)
                    if bssid_value_match is None:
                        pass 
                    else:
                        bssid_bit = bssid_value_match.group(1)
                        
                        try:
                            bssid = ap_baseradiomac[:-1] + bssid_bit[3]
                        except IndexError as e:
                            try:
                                bssid = ap_baseradiomac[:-1] + bssid_bit[2]
                            except IndexError as e:
                                bssid = ap_baseradiomac[:-1] + bssid_bit[1]                            
                        data_bssid_cdpneighbors.append(f"{cdpneighbor_switch_name},{cdpneighbor_chassis},{cdpneighbor_switch_location},{ap_hostname},{bssid},{ap_location}")
                        print(f"        E911 Data:{cdpneighbor_switch_name},{cdpneighbor_chassis},{cdpneighbor_switch_location},{ap_hostname},{bssid},{ap_location}")
            
        return data_bssid_cdpneighbors


    def Play_WriteResultsToFile(data_bssid_cdpneighbors):
        with open(outputfile, "w") as WriteToFile:    
            for dataset in data_bssid_cdpneighbors:
                WriteToFile.write(f"{dataset}\n")


    listofaccesspoints = Play_GetListOfAccessPoints(filter)
    data_bssid_cdpneighbors = Play_GetCDPNeighborsAndBSSIDValues(listofaccesspoints)

    Play_WriteResultsToFile(data_bssid_cdpneighbors) 
