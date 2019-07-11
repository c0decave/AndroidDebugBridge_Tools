#!/usr/bin/env python
# simple script for using adb server at port 5037
# missing still push,pull,uninstall,install ....
# by dash
# July 2019


# you need to:
# pip install pure-python-adb

import os
import sys
import cmd
import time
import argparse

from adb.client import Client as AdbClient


class adbShell(object):
	def __init__(self):
		host = None

	def connect(self,args):
		''' connect to remote tcp daemon'''
		print(args)

		ip,prt = args

		client = AdbClient(host=ip, port=prt)
		try:
			client.create_connection()
		except RuntimeError as e:
			print(e)
			return False
		
		return client

	def get_version(self,cl):
		''' get the version of the adb server '''
		return cl.version()

	def get_devices(self,cl):
		''' get connected devices '''
		devices = cl.devices()
		return devices
		
	def get_features(self,cl):
		''' get connected devices '''
		try:
			feat = cl.features()
		except RuntimeError as e:
			print('[-] Error in getting features: %s' % e)
			return False
		
		return feat

	def kill_adb_server(self,cl):
		''' this simply stops the adb server at remote side '''
		# kills the adb server
		ret=cl.kill()
		print(ret)

	def get_serial(self,dev):
		serial = dev.get_serial_no()
		return serial

	def get_state(self,dev):
		''' get the state'''
		state = dev.get_state()
		return state

	def list_features(self,dev):
		feat = dev.list_features()
		return feat
		
	def get_device_path(self,dev):
		result = dev.get_device_path()
		return result

	def list_forward(self,dev):
		result=dev.list_forward()
		return result

	def list_packages(self,dev):
		result = dev.list_packages()
		return result
		
	def list_reverses(self,dev): 
		result=dev.list_reverses()
		return result

	def adb_root(self,dev):
		try:
			result = dev.root()
		except RuntimeError as e:
			print(e)
			return e
		return result

	def remount_fs(self,dev):
		''' remount the FS as rw '''
		result = dev.remount()
		return result

	def shell_cmd(self,dev, cmd):
		''' run a shell command ''' 
		result = dev.shell(cmd)
		return result

	def screencap(self,dev):
		''' make a screenshot '''
		result = dev.screencap()
		return result

