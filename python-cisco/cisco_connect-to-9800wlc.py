from nornir_function_file import *
from colorama import Fore, Style, init, Back, colorama
# colorama needs to initialize for colored text to show in Windows
# after a colored text line appears, auto-reset to plain (white) text
# these colors add additional characters to the string, so the color values are concatenated
# into the string
init(autoreset=True)
colorama.init()

def Play_ImportFileOfAPs(file):
    listofaccesspoints = []
    with open(file, "r") as FileOpen:
        for line in FileOpen.readlines():
            line = line.strip()
            line = f"{line.split(',')[0]},{line.split(',')[1]},{line.split(',')[2].replace(' ', '')},{line.split(',')[3]}"
            print(line)
            listofaccesspoints.append(line)

    # print(listofaccesspoints)
    return listofaccesspoints

controllers_9800 = [
    "W10",
    "W11",
    "W12",
    ]

def Play_GetListOfAccessPoints(wlc="none",filter="none"):
    listofaccesspoints = []
    if wlc == "none":
        controllers = controllers_9800
    else:
        controllers = [
        wlc
        ]
        
    for wlc in controllers:
        result = NornirCreateConnection(wlc)
        devices = result[0]    
        result = Playbook_SendIOSCommand(devices,commands=["show ap summary"])
        wlc = wlc + ".net"
        try:
            output_as_string = str(result[wlc][1])
        except TypeError as e:
            print(f"Type Error:{e}")
        print("===================================")
        print(f"Access Points that fit within the {Fore.YELLOW+filter+Style.RESET_ALL} filter:")
        print("===================================")
            
        for line in output_as_string.splitlines():        
            if "US" in line:
                ap_hostname = line.split()[0]
                ap_baseradiomac = line.split()[4]
                if "US" in line.split()[6].strip():
                    ap_location = line.split()[5].strip()   
                    ap_ip = line.split()[7]                      
                else:
                    ap_location = line.split()[5].strip() + line.split()[6].strip()
                    ap_ip = line.split()[8]  

                if filter == "none":
                    print(f"[{Back.CYAN+ap_location+Style.RESET_ALL}] - {Back.CYAN+ap_hostname+Style.RESET_ALL} ({ap_baseradiomac}/{Fore.YELLOW+ap_ip+Style.RESET_ALL})")
                    listofaccesspoints.append(f"{ap_hostname},{ap_baseradiomac},{ap_location},{ap_ip}")
                else:
                    if "defaultlocation" in ap_location:
                        print(f"[{Back.MAGENTA+ap_location+Style.RESET_ALL}] - {Back.CYAN+ap_hostname+Style.RESET_ALL} ({ap_baseradiomac}/{Fore.YELLOW+ap_ip+Style.RESET_ALL})")
                        listofaccesspoints.append(f"{ap_hostname},{ap_baseradiomac},{ap_location},{ap_ip}")
                     
                    elif filter in ap_location:
                        print(f"[{Back.CYAN+ap_location+Style.RESET_ALL}] - {Back.CYAN+ap_hostname+Style.RESET_ALL} ({ap_baseradiomac}/{Fore.YELLOW+ap_ip+Style.RESET_ALL})")
                        listofaccesspoints.append(f"{ap_hostname},{ap_baseradiomac},{ap_location},{ap_ip}")
 
                    else:
                        
                        print(f"[{Fore.YELLOW+ap_location+Style.RESET_ALL}] - {Fore.YELLOW+ap_hostname+Style.RESET_ALL}")
            else:
                pass
    return listofaccesspoints
    

if __name__ == "__main__":    
    Play_GetListOfAccessPoints("AZ")


