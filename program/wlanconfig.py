import re
import subprocess
from wifi import Cell, Scheme
import json
from logger import Logger
log = Logger(__name__)

class WlanConfig:
	
	#~ wpasupplicant_path = "/etc/wpa_supplicant/wpa_supplicant.conf"
	
	OK = "ok"
	HARD_RESET = "requires_hard_reset"
	BAD_REQUEST = "bad_request"
	ERROR = "error"
	
	def scanNetworks(self):
		try:
			#~ p = subprocess.Popen(["iwlist", "wlan0", "scan"], stdout=subprocess.PIPE)
			#~ output, error = p.communicate()
			#~ if error == None:
				#~ result = []
				#~ items = output.split("Cell")
				#~ for item in items:
					#~ try:
						#~ idxStart = item.index("ESSID:")
					#~ except ValueError:
						#~ idxStart = -1
					#~ if idxStart > 0:
						#~ idxStart = idxStart + 7
						#~ idxEnd = item.index('"',idxStart)
						#~ strSSID = item[idxStart:idxEnd]
						#~ isSecure = ("PSK" in item)
						#~ auxResult = { "ssid": strSSID, "secure": isSecure }
						#~ result.append(auxResult)
				#~ return json.dumps(result)
			#~ else:
				#~ print('Salio con error al buscar redes wifi')
				#~ return None
			result = ''
			networks = Cell.all('wlan0')
			for item in networks:
				auxSecurity = None
				if item.encrypted:
					auxSecurity = item.encryption_type
				result = result +  item.ssid + '-' + auxSecurity
				if (networks.index(item) + 1) != len(networks):
					result = result + '|'
			return str(result)
		except Exception, ex:
			import traceback
			print traceback.format_exc()
			log.exception(ex)
			return None

	def writeWifiPossibility(self, strObj):
		objReq = None
		try:
			objReq = json.loads(strObj)
			if 'ssid' not in objReq or 'password' not in objReq:
				return self.BAD_REQUEST
		except Exception, ex:
			import traceback
			print traceback.format_exc()
			log.exception(ex)
			return self.BAD_REQUEST
		try:
			#~ with open(self.wpasupplicant_path, "a") as f:
				#~ f.write('\nnetwork={\n')
				#~ f.write('         ssid="' + objReq['ssid'] + '"\n')
				#~ f.write('         psk="' + objReq['password'] + '"\n')
				#~ f.write('}\n')
			#~ return self.OK
			cell = self._findFromSearchList(objReq['ssid'])
			if cell:
				passkey = objReq['password']
				self._delete('indoor')
				#scheme = Scheme.for_cell('wlan0', 'indoor', cell, passkey)
				#scheme.save()
				#~ scheme.activate()
				scheme = SchemeWPA('wlan0',cell.ssid,{"ssid":cell.ssid,"psk":passkey})
				scheme.save()
				return self.HARD_RESET
			else:
				return self.BAD_REQUEST
		except Exception, ex:
			import traceback
			print traceback.format_exc()
			log.exception(ex)
			return self.ERROR
			
	def getConnectedNetwork(self):
		try:
			p = subprocess.Popen(["iwgetid"], stdout=subprocess.PIPE)
			output, error = p.communicate()
			if error == None:
				connectedSsid = ""
				if "ESSID:" in output:
					idxStart = output.index("ESSID:") + 7
					connectedSsid = output[idxStart:-2]
				return connectedSsid
			else:
				return "error"
		except Exception, ex:
			import traceback
			print traceback.format_exc()
			log.exception(ex)
			return None
			
	def _findFromSearchList(self,ssid):
		wifilist = Cell.all('wlan0')
		for cell in wifilist:
			if cell.ssid == ssid:
				return cell
		return False
		
	def _findFromSavedList(self,ssid):
		cell = Scheme.find('wlan0', ssid)
		if cell:
			return cell
		return False
		
	def _delete(self,key):
		if not key:
			return False
		cell = self._findFromSavedList(key)
		if cell:
			cell.delete()
			return True
		return False



