import socket
maya = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
maya.connect(('localhost', 54321))
import  sys

fileParam = str(sys.argv[1])

#command = '''import sys;\nif 'com' in sys.modules:reload(sys.modules['com']);\nelse:import com'''
filename = 'updateTexture'

#command = '''import sys;
#if'''+filename+''' in sys.modules:reload(sys.modules['com']);
#else:import com
#from com import test
#newtst = test()
#newtst.prnt()'''

command = '''import sys;
if "'''+filename+'''" in sys.modules:reload(sys.modules["'''+filename+'''"]);
else:import '''+filename+'''
from '''+filename+''' import texUpd
start = texUpd("'''+fileParam+'''")'''





maya.send(command)
data = maya.recv(1024)
maya.close()
print 'The Result is %s'%data


