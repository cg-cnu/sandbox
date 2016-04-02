#!/usr/bin/python

###
# Create instance from object itself
# keep track of the objects 
###

class Maya(object):
	"""docstring for maya"""

	count = 0
	instances = []

	def __init__(self, ip, port):
		super(Maya, self).__init__()
		self.ip = ip
		self.port = port

	@classmethod
	def create(Maya, ip, port):
		maya = Maya(ip, port)
		Maya.instances.append(maya)
		Maya.count += 1
		return maya

	def getName(self):
		return "maya"

	def getIp(self):
		return self.ip

	def getPort(self):
		return self.port


class Houdini(object):
	"""docstring for Houdini"""

	def __init__(self, ip, port):
		super(Houdini, self).__init__()
		self.ip = ip
		self.port = port

	@classmethod
	def create(ip, port):
		return 

	@classmethod
	def getObjs():
		return Houdini()

	def getName(self):
		return "houdini"


### usage
#maya = Maya()
mayaInstance1 = Maya.create("localhost1", "1111")
print mayaInstance1.getName()
print mayaInstance1.getIp()
print mayaInstance1.getPort()

print Maya.count
print Maya.instances

mayaInstance2 = Maya.create("localhost2", "2222")
print mayaInstance2.getName()
print mayaInstance2.getIp()
print mayaInstance2.getPort()

print Maya.count
print Maya.instances

# houdini = Houdini()
# houdiniInstance1 = houdini.create()
# houdiniInstance2 = houdini.create()
