import json
import urllib2
import os

class MacAddressInfo:
    def __init__(self):
        self.mac_address = ""
        self.company = ""
        self.address1 = ""
        self.address2 = ""
        self.address3 = ""
        self.country = ""

class MacAddressStorage:
    def __init__(self):
        self.data = []    # creates a new empty list
 
    def mac_address_lookup_from_internet(self, mac_address):
        try:
            print "Load from Internet %s" % mac_address
            # Set the request URL http://www.macvendorlookup.com/api/v2/08-86-3B-D4-90-C0
            url = 'http://www.macvendorlookup.com/api/v2/' + mac_address

            # Send the GET request
            response = urllib2.urlopen(url)
            resp = response.read()

            mac_object = MacAddressInfo
            data = [] 
            
            if resp:
                # Interpret the JSON response
                #data = json.loads(resp.decode('utf8'))
                data = json.loads(resp)
                mac_object.mac_address = mac_address
                for company in data:
                    mac_object.company = company['company']
                for address1 in data:
                    mac_object.address1 = address1['addressL1']
                for address2 in data:
                    mac_object.address2 = address2['addressL2']
                for address3 in data:
                    mac_object.address3 = address3['addressL3']
                for country in data:
                    mac_object.country = country['country']
            else:
                mac_object.mac_address = mac_address
                mac_object.company = ""
                mac_object.address1 = ""
                mac_object.address2 = ""
                mac_object.address3 = ""
                mac_object.country = ""
                
            return mac_object
        except :
            print "Unexpected error:", url, resp
            return None

    def mac_address_lookup_from_cache(self, mac_address):
        try:
            self.load_data_from_file()
            count = len( self.data["mac addresses"] )
            for index in range(count):
                if self.data["mac addresses"][index]["macaddress"] == mac_address:
                    mac_object = MacAddressInfo 
                    mac_object.mac_address = mac_address
                    mac_object.company = self.data["mac addresses"][index]["company"]
                    mac_object.address1 = self.data["mac addresses"][index]["address1"]
                    mac_object.address2 = self.data["mac addresses"][index]["address2"]
                    mac_object.address3 = self.data["mac addresses"][index]["address3"]
                    mac_object.country = self.data["mac addresses"][index]["country"]
                    return mac_object
            
            return None
        except :
            print "mac_address_lookup_from_cache error:"
            return None

    def mac_address_lookup(self, mac_address):
        try:
            mac_object = self.mac_address_lookup_from_cache(mac_address)  
            if mac_object is None :
                mac_object = self.mac_address_lookup_from_internet(mac_address)
                if mac_object is not None :
                    #self.load_data_from_file()
                    print mac_address
                    self.data["mac addresses"].append( {"macaddress":mac_address, "company":mac_object.company, "address1":mac_object.address1, "address2":mac_object.address2, "address3":mac_object.address3, "country":mac_object.country} )
                    self.store_data_to_file()
                else :
                    return None
            return mac_object
        except :
            print "mac_address_lookup error:"
            return None

    def load_data_from_file(self):
        if len( self.data ) == 0:
            if os.path.exists("/home/pi/sniffer/mac_addresses.json"):
                file_handel = open('/home/pi/sniffer/mac_addresses.json', 'r')
                self.data = json.load(file_handel)
                #print "Load"
            else:
                #file_handel = open('/home/pi/sniffer/mac_addresses.json', 'w')
                self.data.append( {"mac addresses":[]} )
                #print "new"
                
        
    def store_data_to_file(self):
        file_handel = open('/home/pi/sniffer/mac_addresses.json', 'w')
        json.dump(self.data, file_handel, sort_keys=True, indent=2)
        #file_handel.write('\n')
            

if __name__ == '__main__':
    storage = MacAddressStorage()
    mac_object = MacAddressInfo()
    #mac_object = storage.mac_address_lookup("08:86:3B:D4:90:C0")
    #mac_object = storage.mac_address_lookup("6C:F3:73:E6:0A:11")
    mac_object = storage.mac_address_lookup("9C:6C:15:97:76:04")
    	
    #print storage.mac_address_lookup("08-86-3B-D4-90-C0").mac_address
    if mac_object :
        print mac_object.mac_address
        print mac_object.company
        print mac_object.address1
        print mac_object.address2
        print mac_object.address3
        print mac_object.country
    else :
        print "Error"
        
        
        
