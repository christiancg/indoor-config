import json
from distutils import util

from os.path import expanduser
home = expanduser("~")

class ConfigReadWrite:
	gpioconfig_path = home + "/indoor-config/gpio.config"
	serverconfig_path = home + "/indoor-config/server.config"
	
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
