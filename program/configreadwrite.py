import json
from distutils import util

from os.path import expanduser
home = expanduser("~")

class ConfigReadWrite:
	gpioconfig_path = home + "/indoor-config/gpio.config"
	serverconfig_path = home + "/indoor-config/server.config"
	
	OK = "ok"
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
									result['tiene_luz']=boolvalor
								elif parametro == 'bomba':
									result['tiene_bomba']=boolvalor
								elif parametro == 'humytemp':
									result['tiene_humytemp']=boolvalor
								elif parametro == 'fanintra':
									result['tiene_fanintra']=boolvalor
								elif parametro == 'fanextra':
									result['tiene_fanextra']=boolvalor
								elif parametro == 'humtierra':
									result['tiene_humtierra']=boolvalor
								elif parametro == 'camara':
									result['tiene_camara']=boolvalor
		except Exception, ex:
			import traceback
			print traceback.format_exc()
		return json.dumps(result)
		
	def writeConfigGpio(self, toWrite):
		try:
			try:
				objReq = json.loads(toWrite)
				if 'tiene_luz' not in objReq or 'tiene_bomba' not in objReq or 'tiene_humytemp' not in objReq or 'tiene_fanintra' not in objReq or 'tiene_fanextra' not in objReq or 'tiene_humtierra' not in objReq or 'tiene_camara' not in objReq:
					print('le falta algun atributo')
					return self.BAD_REQUEST 
			except Exception, parseEx:
				import traceback
				print traceback.format_exc()
				return self.BAD_REQUEST
			with open(self.gpioconfig_path, "w") as f:
				f.write('luz=' + str(objReq['tiene_luz']) + '\n')
				f.write('bomba=' + str(objReq['tiene_bomba']) + '\n')
				f.write('humytemp=' + str(objReq['tiene_humytemp']) + '\n')
				f.write('fanintra=' + str(objReq['tiene_fanintra']) + '\n')
				f.write('fanextra=' + str(objReq['tiene_fanextra']) + '\n')
				f.write('humtierra=' + str(objReq['tiene_humtierra']) + '\n')
				f.write('camara=' + str(objReq['tiene_camara']) + '\n')
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
		try:
			try:
				objReq = json.loads(toWrite)
				if 'queueUrl' not in objReq or 'queueName' not in objReq or 'queueUser' not in objReq or 'queuePassword' not in objReq:
					print('le falta algun atributo')
					return self.BAD_REQUEST 
			except Exception, parseEx:
				import traceback
				print traceback.format_exc()
				return self.BAD_REQUEST
			with open(self.serverconfig_path, "w") as f:
				f.write('queueUrl=' + objReq['queueUrl'] + '\n')
				f.write('queueName=' + objReq['queueName'] + '\n')
				f.write('queueUser=' + objReq['queueUser'] + '\n')
				f.write('queuePassword=' + objReq['queuePassword'] + '\n')
		except Exception, ex:
			import traceback
			print traceback.format_exc()
			return self.ERROR
		return self.OK
