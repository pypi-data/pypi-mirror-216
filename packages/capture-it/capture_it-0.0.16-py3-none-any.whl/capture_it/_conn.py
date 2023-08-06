# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from netmiko import ConnectHandler
import traceback
from nettoolkit import STR, LOG
from .common import visual_print
from ._detection import DeviceType

# -----------------------------------------------------------------------------

BAD_CONNECTION_MSG = ': BAD CONNECTION DETECTED, TEARED DOWN'
cisco_banner ="""
! ---------------------------------------------------------------------------- !
! This output is generated using capture_it utility.
! Script written by : Aliasgar Hozaifa Lokhandwala (aholo2000@gmail.com)
! Write an email if any errors found.
! ---------------------------------------------------------------------------- !
"""
juniper_banner = """
# ---------------------------------------------------------------------------- #
# This output is generated using capture_it utility.
# Script written by : Aliasgar Hozaifa Lokhandwala (aholo2000@gmail.com)
# Write an email if any errors found.
# ---------------------------------------------------------------------------- #
"""

# -----------------------------------------------------------------------------
# connection Object (2nd Connection)
# -----------------------------------------------------------------------------

class conn(object):
	"""Initiate an active connection.  
	use it with context manager to execute necessary commands on to it.

	Args:
		ip (str): ip address of device to establish ssh connection with
		un (str): username to login to device
		pw (str): user password to login to device
		en (str): enable password (For cisco)
		delay_factor (int): connection stability factor
		visual_progress (int): scale 0 to 10. 0 being no output, 10 all.
		logger(list): device logging messages list
		devtype (str, optional): device type from DeviceType class. Defaults to ''.
		hostname (str, optional): hostname of device ( if known ). Defaults to ''.

	Properties:
		hn (str): hostname
		devvar (dict) : {'ip':ip, 'host':hostname}
		devtype (str) : device type ('cisco_ios', 'arista_eos', 'juniper_junos')
	"""    	
	# Connection Initializer
	def __init__(self, 
		ip, 
		un, 
		pw, 
		en, 
		delay_factor, 
		visual_progress,
		logger_list,
		devtype='', 
		hostname='', 
		):
		"""initiate a connection object

			Args:
			ip (str): ip address of device to establish ssh connection with
			un (str): username to login to device
			pw (str): user password to login to device
			en (str): enable password (For cisco)
			delay_factor (int): connection stability factor
			visual_progress (int): scale 0 to 10. 0 being no output, 10 all.
			logger(list): device logging messages list
			devtype (str, optional): device type from DeviceType class. Defaults to ''.
			hostname (str, optional): hostname of device ( if known ). Defaults to ''.
		"""	
		self.logger_list = logger_list
		self.conn_time_stamp = LOG.time_stamp()
		self._devtype = devtype 						# eg. cisco_ios
		self._devvar = {'ip': ip, 'host': hostname }	# device variables
		self.visual_progress = visual_progress
		self.__set_local_var(un, pw, en)				# setting 
		self.banner = juniper_banner if self.devtype == 'juniper_junos' else cisco_banner
		self.delay_factor = delay_factor
		self.clsString = f'Device Connection: {self.devtype}/{self._devvar["ip"]}/{self._devvar["host"]}'
		self.__connect
		self.devvar = self._devvar

	# context load
	def __enter__(self):
		if self.connectionsuccess:
			self.__set_hostname
			self.clsString = f'Device Connection: {self.devtype}/{self._devvar["ip"]}/{self._devvar["host"]}'
			msg_level, msg = 10, f"{self._devvar['ip']} - conn - enter - {self.clsString}"
			visual_print(msg, msg_level, self.visual_progress, self.logger_list)
		return self      # ip connection object

	# cotext end
	def __exit__(self, exc_type, exc_value, tb):
		msg_level, msg = 10, f"{self._devvar['ip']} - conn - terminate - {self.clsString}"
		visual_print(msg, msg_level, self.visual_progress, self.logger_list)
		self.__terminate
		if exc_type is not None:
			traceback.print_exception(exc_type, exc_value, tb)

	# representation of connection
	def __repr__(self):
		return self.clsString

	@property
	def clsStr(self):
		return self.clsString
	@clsStr.setter
	def clsStr(self, s):
		self.clsString = s

	# RETURN --- > DEVICETYPE
	@property
	def devtype(self):
		"""device type
		* 'cisco': 'cisco_ios',
		* 'arista': 'arista_eos',
		* 'juniper': 'juniper_junos'

		Returns:
			str: device type
		"""    
		return self._devtype

	# RETURN --- > DEVICE HOSTNAME
	@property
	def hn(self):
		"""device hostname

		Returns:
			str: device hostname
		"""    
		return self._devvar['host']

	# set connection var|properties
	def __set_local_var(self, un, pw, en):
		'''Inherit User Variables'''
		msg_level, msg = 10, f"{self._devvar['ip']} - conn - setting up auth parameters"
		visual_print(msg, msg_level, self.visual_progress, self.logger_list)
		self._devvar['username'] = un
		self._devvar['password'] = pw
		self._devvar['secret'] = en
		if self._devtype == '':
			self._devtype = DeviceType(self._devvar['ip'], 
				self._devvar['username'], self._devvar['password'],
				self.visual_progress, self.logger_list,
				).device_type 
		self._devvar['device_type'] = self._devtype

	# establish connection
	@property
	def __connect(self):
		msg_level, msg = 10, f"{self._devvar['ip']} - conn - start ConnectHandler"
		visual_print(msg, msg_level, self.visual_progress, self.logger_list)
		try:
			self.net_connect = ConnectHandler(**self._devvar) 
			self.connectionsuccess = True			
		except:
			self.connectionsuccess = False

		if self.connectionsuccess:
			self._devvar['host'] = STR.hostname(self.net_connect)
			self._hn = self._devvar['host']
			if any( [
				self._devvar['device_type'].lower() == 'cisco_ios'
				] ):
				for tries in range(3):
					try:
						self.net_connect.enable(cmd="enable")
						break
					except:
						print(f"{self._devvar['host']} - enable failed on attemp {tries}")
						continue

	# set connection hostname property
	@property
	def __set_hostname(self):
		self._devvar['host'] = STR.hostname(self.net_connect)

	# terminate/disconnect session
	@property
	def __terminate(self):
		try:
			self.net_connect.disconnect()
		except:
			pass


