#
#
def Play_SSHConnectionToWLC(wlc_hostname):
        wlc_fqdn = wlc_hostname + ".net.wwu.edu"
        adminusername = "venegaa"
        adminpassword = "smerdyashchaya!"
        print(f"\nConnecting to {Back.CYAN+wlc_fqdn+Style.RESET_ALL}...")        
        net_connect = {
            'device_type': 'cisco_ios',
                'host': wlc_fqdn,
                'username': adminusername,
                'password': adminpassword,
                'port': 22,        
        }
        return net_connect
