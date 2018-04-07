import subprocess
import json

class WlanConfig:
	
	def scanNetworks(self):
		try:
			p = subprocess.Popen(["sudo", "iwlist", "wlan0", "scan"], stdout=subprocess.PIPE)
			output, error = p.communicate()
			if error != None:
				result = []
				items = output.split("Cell")
				for item in items:
					idxStart = item.index("ESSID:") + 8
					idxEnd = item.index('"',idxStart)
					strSSID = item[idxStart:idxEnd]
					result.append(strSSID)
				return json.dumps(result)
			else:
				return None
		except Exception, ex:
			import traceback
			print traceback.format_exc()
			return None
