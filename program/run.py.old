#~ import subprocess
#~ import bluetooth

#~ subprocess.call(['sudo', 'hciconfig', 'hci0', 'up'])

#~ p = subprocess.Popen(['sudo', 'hciconfig', 'hci0', 'name'], stdout=subprocess.PIPE)
#~ result = p.communicate()
#~ splitted = result[0].split('\n\t')

#~ matching = [s for s in splitted if "Name" in s]
#~ name = None
#~ if matching is not None:
	#~ matchingstr = ''.join(matching)
	#~ idxstartname = matchingstr.find('\'')
	#~ idxendname = matchingstr.find('\'', idxstartname)
	#~ name = matchingstr[idxstartname + 1 : idxstartname+idxendname + 1]
	#~ if name != 'indoor':
		#~ subprocess.call(['sudo', 'hciconfig', 'hci0', 'name', 'indoor'])


#~ subprocess.call(['sudo', 'rfcomm', 'listen', addr])
#~ subprocess.call(['sudo', 'rfcomm', 'bind', '0', addr])
#~ subprocess.call(['sudo', 'sdptool', 'add', 'SP'])
#~ subprocess.call(['sudo', 'rfcomm', 'watch', '0', '1']) 

#~ subprocess.call(['sudo', 'hciconfig', 'hci0', 'noscan'])
#~ subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
#~ subprocess.call(['sudo', 'hciconfig', 'hci0', 'leadv', '0'])
import subprocess
from bluetooth import *

subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

addr = 'B8:27:EB:E5:C6:EA'
subprocess.call(['sudo', 'rfcomm', 'bind', '0', addr])
subprocess.call(['sudo', 'sdptool', 'add', 'SP'])
#~ subprocess.call(['sdptool', 'setseq', '0x10011', '0x0001', 'u0x1124'])
subprocess.call(['sudo', 'hciconfig', 'hci0', 'leadv', '0'])

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
                 
print("Waiting for connection on RFCOMM channel %d" % port)



client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        if len(data) == 0: break
        print("received [%s]" % data)
except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")
