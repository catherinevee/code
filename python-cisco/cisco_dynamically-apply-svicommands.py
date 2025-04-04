
def Playbook_AddCmdToEverySVI(devices, commands):

    def Worker_AddCmdToEverySVI(task, commands):

        commands = Play_SanitizeCommandInput(commands)
        
        
        def Play_GetListOfSVIs(result):
            list_of_svis = []
            for line in result.splitlines():
                if "Vlan" in line and "up" in line:
                    if "208" in line or "203" in line or "165" in line:
                        pass
                    else:
                        line = line.split()
                        svi = line[0]
                        list_of_svis.append(svi)
            for svi in list_of_svis:
                print(f"[{Fore.GREEN}X{Style.RESET_ALL}] {svi}")
            return list_of_svis


        def Play_IterateThroughFoundSVIs(task, list_of_svis, commands):
            print(f"\nvvvv SVI CHECK**vvvvvvvvvvvvvvvvvvvvvvv INFO")
            commandSet = []
            for svi in list_of_svis:
                svicmd = f"show run int {svi}"
                result = task.run(
                    task=netmiko_send_command,
                    command_string=svicmd,
                    )
                result = Play_SendCommand_ParseOutput(result)
                #iterate through the "show run int" of an SVI
                for line in result.splitlines():
                    if "10.249.12.135" in line:
                        commandSet.append(f"interface {svi}")
                        for command in commands:
                            print(f"{svi} -> {Fore.YELLOW+line+Style.RESET_ALL} -> {command}")
                            commandSet.append(f"{command}")
            return commandSet
            
     
        def Play_SendCommandSet(task, commandSet):
            for cmd in commandSet:
                print(cmd)
                
            result = task.run(
                task=netmiko_send_config,
                config_commands=commandSet,
            )
            result = Play_SendCommand_ParseOutput(result)
            print(result)
            
            

            
        ip = str(task.host.hostname)
        hostname = str(task.host)
        print(f"\nConnecting to ({Fore.YELLOW+ip+Style.RESET_ALL}) / ({Fore.YELLOW+hostname+Style.RESET_ALL})...")
        shcommands = "do show ip int brief | i Vlan"
        result = task.run(
            task=netmiko_send_config,
            name=f"{ip}",
            config_commands=shcommands,
        )
        result = Play_SendCommand_ParseOutput(result)
        print(f"\nvvvv SVIS FOUND**vvvvvvvvvvvvvvvvvvvvvvv INFO")
        list_of_svis = Play_GetListOfSVIs(result)
        commandSet = Play_IterateThroughFoundSVIs(task, list_of_svis, commands)
        print(list_of_svis)
        print(commandSet)
        Play_SendCommandSet(task, commandSet)    
        
    result = devices.run(
            task=Worker_AddCmdToEverySVI,
            commands=commands
        )
        