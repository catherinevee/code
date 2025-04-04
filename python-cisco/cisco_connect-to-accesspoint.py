#
#

def Play_SSHConnectionToAP(ap_hostname, ap_ip):
        localadminusername = ""
        localadminpassword = "@n^!"
        print(f"\nConnecting to {Back.CYAN+ap_hostname+Style.RESET_ALL} at {Fore.YELLOW+ap_ip+Style.RESET_ALL}...")        
        net_connect = {
            'device_type': 'cisco_ios',
                'host': ap_ip,
                'username': localadminusername,
                'password': localadminpassword,
                'secret': localadminpassword,
                'port': 22,        
        }
        return net_connect
