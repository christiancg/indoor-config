import subprocess


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
		else:
			return self.BAD_REQUEST 

	def _startServer(self):
		return self.OK
		
	def _stopServer(self):
		return self.OK
		
	def _restartServer(self):
		return self.OK
