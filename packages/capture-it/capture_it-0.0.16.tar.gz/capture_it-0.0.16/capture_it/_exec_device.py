# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from time import sleep
from nettoolkit import STR, IP
from .common import visual_print
from ._detection import DeviceType
from ._conn import conn
from ._captures import Captures

# -----------------------------------------------------------------------------
# Execution of Show Commands on a single device. 
# -----------------------------------------------------------------------------

class Execute_Device():
	"""Execute a device capture

	Args:
		ip (str): device ip
		auth (dict): authentication parameters
		cmds (list, set, tuple): set of commands to be executed.
		path (str): path where output to be stored
		cumulative (bool, optional): True,False,both. Defaults to False.
		forced_login (bool): True will try login even if device ping fails.
		parsed_output (bool): parse output and generate Excel or not.
		visual_progress (int): scale 0 to 10. 0 being no output, 10 all.
		logger(list): device logging messages list
	"""    	

	def __init__(self, 
		ip, 
		auth, 
		cmds, 
		path, 
		cumulative, 
		forced_login, 
		parsed_output,
		visual_progress,
		logger,
		):
		"""initialize execution

		Args:
			ip (str): device ip
			auth (dict): authentication parameters
			cmds (list, set, tuple): set of commands to be executed.
			path (str): path where output to be stored
			cumulative (bool): True,False,'both'.
			forced_login (bool): True will try login even if device ping fails.
			parsed_output (bool): parse output and generate Excel or not.
			visual_progress (int): scale 0 to 10. 0 being no output, 10 all.
			logger(list): device logging messages list
		"""    		
		self.log_key = ip
		self.auth = auth
		self.cmds = cmds
		self.path = path
		self.cumulative = cumulative
		self.cumulative_filename = None
		self.forced_login = forced_login
		self.parsed_output = parsed_output
		self.visual_progress = visual_progress
		self.delay_factor, self.dev = None, None
		#
		logger.add_host(self.log_key)
		self.logger_list = logger.log[self.log_key]
		#
		pinging = self.check_ping(ip)
		if forced_login or pinging:
			self.get_device_type(ip)
			try:
				self.dev.dtype
				execute = True
			except:
				execute = False
				msg_level, msg = 0, f"{ip} - DeviceType not detected"
				visual_print(msg, msg_level, self.visual_progress, self.logger_list)

			if execute and self.dev is not None and self.dev.dtype == 'cisco_ios': 
				try:
					self.execute(ip)
				except:
					msg_level, msg = 10, f"{ip} - sleeping progress for 65 seconds due to known cisco ios bug"
					visual_print(msg, msg_level, self.visual_progress, self.logger_list)
					
					sleep(65)
					self.execute(ip)
			elif execute:
				self.execute(ip)
			else:
				msg_level, msg = 0, f"{ip} - skipping device since unable to get device type"
				visual_print(msg, msg_level, self.visual_progress, self.logger_list)



	def check_ping(self, ip):
		"""check device reachability

		Args:
			ip (str): device ip

		Returns:
			int: delay factor if device reachable,  else False
		"""    		
		try:
			msg_level, msg = 8, f"{ip} - Checking ping response"
			visual_print(msg, msg_level, self.visual_progress, self.logger_list)

			self.delay_factor = IP.ping_average (ip)/100 + 3
			msg_level, msg = 8, f"{ip} - Delay Factor={self.delay_factor}"
			visual_print(msg, msg_level, self.visual_progress, self.logger_list)

			return self.delay_factor
		except:
			msg_level, msg = 10, f"{ip} - Ping was unsuccessful"
			visual_print(msg, msg_level, self.visual_progress, self.logger_list)

			return False

	def get_device_type(self, ip):
		"""detect device type (cisco, juniper)

		Args:
			ip (str): device ip

		Returns:
			str: device type if detected, else None
		"""    		
		try:
			self.dev = DeviceType(dev_ip=ip, 
				un=self.auth['un'], 
				pw=self.auth['pw'],
				visual_progress=self.visual_progress,
				logger_list=self.logger_list,
			)
			return self.dev
		except Exception as e:
			msg_level, msg = 0, f"{ip} - Device Type Detection Failed with Exception \n{e}"
			visual_print(msg, msg_level, self.visual_progress, self.logger_list)

			return None

	def is_connected(self, c, ip):
		"""check if connection is successful

		Args:
			c (conn): connection object
			ip(str): ip address of connection

		Returns:
			conn: connection object if successful, otherwise None
		"""    		
		connection = True
		if STR.found(str(c), "FAILURE"): connection = None
		if c.hn == None or c.hn == 'dummy': connection = None
		if connection is None:
			msg_level, msg = 0, f"{ip} - Connection establishment failed"
		else:
			msg_level, msg = 0, f"{ip} - Connection establishment success"
		visual_print(msg, msg_level, self.visual_progress, self.logger_list)

		return connection

	def execute(self, ip):
		"""login to given device(ip) using authentication parameters from uservar (u).
		if success start command captuers

		Args:
			ip (str): device ip
		"""    		
		msg_level, msg = 8, f"{ip} - Initializing"
		visual_print(msg, msg_level, self.visual_progress, self.logger_list)

		with conn(	ip=ip, 
					un=self.auth['un'], 
					pw=self.auth['pw'], 
					en=self.auth['en'], 
					delay_factor=self.delay_factor,
					visual_progress=self.visual_progress,
					logger_list=self.logger_list,
					devtype=self.dev.dtype,
					) as c:
			if self.is_connected(c, ip):
				msg_level, msg = 10, f"Connection established : {ip} == {c.hn}"
				visual_print(msg, msg_level, self.visual_progress, self.logger_list)

				cc = self.command_capture(c)
				self.cumulative_filename = cc.cumulative_filename
				if self.parsed_output: 
					xl_file = cc.write_facts()

	def command_capture(self, c):
		"""start command captures on connection object

		Args:
			c (conn): connection object
		"""    		
		msg_level, msg = 8, f"{c.hn} - Starting Capture"
		visual_print(msg, msg_level, self.visual_progress, self.logger_list)

		cc = Captures(dtype=self.dev.dtype, 
			conn=c, 
			cmds=self.cmds, 
			path=self.path, 
			visual_progress=self.visual_progress,
			logger_list=self.logger_list,
			cumulative=self.cumulative,
			parsed_output=self.parsed_output
			)
		return cc
