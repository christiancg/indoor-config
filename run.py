import subprocess

p = subprocess.Popen(['sudo', 'hciconfig', 'hci0', 'name'], stdout=subprocess.PIPE)
result = p.communicate()
splitted = result[0].split('\n\t')
matching = [s for s in splitted if "Name" in s]
name = None
if matching is not None:
	matchingstr = ''.join(matching)
	idxstartname = matchingstr.find('\'')
	idxendname = matchingstr.find('\'', idxstartname)
	name = matchingstr[idxstartname + 1 : idxstartname+idxendname + 1]
	if name != 'indoor':
		subprocess.call(['sudo', 'hciconfig', 'hci0', 'name', 'indoor'])

subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])		
#subprocess.call(['sudo', 'hciconfig', 'hci0', 'name', '"indoor"'])
#subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
