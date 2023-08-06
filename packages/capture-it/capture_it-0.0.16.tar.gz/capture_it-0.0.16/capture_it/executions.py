# -----------------------------------------------------------------------------
import os
from nettoolkit import Validation, STR, Multi_Execution, addressing, IPv4
from pprint import pprint

from ._exec_device import Execute_Device
from .common import visual_print, Log, write_log

# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
# COMMON methods and variables defining class
# -----------------------------------------------------------------------------------------------
class Execute_Common():
	"""common methods/variables declaration in a Execute Common class
	"""	

	def __init__(self, 
		cumulative, 
		forced_login, 
		parsed_output,
		visual_progress,
		log_type,
		common_log_file,
		):
		"""Initiatlize the connections for the provided iplist, authenticate with provided auth parameters, and execute given commands.

		Args:
			cumulative (bool, optional): True: will store all commands output in a single file, 
				False will store each command output in differet file. Defaults to False.
				and 'both' will do both.
			forced_login (bool, optional): True: will try to ssh/login to devices even if ping respince fails.
				False will try to ssh/login only if ping responce was success. (default: False)
			parsed_output (bool, optional): True: will check the captures and generate the general parsed excel file.
				False will omit this step. No excel will be generated in the case. (default: False)
			visual_progress (int, optional): 0 will not show any progress, 10 will show all progress (default=3).
			log_type (str): what type of log output requires. choices are = common, individual, both
			common_log_file (str): output file name of a common log file

		Raises:
			Exception: raise exception if any issue with authentication or connections.
		"""    		
		self.cumulative = cumulative
		self.forced_login = forced_login
		self.parsed_output = parsed_output
		self.visual_progress = visual_progress
		self.log_type = log_type
		self.common_log_file = common_log_file
		#
		self.verifications()
		self.lg = Log()
		#

	def verifications(self):
		"""Verification/Validation of input values
		"""
		if not isinstance(self.visual_progress, (int, float)):
			print(f"visual_progress level to be entered in number, default value (3) selected")
			self.visual_progress = 3
		if self.parsed_output and not self.cumulative :
			self.cumulative='both'
		if self.log_type in ('common', 'both') and not self.common_log_file:
			print( f"common_log_file is missing, debug log will not be generated" )
			self.common_log_file = None

	def validate_max_connection_input(self, concurrent_connections):
		"""check validate and update maximum concurrent connections value for execution
		if error in input, default 100 will be selected.

		Args:
			concurrent_connections (int): number of max concurrent connections can be establish
		"""		

		try:
			self.max_connections = concurrent_connections
		except:
			msg_level, msg = 0, f"Invalid number of `concurrent_connections` defined {concurrent_connections}, default 100 taken."
			visual_print(msg, msg_level, self.visual_progress)

	def is_valid(self, ip):
		"""Validation function to check if provided ip is valid IPv4 or IPv6 address

		Args:
			ip (str): ipv4 or ipv6 address

		Returns:
			bool: True/False based on validation success/fail
		"""    		
		try:
			return ip and Validation(ip).version in (4, 6)
		except:
			msg_level, msg = 0, f'Device Connection: {ip} :: Skipped due to bad Input'
			visual_print(msg, msg_level, self.visual_progress)
			return False
		return True

# -----------------------------------------------------------------------------------------------
# Execute class - capture_it - for common commands to all devices
# -----------------------------------------------------------------------------------------------

