import json
from distutils import util

#~ from os.path import expanduser
#~ home = expanduser("~")

class ConfigReadWrite:
	gpioconfig_path = "/home/pi/indoor-config/gpio.config"
	serverconfig_path = "/home/pi/indoor-config/server.config"
	userconfig_path = "/home/pi/indoor-config/user.config"
	hostname_path = "/etc/machine-info"
	
	OK = "ok"
	HARD_RESET = "requires_hard_reset"
	BAD_REQUEST = "bad_request"
	ERROR = "error"
	
	def readConfigGpio(self):
		result = {}
		try:
			with open(self.gpioconfig_path) as f:
				for line in f:
					if line:
						if '=' in line:
							index = line.find('=')
							if index > 0:
								parametro = line[0:index]
								valor = line[index+1:].rstrip()
								try:
									boolvalor = util.strtobool(valor)
								except:
									print 'Error al leer el valor del parametro: ' + parametro + '. Los valores validos son true o false -> recibido: ' + valor
									boolvalor = False
								print parametro + ' ' + valor
								if parametro == 'luz':
									result['luz']=boolvalor
								elif parametro == 'bomba':
									result['bomba']=boolvalor
								elif parametro == 'humytemp':
									result['humytemp']=boolvalor
								elif parametro == 'fanintra':
									result['fanintra']=boolvalor
								elif parametro == 'fanextra':
									result['fanextra']=boolvalor
								elif parametro == 'humtierra':
									result['humtierra']=boolvalor
								elif parametro == 'camara':
									result['camara']=boolvalor
		except Exception, ex:
			import traceback
			print traceback.format_exc()
		return json.dumps(result)
		
	def writeConfigGpio(self, toWrite):
		try:
			try:
				objReq = json.loads(toWrite)
				if 'luz' not in objReq or 'bomba' not in objReq or 'humytemp' not in objReq or 'fanintra' not in objReq or 'fanextra' not in objReq or 'humtierra' not in objReq or 'camara' not in objReq:
					print('le falta algun atributo')
					return self.BAD_REQUEST 
			except Exception, parseEx:
				import traceback
				print traceback.format_exc()
				return self.BAD_REQUEST
			with open(self.gpioconfig_path, "w") as f:
				f.write('luz=' + str(objReq['luz']) + '\n')
				f.write('bomba=' + str(objReq['bomba']) + '\n')
				f.write('humytemp=' + str(objReq['humytemp']) + '\n')
				f.write('fanintra=' + str(objReq['fanintra']) + '\n')
				f.write('fanextra=' + str(objReq['fanextra']) + '\n')
				f.write('humtierra=' + str(objReq['humtierra']) + '\n')
				f.write('camara=' + str(objReq['camara']) + '\n')
		except Exception, ex:
			import traceback
			print traceback.format_exc()
			return self.ERROR
		return self.OK
	
	def readConfigServer(self):
		result = {}
		try:
			with open(self.serverconfig_path) as f:
				for line in f:
					if line:
						if '=' in line:
							index = line.find('=')
							if index > 0:
								parametro = line[0:index]
								valor = line[index+1:].rstrip()
								print parametro + ' ' + valor
								if parametro == 'queueUrl':
									result['queueUrl']=valor
								elif parametro == 'queueName':
									if not valor=='random':
										result['queueName']=valor
								elif parametro == 'queueUser':
									result['queueUser']=valor
								elif parametro == 'queuePassword':
									result['queuePassword']=valor
		except Exception, ex:
			import traceback
			print traceback.format_exc()
		return json.dumps(result)
		
	def writeConfigServer(self, toWrite):
		result = None
		try:
			old_indoor_name = ''
			try:
				objReq = json.loads(toWrite)
				if 'queueUrl' not in objReq or 'queueName' not in objReq or 'queueUser' not in objReq or 'queuePassword' not in objReq:
					print('le falta algun atributo')
					return self.BAD_REQUEST 
			except Exception, parseEx:
				import traceback
				print traceback.format_exc()
				return self.BAD_REQUEST
			
			result = self.OK
			with open(self.serverconfig_path, "w") as f:
				f.write('queueUrl=' + objReq['queueUrl'] + '\n')
				f.write('queueName=' + objReq['queueName'] + '\n')
				f.write('queueUser=' + objReq['queueUser'] + '\n')
				f.write('queuePassword=' + objReq['queuePassword'] + '\n')
			
			with open(self.hostname_path, 'r+w') as f:
				for line in f:
					if line:
						if 'PRETTY_HOSTNAME=' in line:
							index = line.find('=')
							if index > 0:
								old_indoor_name = line[index+1:].rstrip()
								if old_indoor_name != objReq['queueName']:
									f.seek(0)
									newLine = 'PRETTY_HOSTNAME=' + objReq['queueName']
									f.write(newLine)
									f.truncate()
									result = self.HARD_RESET
		except Exception, ex:
			import traceback
			print traceback.format_exc()
			return self.ERROR
		return result
		
	def readConfigUser(self):
		result = {}
		try:
			with open(self.userconfig_path) as f:
				for line in f:
					if line:
						if '=' in line:
							index = line.find('=')
							if index > 0:
								parametro = line[0:index]
								valor = line[index+1:].rstrip()
								result[parametro] = valor
		except Exception, ex:
			import traceback
			print traceback.format_exc()
		return json.dumps(result)
		
	def writeConfigUser(self, toWrite):
		result = None
		try:
			try:
				objReq = json.loads(toWrite)
				if not objReq:
					print('No hay ningun usuario para escribir')
					return self.BAD_REQUEST 
			except Exception, parseEx:
				import traceback
				print traceback.format_exc()
				return self.BAD_REQUEST
			with open(self.userconfig_path, "w") as f:
				for key in objReq:
					f.write(key + '=' + objReq[key] + '\n')
			result = self.OK
		except Exception, ex:
			import traceback
			print traceback.format_exc()
			return self.ERROR
		return result