import wifi.subprocess_compat as subprocessWPA
from wifi.utils import ensure_file_exists

class SchemeWPA(Scheme):

    interfaces = "/etc/wpa_supplicant/wpa_supplicant.conf"

    def __init__(self, interface, name, options=None):
        self.interface = interface
        self.name = name
        self.options = options or {} 

    def __str__(self):
        """
        Returns the representation of a scheme that you would need
        in the /etc/wpa_supplicant/wpa_supplicant.conf file.
        """

        options = ''.join("\n    {k}=\"{v}\"".format(k=k, v=v) for k, v in self.options.items())
        return "network={" + options + '\n}\n'

    def __repr__(self):
            return 'Scheme(interface={interface!r}, name={name!r}, options={options!r}'.format(**vars(self))
    def save(self):
        """
        Writes the configuration to the :attr:`interfaces` file.
        """
        if not self.find(self.interface, self.name):
            with open(self.interfaces, 'a') as f:
                f.write('\n')
                f.write(str(self))        

    @classmethod
    def all(cls):
        """
        Returns an generator of saved schemes.
        """
        ensure_file_exists(cls.interfaces)
        with open(cls.interfaces, 'r') as f:
            return extract_schemes(f.read(), scheme_class=cls) 
    def activate(self):
        """
        Connects to the network as configured in this scheme.
        """

        subprocessWPA.check_output(['/sbin/ifdown', self.interface], stderr=subprocessWPA.STDOUT)
        ifup_output = subprocessWPA.check_output(['/sbin/ifup', self.interface] , stderr=subprocessWPA.STDOUT)
        ifup_output = ifup_output.decode('utf-8')

        return self.parse_ifup_output(ifup_output)
    def delete(self):
        """
        Deletes the configuration from the /etc/wpa_supplicant/wpa_supplicant.conf file.
        """
        content = ''
        with open(self.interfaces, 'r') as f:
            lines=f.read().splitlines()
            while lines:
                line=lines.pop(0)

                if line.startswith('#') or not line:
                    content+=line+"\n"
                    continue

                match = scheme_re.match(line)
                if match:
                    options = {}
                    ssid=None
                    content2=line+"\n"
                    while lines and lines[0].startswith(' '):
                        line=lines.pop(0)
                        content2+=line+"\n"
                        key, value = re.sub(r'\s{2,}', ' ', line.strip()).split('=', 1)
                        #remove any surrounding quotes on value
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        #store key, value
                        options[key] = value
                        #check for ssid (scheme name)
                        if key=="ssid":
                            ssid=value
                    #get closing brace        
                    line=lines.pop(0)
                    content2+=line+"\n"

                    #exit if the ssid was not found so just add to content
                    if not ssid:
                        content+=content2
                        continue
                    #if this isn't the ssid then just add to content
                    if ssid!=self.name:
                        content+=content2

                else:
                    #no match so add content
                    content+=line+"\n"
                    continue

        #Write the new content
        with open(self.interfaces, 'w') as f:
            f.write(content)    

scheme_re = re.compile(r'network={\s?')


#override extract schemes
def extract_schemes(interfaces, scheme_class=SchemeWPA):
    lines = interfaces.splitlines()
    while lines:
        line = lines.pop(0)
        if line.startswith('#') or not line:
            continue

        match = scheme_re.match(line)
        if match:
            options = {}
            interface="wlan0"
            ssid=None

            while lines and lines[0].startswith(' '):
                key, value = re.sub(r'\s{2,}', ' ', lines.pop(0).strip()).split('=', 1)
                #remove any surrounding quotes on value
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                #store key, value
                options[key] = value
                #check for ssid (scheme name)
                if key=="ssid":
                    ssid=value

            #exit if the ssid was not found
            if ssid is None:
                continue
            #create a new class with this info
            scheme = scheme_class(interface, ssid, options)

            yield scheme
