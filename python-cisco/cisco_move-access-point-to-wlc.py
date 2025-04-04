
def Playbook_MoveToWLC(wlc_to_move_to,wlc="none", ap_filter="none"):
    def Play_SendCommandToEveryAccessPoint(listofaccesspoints, commands):
        # print(commands)

        for ap_data in listofaccesspoints:        
            ap_hostname = str(ap_data.split(",")[0])
            ap_hostname = ap_hostname.split(".")[0]
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
            for command in commands:
                try:
                    result = ssh.send_command(command)
                    for line in result.splitlines():
                        print(line)
                except OSError:
                    print("Commands were sent successfully.")
                    continue

    if wlc_to_move_to == "dghfghf":
        commands = [
        "capwap ap primary-base rwe 10.111.10.26",  
        "capwap ap secondary-base rrwerew 10.111.10.27",        
        "capwap ap tertiary-base dfds 10.111.10.25",
        "capwap ap restart"
        ]
    elif wlc_to_move_to == "wrewr":
        commands = [
        "capwap ap primary-base dfdfgsdg 10.111.10.28",
        "capwap ap secondary-base werwer 10.111.10.29",
        "capwap ap tertiary-base xvxcvxsd 10.111.10.26",
        "capwap ap restart"
        ]
    elif wlc_to_move_to == "rrwerw":
        commands = [
        "capwap ap primary-base asdadas 10.111.10.29",
        "capwap ap secondary-base dfsdfsd 10.111.10.28",
        "capwap ap tertiary-base cxvxcvc 10.111.10.26",
        "capwap ap restart"
        ]
    elif wlc_to_move_to == "fdgfd":
        commands = [
        "capwap ap primary-base dfgdfgdf 10.111.10.24",
        "capwap ap secondary-base asdassad 10.111.10.23",
        "capwap ap tertiary-base asdasd 10.111.10.26",
        "capwap ap restart"
        ]
    elif wlc_to_move_to == "BH011BW04":
        commands = [
        "capwap ap primary-base sdfsd 10.111.10.23",
        "capwap ap secondary-base asdsad 10.111.10.24",
        "capwap ap tertiary-base asdasd 10.111.10.25",
        "capwap ap restart"
        ]
        
    listofaccesspoints = Play_GetListOfAccessPoints(wlc,ap_filter)

    print(commands)
    
    Play_SendCommandToEveryAccessPoint(listofaccesspoints, commands)    