class Execute_By_Login(Multi_Execution, Execute_Common):
	"""Execute the device capture by logging in to device.

	"""    	

	def __init__(self, 
		ip_list, 
		auth, 
		cmds, 
		path, 
		cumulative=False, 
		forced_login=False, 
		parsed_output=False,
		visual_progress=3,
		log_type=None,   #  options = 'common', individual', 'both', None
		common_log_file=None,  # provide if log_type = common
		concurrent_connections=100,
		):
		"""Initiatlize the connections for the provided iplist, authenticate with provided auth parameters, and execute given commands.

		Args:
			ip_list (set, list, tuple): set of ip addresses to be logging for capture
			auth (dict): authentication parameters ( un, pw, en)
			cmds (set, list, tuple): set of commands to be captured
			path (str): path where output(s), logs(s) should be stored.
			cumulative (bool, optional): True: will store all commands output in a single file, 
				False will store each command output in differet file. Defaults to False.
				and 'both' will do both.
			forced_login (bool, optional): True: will try to ssh/login to devices even if ping respince fails.
				False will try to ssh/login only if ping responce was success. (default: False)
			parsed_output (bool, optional): True: will check the captures and generate the general parsed excel file.
				False will omit this step. No excel will be generated in the case. (default: False)
			visual_progress (int, optional): 0 will not show any progress, 10 will show all progress (default=3).
			log_type (str): what type of log output requires. choices are = common, individual, both
			common_log_file (str): output file name of a common log file
			concurrent_connections (int, optional): 100: manipulate how many max number of concurrent connections to be establish.
				default is 100.

		Raises:
			Exception: raise exception if any issue with authentication or connections.
		"""    		
		self.devices = STR.to_set(ip_list) if isinstance(ip_list, str) else set(ip_list)
		self.auth = auth
		if not isinstance(cmds, dict):
			raise Exception("commands to be executed are to be in proper dict format")
		self.cmds = cmds
		self.path = path
		Execute_Common.__init__(self, cumulative, forced_login, parsed_output, visual_progress, log_type, common_log_file)
		super().__init__(self.devices)
		self.validate_max_connection_input(concurrent_connections)
		self.start()
		# self.end()
		write_log(self.lg, log_type, common_log_file, self.path)



	def execute(self, hn):
		"""execution function for a single device. hn == ip address in this case.

		Args:
			hn (str): ip address of a reachable device
		"""    		
		Execute_Device(hn, 
			auth=self.auth, 
			cmds=self.cmds, 
			path=self.path, 
			cumulative=self.cumulative,
			forced_login=self.forced_login, 
			parsed_output=self.parsed_output,
			visual_progress=self.visual_progress,
			logger=self.lg,
			)
		if self.log_type and self.log_type.lower() in ('individual', 'both'):
			self.lg.write_individuals(self.path)





