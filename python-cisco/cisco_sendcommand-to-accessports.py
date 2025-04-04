
def Playbook_SendCommandToAllAccessPorts(devices):
    def Worker_ParseOutput(task, switchport_cmd_output):
        # print(f"\nvvvv CDP NEIGHBOR SEARCH: {Back.CYAN+str(task.host).split('.')[0]+Style.RESET_ALL}** vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
        # print(f"has these CDP neighbors:")
        for interface in switchport_cmd_output.splitlines():
            interface_cmd = f"show run interface {str(interface).split(':')[1].strip()}"
            interface_cmd_output = task.run(
                    task=netmiko_send_command,
                    command_string=interface_cmd,
                )  
            interface_cmd_output = Play_SendCommand_ParseOutput(interface_cmd_output)
            print(interface_cmd)
            for line in interface_cmd_output.splitlines():
                line = line.strip()
                if "Building configuration" in line:
                    pass
                elif "Current configuration" in line:
                    pass
                elif "!" in line:
                    pass
                elif "switchport mode trunk" in line:
                    print(f"    {Back.GREEN+line+Style.RESET_ALL}")                
                elif "bpdufilter enable" in line:
                    print(f"    {Back.CYAN+line+Style.RESET_ALL}")                
                else:
                    print(f"    {Back.MAGENTA+line+Style.RESET_ALL}")
            

    def Worker_SendCommand(task):
        switchport_cmd_output = task.run(
            task=netmiko_send_command,
            command_string="sh int switchport | i Name:",
        )
        switchport_cmd_output = Play_SendCommand_ParseOutput(switchport_cmd_output)
        Worker_ParseOutput(task, switchport_cmd_output)
        
        

    switchport_cmd_output = devices.run(
            task=Worker_SendCommand,
        )
