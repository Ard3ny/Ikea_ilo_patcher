import paramiko
import time
import re
import os

hostrepo = 'deika9010is021p'
usernamerepo = 'cio_ad_s'
passwordrepo = 'TsimbCIO5!'
# hostrepo = '192.168.100.8'          #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# usernamerepo = 'root'                  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# passwordrepo = 'aaa'                     #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
print ('You will be logged in as ' + usernamerepo)

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostrepo, username=usernamerepo, password=passwordrepo)
channel = client.invoke_shell()

# clear welcome message and send newline
time.sleep(1) 
channel.recv(9999)
channel.send("\n")
time.sleep(1)


#sed old BU code for new in hostname
cmds_ls_of_repo = ["""sudo su -""", """%(passwordrepo)s""" % locals(), """ls -1 /root/config"""]             #list of ls, one per line
for ls in cmds_ls_of_repo:
    channel.send(ls + "\n")
    while not channel.recv_ready(): #Wait for the server to read and respond
        time.sleep(0.5)
    time.sleep(0.1) #wait enough for writing to (hopefully) be finished
    ls_of_repo = channel.recv(9999) #read invoke_shell
    string_of_ls_of_repo= str(ls_of_repo.decode('utf-8'))               #makes string of recieve from console
    time.sleep(0.5)

#print ('test1' + string_of_ls_of_repo)


#string_of_ls_of_repo of all servers
pattern = re.compile(r'..\d\d\d')
matches = pattern.findall(string_of_ls_of_repo)
stringofmatches = str(matches)
for match in matches:
    #channel.close()
    #print('test3' + match)
    client = paramiko.SSHClient()                                                   #again connects to repo server so it can get another ip from cat of next server
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostrepo, username=usernamerepo, password=passwordrepo)
    channel = client.invoke_shell()

    time.sleep(1) 
    channel.recv(9999)
    channel.send("\n")
    time.sleep(1)
    
    cmd_cat_of_server = ["""sudo cat /root/config/%(match)s""" % locals()]                               #cat of server config file so i can get his ILO IP adress
    for cat in cmd_cat_of_server:
        channel.send(cat + "\n")
        while not channel.recv_ready():
            time.sleep(1)
        time.sleep(1) 
        cat_of_repo = channel.recv(9999) #read invoke_shell
        string_of_cat_of_repo= str(cat_of_repo.decode(encoding='utf-8', errors='ignore'))         
        #print (string_of_cat_of_repo)
        time.sleep(0.5)

                                                                #ILO_IPADDR="10.28.108.17"
        pattern2 = re.compile(r'ILO_IPADDR="....+?(?=\")')                                                  #patern looking for ilo ip addrs
        matches2 = pattern2.findall(string_of_cat_of_repo)
        stringofmatches2 = str(matches2)                    #['ILO_IPADDR="192.168.10.5']   output
        sliceofstringofmatches2 = stringofmatches2[14:-2]       #192.168.10.5 output
        channel.close() #zavre shh channel


                                                                                                            #login to ILO via SSH
        hostofserver = sliceofstringofmatches2                                                              #ip address taken from repo server           
        usernameserver = 'cio_ad_bx'          #cio_ad_bx    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! when testing 'root'                                                   
        passwordserver = 'ILOikea2015'          #cio ad bx password !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! when testing 'aaa'
        print('You are connected to  ' + hostofserver + ' with name ' + match)

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostofserver, username=usernameserver, password=passwordserver)
        channel = client.invoke_shell()

        
        time.sleep(1) 
        channel.recv(9999)
        channel.send("\n")
        time.sleep(1)
        
    cmd_cat_of_server = ["""show /map1/firmware1"""]         #later change to show /map1/firmware1       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    for catt in cmd_cat_of_server:
        channel.send(catt + "\n")
        while not channel.recv_ready():
            time.sleep(2)
        time.sleep(5) #
        cat_of_server = channel.recv(9999) 
        string_of_cat_of_server= str(cat_of_server.decode('utf-8'))
        #print ('test 1 ' + string_of_cat_of_server)                                #whole output of show/map1/firmware1, we only need the firmware line    
        time.sleep(0.5)


    #string_of_cat_of_server 
    pattern3 = re.compile(r'name=iLO\s\d')                         #patternt looking for iLO 4/ iLO5 line
    matches3 = pattern3.findall(string_of_cat_of_server)
    stringofmatches3 = str(matches3)
    firmware_version = stringofmatches3[7:-2]               #output iLO 4
    #print('test 2 ' + firmware_version)                   

    if firmware_version == 'iLO 4':                              #function for what to do if ilo 4 or ilo 5                     
        #print ('Uhadlo spravne ze to je ilo 4')                                                                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #cmds_load_of_server = ["""touch /tmp/fungujeto4"""]
        cmds_load_of_server = ["""load /map1/firmware1 -source http://10.60.215.27/pub/iso/ilo_firmwares/ilo4_275.bin"""]   
        for load in cmds_load_of_server:
            channel.send(load + "\n")
            while not channel.recv_ready():
                time.sleep(0.5) 
            load_of_server = channel.recv(9999) 
            string_of_load_of_server= str(load_of_server.decode('utf-8'))
            print (string_of_load_of_server)
            print (firmware_version + ' of server ' + match + " was successfully patched with version " + firmware_version)              
            time.sleep(0.5)

    elif firmware_version == 'iLO 5':
       # print ('Uhadlo spravne ze to je ilo 5')                                                                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #cmds_load_of_server = ["""touch /tmp/fungujeto5"""]
        cmds_load_of_server = ["""load /map1/firmware1 -source http://10.60.215.27/pub/iso/ilo_firmwares/ilo5_230.bin"""]   
        for load in cmds_load_of_server:
            channel.send(load + "\n")
            while not channel.recv_ready():
                time.sleep(0.5) 
            load_of_server = channel.recv(9999) 
            string_of_load_of_server= str(load_of_server.decode('utf-8'))
            print (string_of_load_of_server)
            print (firmware_version + ' of server ' + match + " was successfully patched with version " + firmware_version)              
            time.sleep(0.5)
            channel.close()
    
    #time.sleep(5)

    

time.sleep(20)                                  #docasny stop kym vymyslim nieco lpesie




