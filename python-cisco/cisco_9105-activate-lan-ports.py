with open("aps.txt", "r") as OpenAPFile:
    for line in OpenAPFile.readlines():
        print("ap name "+line.strip()+"  lan port-id 1 enable")
        print("ap name "+line.strip()+"  lan port-id 2 enable")
        print("ap name "+line.strip()+"  lan port-id 3 enable")