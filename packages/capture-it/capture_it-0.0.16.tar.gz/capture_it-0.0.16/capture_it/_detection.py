
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import paramiko
from time import sleep
from nettoolkit import STR
from .common import visual_print


# -----------------------------------------------------------------------------
# Device Type Detection (1st Connection)
# -----------------------------------------------------------------------------
class DeviceType():
	"""'Defines Device type ( 'cisco_ios', 'arista_eos', 'juniper_junos')

	Args:
		dev_ip (str): ip address of device
		un (str): username to login to device
		pw (str): password to login to device
		visual_progress (int): scale 0 to 10. 0 being no output, 10 all.
		logger(list): device logging messages list
	
	Properties:
		dtype (str): device type (default/or exception will return 'cisco_ios')
	"""    	

	# INITIALIZER - DEVICE TYPE
	def __init__(self, dev_ip, un, pw, visual_progress, logger_list):
		"""initialize object with given ip and credentials

		Args:
			dev_ip (str): ip address of device
			un (str): username to login to device
			pw (str): password to login to device
			visual_progress (int): scale 0 to 10. 0 being no output, 10 all.
			logger(list): device logging messages list

		"""    		
		'''class initializer'''
		self.dev_ip = dev_ip
		self.visual_progress = visual_progress
		self.logger_list = logger_list
		self.device_types = {'cisco': 'cisco_ios',
						'arista': 'arista_eos',
						'juniper': 'juniper_junos'}
		self.dtype = self.__device_make(dev_ip, un, pw)

	# device type
	@property
	def dtype(self):
		"""device type
		* 'cisco': 'cisco_ios',
		* 'arista': 'arista_eos',
		* 'juniper': 'juniper_junos'

		Returns:
			str: device type
		"""    		
		return self.device_type

	# set device type
	@dtype.setter
	def dtype(self, devtype='cisco'):
		self.device_type = self.device_types.get(devtype, 'cisco_ios')
		msg_level, msg = 9, f"{self.dev_ip} - Detected Device Type - {self.device_type}"
		visual_print(msg, msg_level, self.visual_progress, self.logger_list)		

		return self.device_type

	# device make retrival by login
	def __device_make(self, dev_ip, un, pw):
		with paramiko.SSHClient() as ssh:
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			try:
				ssh.connect(dev_ip, username=un, password=pw)
				msg_level, msg = 9, f"{dev_ip} - Device SSH Connection Success - using username {un}"
				visual_print(msg, msg_level, self.visual_progress, self.logger_list)		

			except (paramiko.SSHException, 
					paramiko.ssh_exception.AuthenticationException, 
					paramiko.AuthenticationException
					) as e:
				msg_level, msg = 5, f"{dev_ip} - Device SSH Connection Failure - using username {un}"
				visual_print(msg, msg_level, self.visual_progress, self.logger_list)		
				pass

			with ssh.invoke_shell() as remote_conn:
				remote_conn.send('\n')
				sleep(1)
				msg_level, msg = 9, f"{dev_ip} - Verifying show version output"
				visual_print(msg, msg_level, self.visual_progress, self.logger_list)		

				remote_conn.send('ter len 0 \nshow version\n')
				sleep(2)
				output = remote_conn.recv(5000000).decode('UTF-8').lower()
				msg_level, msg = 11, f"{dev_ip} - show version output - {output}"
				visual_print(msg, msg_level, self.visual_progress, self.logger_list)		

				for k, v in self.device_types.items():
					if STR.found(output, k): 
						msg_level, msg = 10, f"{dev_ip} - Returning - {k}"
						visual_print(msg, msg_level, self.visual_progress, self.logger_list)
						return k