# -----------------------------------------------------------------------------------------------
# Execute class - capture_it - for selected individual commands for each device(s)
# -----------------------------------------------------------------------------------------------
class Execute_By_Individual_Commands(Multi_Execution, Execute_Common):
	"""Execute the device capture by logging in to device and running individual commands on to it.

	"""    	

	def __init__(self, 
		auth, 
		dev_cmd_dict,
		op_path='.', 
		cumulative=False, 
		forced_login=False, 
		parsed_output=False,
		visual_progress=3,
		log_type=None,         #  options = 'common', individual', 'both', None
		common_log_file=None,  #  provide if log_type = common
		concurrent_connections=100,
		):
		"""Initiatlize the connections for the provided iplist, authenticate with provided auth parameters, and execute given commands.

		Args:
			auth (dict): authentication parameters ( un, pw, en)
			dev_cmd_dict: dictionary of list {device_ip:[commands list,]}
			op_path (str): path where output(s), logs(s) should be stored.
			cumulative (bool, optional): True: will store all commands output in a single file, 
				False will store each command output in differet file. Defaults to False.
				and 'both' will do both.
			forced_login (bool, optional): True: will try to ssh/login to devices even if ping respince fails.
				False will try to ssh/login only if ping responce was success. (default: False)
			parsed_output (bool, optional): True: will check the captures and generate the general parsed excel file.
				False will omit this step. No excel will be generated in the case. (default: False)
			visual_progress (int, optional): 0 will not show any progress, 10 will show all progress (default=3).
			log_type (str): what type of log output requires. choices are = common, individual, both
			common_log_file (str): output file name of a common log file
			concurrent_connections (int, optional): 100: manipulate how many max number of concurrent connections to be establish.
				default is 100.

		Raises:
			Exception: raise exception if any issue with authentication or connections.
		"""
		#
		self.add_auth_para(auth)
		self.verify_dev_cmd_dict(dev_cmd_dict)
		self.add_devices(dev_cmd_dict)
		self.individual_device_cmds_dict(dev_cmd_dict)
		self.path = op_path
		Execute_Common.__init__(self, cumulative, forced_login, parsed_output, visual_progress, log_type, common_log_file)
		super().__init__(self.devices)
		self.validate_max_connection_input(concurrent_connections)
		self.start()
		# self.end()
		#
		write_log(self.lg, log_type, common_log_file, self.path)


	def add_auth_para(self, auth):
		"""add authentication parameters to self instance
		
		Args:
			auth (dict): authentication parameters

		Returns:
			None
		"""
		if not isinstance(auth, dict):
			raise Exception(f"authentication parameters needs to be passed as dictionary")
		if not auth.get('un') or auth['un'] == '':
			raise Exception(f"authentication parameters missing with username `un`")
		if not auth.get('pw') or auth['pw'] == '':
			raise Exception(f"authentication parameters missing with password `pw`")
		if not auth.get('en') or auth['en'] == '':
			auth['en'] = auth['pw']
		self.auth = auth

	def verify_dev_cmd_dict(self, dev_cmd_dict):
		"""Verify device commands dictionary `dev_cmd_dict` format and values. and raises Exceptions for errors.
		dev_cmd_dict dictionary keys are to be from either of non-iterable type such as (string, tuple, set).
		dev_cmd_dict dictionary values are to be from either of iterable type such as (list, set, tuple, dict).

		Args:
			dev_cmd_dict (dict): device commands dictionary

		Returns:
			None
		"""
		if not isinstance(dev_cmd_dict, dict):
			raise Exception(f"`capture_individual` requires `dev_cmd_dict` parameter in dictionary format")
		for ip, cmds in dev_cmd_dict.items():
			if isinstance(ip, (tuple, set)):
				for x in ip:
					if not isinstance(addressing(x), IPv4):
						raise Exception(f"`dev_cmd_dict` key expecting IPv4 address, received {ip}")
			elif isinstance(ip, str) and not isinstance(addressing(ip), IPv4):
				raise Exception(f"`dev_cmd_dict` key expecting IPv4 address, received {ip}")
			if not isinstance(cmds, (list, set, tuple, dict)):
				raise Exception(f"`dev_cmd_dict` values expecting iterable, received {cmds}")

	def add_devices(self, dev_cmd_dict):
		"""check device commands dictionary and returns set of devices

		Args:
			dev_cmd_dict (dict): device commands dictionary

		Returns:
			None
		"""
		devs = set()
		for ip, cmds in dev_cmd_dict.items():
			if isinstance(ip, (tuple, set)):
				for x in ip:
					devs.add(x)
			elif isinstance(ip, str):
				devs.add(ip)
		self.devices = devs

	def is_valid(self, ip):
		"""Validation function to check if provided ip is valid IPv4 or IPv6 address

		Args:
			ip (str): ipv4 or ipv6 address

		Returns:
			bool: True/False based on validation success/fail
		"""    		
		try:
			return ip and Validation(ip).version in (4, 6)
		except:
			msg_level, msg = 0, f'Device Connection: {ip} :: Skipped due to bad Input'
			visual_print(msg, msg_level, self.visual_progress)
			return False
		return True

	def execute(self, ip):
		"""execution function for a single device. hn == ip address in this case.

		Args:
			ip (str): ip address of a reachable device
		"""
		Execute_Device(ip, 
			auth=self.auth, 
			cmds=sorted(self.dev_cmd_dict[ip]), 
			path=self.path, 
			cumulative=self.cumulative,
			forced_login=self.forced_login, 
			parsed_output=self.parsed_output,
			visual_progress=self.visual_progress,
			logger=self.lg,
			)
		if self.log_type and self.log_type.lower() in ('individual', 'both'):
			self.lg.write_individuals(self.path)


	def individual_device_cmds_dict(self, dev_cmd_dict):
		"""check device commands dictionary and sets commands list for each of device

		Args:
			dev_cmd_dict (dict): device commands dictionary

		Returns:
			None
		"""
		self.dev_cmd_dict = {}
		for device in self.devices:
			if not self.dev_cmd_dict.get(device):
				self.dev_cmd_dict[device] = set()
			for ips, cmds in dev_cmd_dict.items():
				if isinstance(ips, (tuple, set, list)):
					for ip in ips:
						if device == ip:
							self.add_to(ip, cmds)
				if isinstance(ips, str):
					if device == ips:
						self.add_to(ips, cmds)


	def add_to(self, ip, cmds):
		"""adds `cmds` to the set of commands for given ip in device commands dictionary 

		Args:
			ip (str): ip address of device
			cmds (set): set of commands to be added for ip

		Returns:
			None
		"""
		cmds = set(cmds)
		self.dev_cmd_dict[ip] = self.dev_cmd_dict[ip].union(cmds)

# -----------------------------------------------------------------------------------------------
