controllers_9800 = ["wlc1","wlc2"]


def Playbook_SendCommandToWLC():
    commands = [
    "do sh ver | i 9800",
    "do sh user"
    ]
    
    def TryAuthentication(net_connect):
        try:
            print(f"...successful SSH to {wlc}.")        
            ssh_handler = ConnectHandler(**net_connect)
            print("======================")
        except NetmikoTimeoutException as e:
            print(f"NetmikoTimeoutException raised using {str(net_connect)}, trying again with same credentials...")
            try:
                ssh = ConnectHandler(**net_connect)
            except NetmikoTimeoutException as e:
                print(f"NetmikoTimeoutException to {str(net_connect)} raised again, skipping device.")
                return
        return ssh_handler
        

    def SendCommandsToWLC(wlc,list_of_commands):
        try:
            result = ssh_handler.send_config_set(list_of_commands)
            for line in result.splitlines():
                if "configure terminal" in line:
                    pass
                elif "Enter configuration commands" in line:
                    pass
                elif "(config)#end" in line:
                    pass
                elif ")#" in line:
                    print(f"\n    {line}")                
                else:
                    print(f"    {Back.MAGENTA+line+Style.RESET_ALL}")
                
        except NetmikoTimeoutException:
            time.sleep(20)
            print(f"NetmikoTimeoutException raised connecting to {wlc}, skipping device.")
            return

    for wlc in controllers_9800:
        net_connect = Play_SSHConnectionToWLC(wlc)
        ssh_handler = TryAuthentication(net_connect)
        

        print("Sending below commands..")  
        for command in commands:
            print(f"    {Fore.YELLOW+command+Style.RESET_ALL}")
        print("\n")
        SendCommandsToWLC(wlc, commands)
