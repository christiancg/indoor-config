import subprocess
import json

class WlanConfig:
	
	wpasupplicant_path = "/etc/wpa_supplicant/wpa_supplicant.conf"
	
	OK = "ok"
	BAD_REQUEST = "bad_request"
	ERROR = "error"
	
	def scanNetworks(self):
		try:
			p = subprocess.Popen(["iwlist", "wlan0", "scan"], stdout=subprocess.PIPE)
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

	def writeWifiPossibility(self, strObj):
		objReq = None
		try:
			objReq = json.loads(strObj)
			if 'ssid' not in objReq or 'password' not in objReq:
				return self.BAD_REQUEST
		except Exception:
			import traceback
			print traceback.format_exc()
			return self.BAD_REQUEST
		try:
			with open(self.wpasupplicant_path, "a") as f:
				f.write('\nnetwork={\n')
				f.write('         ssid="' + objReq['ssid'] + '"\n')
				f.write('         psk="' + objReq['password'] + '"\n')
				f.write('}\n')
			return self.OK
		except Exception:
			import traceback
			print traceback.format_exc()
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
			return None
