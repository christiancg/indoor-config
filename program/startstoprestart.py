import subprocess
import os

class StartStopRestart:	
	OK = "ok"
	BAD_REQUEST = "bad_request"
	ERROR = "error"

	def process(self, todo):
		if todo == 1:
			return self._startServer()
		elif todo == 2:
			return self._stopServer()
		elif todo == 3:
			return self._restartServer()
		elif todo == 4:
			return self._hardRestartServer()
		elif todo == 5:
			return self._disconnectFromBluetoothDevice()
		else:
			return self.BAD_REQUEST 

	def _startServer(self):
		subprocess.call(['sudo', 'service', 'indoor', 'start'])
		return self.OK
		
	def _stopServer(self):
		subprocess.call(['sudo', 'service', 'indoor', 'stop'])
		return self.OK
		
	def _restartServer(self):
		subprocess.call(['sudo', 'service', 'indoor', 'restart'])
		return self.OK
		
	def _hardRestartServer(self):
		subprocess.call(['sudo', 'reboot'])
		return self.OK
		
	def _disconnectFromBluetoothDevice(self):
		p = subprocess.Popen('sudo echo -e devices | bluetoothctl', shell=True, stdout=subprocess.PIPE)
		output, error = p.communicate()
		if error == None:
			print(output)
			devices = []
			for item in output.split("\n"):
				if "Device" in item:
					try:
						idxStart = item.index(" ")
					except ValueError:
						idxStart = -1
					if idxStart > 0:
						idxStart = idxStart + 1
						idxEnd = item.index(' ',idxStart)
						aux_device = item[idxStart:idxEnd]
						devices.append(aux_device)
			for device in devices:
				subprocess.call('sudo echo -e "remove ' + device + '" | bluetoothctl', shell=True)
		return self.OK

	def isServiceRunning(self):
		try:
			with open(os.devnull, 'wb') as hide_output:
				exit_code = subprocess.Popen(['service', 'indoor', 'status'], stdout=hide_output, stderr=hide_output).wait()
				return exit_code == 0
		except Exception, ex:
			print('Salio por excepcion: ' + ex)
			return 'error'
