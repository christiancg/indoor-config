import subprocess
import json

class WlanConfig:
	
	wpasupplicant_path = "/etc/wpa_supplicant/wpa_supplicant.conf"
	
	def scanNetworks(self):
		try:
			p = subprocess.Popen(["sudo", "iwlist", "wlan0", "scan"], stdout=subprocess.PIPE)
			output, error = p.communicate()
			if error == None:
				result = []
				items = output.split("Cell")
				for item in items:
					try:
						idxStart = item.index("ESSID:")
					except ValueError:
						idxStart = -1
					if idxStart > 0:
						idxStart = idxStart + 7
						idxEnd = item.index('"',idxStart)
						strSSID = item[idxStart:idxEnd]
						isSecure = ("PSK" in item)
						auxResult = { "ssid": strSSID, "secure": isSecure } 
						result.append(auxResult)
				return json.dumps(result)
			else:
				print('Salio con error al buscar redes wifi')
				return None
		except Exception, ex:
			import traceback
			print traceback.format_exc()
			return None

	def writeWifiPossibility(self, ssid, password):
		try:
			with open(self.wpasupplicant_path, "a") as f:
				f.write('\nnetwork={\n')
				f.write('         ssid="' + ssid + '"\n')
				f.write('         psk="' + password + '"\n')
				f.write('}\n')
			return True
		except Exception:
			import traceback
			print traceback.format_exc()
			return False
			
	def getConnectedNetwork(self):
		try:
			p = subprocess.Popen(["iwgetid"], stdout=subprocess.PIPE)
			output, error = p.communicate()
			if error == None:
				connectedSsid = ""
				if "ESSID:" in output:
					idxStart = item.index("ESSID:") + 1
					connectedSsid = item[idxStart:-1]
				return connectedSsid
			else:
				return "error"
		except Exception, ex:
			import traceback
			print traceback.format_exc()
			return None
