import subprocess
from wifi import Cell, Scheme
import json
from logger import Logger
log = Logger(__name__)

class WlanConfig:
	
	#~ wpasupplicant_path = "/etc/wpa_supplicant/wpa_supplicant.conf"
	
	OK = "ok"
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
			result = []
			networks = Cell.all('wlan0')
			for item in networks:
				auxSecurity = None
				if item.encrypted:
					auxSecurity = item.encryption_type
				auxResult = { "ssid": item.ssid, "security_type": auxSecurity }
				result.append(auxResult)
			return json.dumps(result)
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
				scheme = Scheme.for_cell('wlan0', 'indoor', cell, passkey)
				scheme.save()
				#~ scheme.activate()
				subprocess.call(["sudo", "ifdown", "wlan0"])
				subprocess.call(["sudo", "ifup", "wlan0"])
				return self.OK
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