class adbCmd(cmd.Cmd,adbShell):

	devCmd = ['list_features','state','serial','screenshot','root','remount','shell_cmd','state','device_path','list_packages','list_forwards','list_reverses']
	prompt="adb> "
	intro = "Welcome to adb_shell"
	adbs = adbShell()
	client = None
	devices = []
	args = []
	dev = None


	def precmd(self, line):
		print ('precmd(%s)' % line)
		c = line.split(' ')[0]
		if self.devCmd.count(c) and self.dev == None:
			print('Sorry, cannot execute command without defining a device')
			return cmd.Cmd.precmd(self, '')

		return cmd.Cmd.precmd(self, line)


	def cmdloop(self,args, intro=None,):
		print ('cmdloop(%s)' % args)
		self.args = args
		if args.host:
			self._do_connect(args.host,args.prt)
		return cmd.Cmd.cmdloop(self, intro)

	def _do_connect(self,host,port):
		''' laber '''
		self.client=self.adbs.connect((host,port))

	def do_set_device(self,line):
		''' set the device, example set_device 0 '''
		dev = -1
		print(len(line))
		if len(line)==0 or line.isnumeric()==False:
			print('Sorry no device number given, example: set_device 0')
			return False

		nmb = int(line[0])
		print(nmb)
		
		self.do_devices(line)

		for dev in self.devices:
			print('Available: [%s](%s)' % (dev.serial,dev))

		if len(self.devices)<nmb:
			print('Sorry, device does not exist')
		else:
			self.dev = self.devices[nmb]

	def do_connect(self, line):
		l = line.split(' ')
		print(l)
		if len(l)==1 and l[0]!='':
			host = l[0]
			host = host.rstrip('\n')
			self.client=self.adbs.connect((host,5037))
		elif len(l)==2:
			host = l[0]
			host = host.rstrip('\n')
			port = int(l[1])
			self.client=self.adbs.connect((host,port))
		else:
			self.help_connect()
	
	def do_version(self,line):
		version = (self.adbs.get_version(self.client))
		print('[+] Version: %s' % version)

	def do_devices(self,line):
		devices = self.adbs.get_devices(self.client)
		self.devices = devices
		print(devices)
	
	def do_features (self,line):
		''' ac1d '''
		result = self.adbs.get_features(self.client)
		self.features = result
		print(result)

		return 

	def do_killadb (self,line):
		''' kills adb server remotely '''
		result = self.adbs.kill_adb_server(self.client)
		print(result)

		return 

	def do_serial (self,line):
		''' ac1d '''
		result = self.adbs.get_serial(self.dev)
		self.serial = result
		print(result)

		return 

	def do_state (self,line):
		''' ac1d '''
		result = self.adbs.get_state(self.dev)
		self.state = result
		print(result)

		return 

	def do_list_features (self,line):
		''' ac1d '''
		result = self.adbs.list_features(self.dev)
		self.lfeatures = result
		print(result)

		return 

	def do_device_path (self,line):
		''' solution=ac1d '''
		result = self.adbs.get_device_path(self.dev)
		self.dev_path = result
		print(result)
		return 

	def do_list_forwards(self,line):
		''' solution=ac1d '''
		result = self.adbs.list_forward(self.dev)
		self.forwards = result
		print(result)
		return 

	def do_list_packages(self,line):
		''' solution=ac1d '''
		result = self.adbs.list_packages(self.dev)
		self.packages = result
		print(result)
		return 

	def do_list_reverses(self,line):
		''' solution=ac1d '''
		result = self.adbs.list_reverses(self.dev)
		self.reverses = result
		print(result)
		return 

	def do_root(self,line):
		''' solution=ac1d '''
		result = self.adbs.adb_root(self.dev)
		#self.dev_path = result
		print(result)
		return 

	def do_remount(self,line):
		''' solution=ac1d '''
		result = self.adbs.remount_fs(self.dev)
		#self.dev_path = result
		print(result)
		return 

	def do_shell_cmd (self,line):
		''' solution=ac1d '''
		seperator = ''
		cmd = seperator.join(line)
		print(cmd)
 
		result = self.adbs.shell_cmd(self.dev,cmd)
		#self.dev_path = result
		print(result)

		return 

	def do_screenshot(self,line):
		''' solution=ac1d '''
		result = self.adbs.screencap(self.dev)
		self.screencap = result
		# TODO 
		# add better save function
		fname = 'screenshot_%d.png' % (int(time.time()))
		fw = open(fname,'wb')
		fw.write(result)
		fw.close()
		#print(result)

		return 

	def help_version(self):
		print('\n'.join([ 'version',
			'prints the version of the remote adb server',
					]))
		

	def help_connect(self):
		print('\n'.join([ 'connect <host> [port]',
			'connect to adb host, example: connect 127.0.0.1 5037',
					]))
	
	def do_exit(self,line):
		''' exit adb_shell'''
		sys.exit()	

	def do_EOF(self,line):
		print()
		print('Cya')
		return True
		

	
def run(args):
	''' horayy we got a runner .... '''

	# this will not be executed by now
	# focus is at shell functions 
	# see __main__ for more information what is happening
	cl = connect(args)
	print('Connected')
	print(get_version(cl))
	devices = get_devices(cl)
	#get_features(cl)
	for dev in devices:
		print('dev')
		res = shell_cmd(dev,'id')
		print(res)



def main():
	''' aha it is a main '''

	version = '0.1'
	parser_desc = 'adb server shell %s' % version
	prog_desc = 'adbs_shell.py'
	parser = argparse.ArgumentParser(prog = prog_desc, description=parser_desc)
	parser.add_argument("-l","--host",action="store",required=True,help='host to check',dest='host')
	parser.add_argument("-p","--port",action="store",required=False,default=5037,help='adb port (default:427)',dest='prt', type=int)
	parser.add_argument("-T","--timeout",action="store",required=False,default=5,help='timeout of socket recv',dest='timeout')
	parser.add_argument("-o","--outfile",action="store",required=False,help='outfile in txt format',dest='outfile')
	args = parser.parse_args()
	return(args)

if __name__ == "__main__":
	args=main()
	adbCmd().cmdloop(args)
