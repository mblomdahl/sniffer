import json
import datetime as dt
import mac_address_info

def mac_address_name( mac_address ):
    #print bssid_dict.has_key(mac_address), mac_address
    if bssid_dict.has_key(mac_address):
        #print bssid_dict[mac_address]
        return bssid_dict[mac_address]
    else:
        infile = open('/home/pi/sniffer/config.json', 'r')
        #reader = infile.readlines()
        #print reader
        json_object = json.load(infile)

        for attribute, value in json_object.iteritems():
            #print attribute, value # example usage
            if attribute == mac_address:
                return value
        return mac_address



#mac_address_name("aaa")
bssid_dict = dict()
            
lastHourDateTime = dt.datetime.now() - dt.timedelta(hours = 1)
infile = open('/var/log/aircrack-ng/sniff.txt-01.csv', 'r')
jsonfile = open('/var/log/aircrack-ng/log.json', 'a')
# lastHourDateTime = dt.datetime.now() - dt.timedelta(hours = 10000)
# infile = open('/home/pi/sniff.txt.csv', 'r')
# jsonfile = open('/home/pi/log.json', 'a')

storage = mac_address_info.MacAddressStorage()
#mac_object = mac_address_info.MacAddressInfo()

reader = infile.readlines()
for line in reader:
    #print line
    mylist = line.split(', ')
    #print len(mylist)
    if len(mylist) == 14 and len(mylist[0]) == 17 and len(mylist[12]) > 0:
        #print mylist[0], mylist[12]
        bssid_dict[mylist[0]] = mylist[12]

    if len(mylist) == 15 and len(mylist[0]) == 17 and len(mylist[13]) > 0:
        #print mylist[0], mylist[13]
        bssid_dict[mylist[0]] = mylist[13]
    
    if len(mylist) == 7 and len(mylist[0]) == 17:
        #print mylist[2]
        #print dt.datetime.now().strftime('%Y-%m-%d %X')
        #oLastTime = dt.datetime.strptime("%Y-%m-%d %X", mylist[2])
        #if oLastTime > lastHourDateTime:

        if mylist[2] > lastHourDateTime.strftime('%Y-%m-%d %X'):
            mac_object = storage.mac_address_lookup(mylist[0])
            if mac_object :
                mydict = {
                "StationMAC":mylist[0],
                "Device":mac_address_name(mylist[0]),
                "FirstTimeSeen":mylist[1],
                "LastTimeSeen":mylist[2],
                "Power":mylist[3],
                "Packets":mylist[4].strip(),
                "BSSID":mylist[5],
                "BSSIDName":mac_address_name(mylist[5]),
                "ProbedESSIDs":mylist[6].strip(),
                "Vendor":mac_object.company
                }
                json.dump(mydict, jsonfile)
                jsonfile.write('\n')
