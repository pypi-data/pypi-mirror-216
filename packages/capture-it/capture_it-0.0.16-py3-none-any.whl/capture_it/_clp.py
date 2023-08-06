# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import pandas as pd
from .common import visual_print
from ._command import COMMAND

# -----------------------------------------------------------------------------
# Execution of Show Commands on a single device. 
# -----------------------------------------------------------------------------

class CLP():
	"""parent class for Command processing

	Args:
		dtype (str): device type
		conn (conn): connection object
		path (str): path to store the captured output	
		parsed_output(bool): Need to parse output and generate excel or not.
		visual_progress (int): scale 0 to 10. 0 being no output, 10 all.
		logger(list): device logging messages list
	"""    	
	def __init__(self, dtype, conn, path, parsed_output, visual_progress, logger_list):
		"""Initialize object

		Args:
			dtype (str): device type
			conn (conn): connection object
			path (str): path to store the captured output	
			parsed_output(bool): Need to parse output and generate excel or not.
			visual_progress (int): scale 0 to 10. 0 being no output, 10 all.
			logger(list): device logging messages list
		"""    		
		self.dtype = dtype
		self.conn = conn
		self.path = path
		self.parsed_output = parsed_output
		self.visual_progress = visual_progress
		self.logger_list = logger_list
		self.cumulative_filename = None
		self.parsed_cmd_df = {}
		self.cmd_exec_logs = []
		self.hn = self.conn.hn
		self.ip = self.conn.devvar['ip']
		self.configure(False)						# fixed disable as now

	def configure(self, config_mode=False):
		"""set configuration mode

		Args:
			config_mode (bool, optional): enable/disable config commands. Defaults to False.
		"""    		
		self._configure = config_mode

	def check_config_authorization(self, cmd):
		"""check if given command is allowed or not on this device.

		Args:
			cmd (str): command to be executed

		Returns:
			bool: True/False
		"""    		
		if not self._configure and 'config' == cmd.lstrip()[:6].lower():
			msg_level, msg = 0, f"{self.hn} - Config Mode disabled, Exiting"
			visual_print(msg, msg_level, self.visual_progress, self.logger_list)
			return False
		return True

	def cmd_capture(self, cmd, cumulative=False, banner=False):
		"""start command capture for given command

		Args:
			cmd (str): command to be executed
			cumulative (bool, optional): True/False/both. Defaults to False.
			banner (bool, optional): set a banner property to object if given. Defaults to False.

		Returns:
			[type]: [description]
		"""    		
		self.cmd_exec_logs.append({'command':cmd})
		cmdObj = self._cmd_capture_raw(cmd, cumulative, banner)
		if cmdObj is not None:
			self._cmd_capture_parsed(cmd, cumulative, banner)
		return cmdObj

	# Raw Command Capture
	def _cmd_capture_raw(self, cmd, cumulative=False, banner=False):
		try:
			cmdObj = COMMAND(conn=self.conn, cmd=cmd, path=self.path, parsed_output=False, 
				visual_progress=self.visual_progress, logger_list=self.logger_list)
		except:
			msg_level, msg = 2, f"{self.hn} - Error executing command {cmd}"
			visual_print(msg, msg_level, self.visual_progress, self.logger_list)
			self.cmd_exec_logs[-1]['raw'] = False
			return None
		try:
			cmdObj.banner = banner		
			file = cmdObj.op_to_file(cumulative=cumulative)
			self.cmd_exec_logs[-1]['raw'] = True
			if self.cumulative_filename is None:
				self.cumulative_filename = cmdObj.cumulative_filename
			return cmdObj
		except:
			msg_level, msg = 2, (f"{self.hn} : Error writing output for command {cmd}\n",
								f"{cmdObj.output}\n",
								f"{self.cmd_exec_logs}")
			visual_print(msg, msg_level, self.visual_progress, self.logger_list)
			self.cmd_exec_logs[-1]['raw'] = False
			return False

	# Parsed Command Capture
	def _cmd_capture_parsed(self, cmd, cumulative=False, banner=False):
		try:
			cmdObj_parsed = COMMAND(conn=self.conn, cmd=cmd, path=self.path, parsed_output=True, 
				visual_progress=self.visual_progress, logger_list=self.logger_list)
		except:
			msg_level, msg = 2, f"{self.hn} - Error executing command - Parse Run {cmd}"
			visual_print(msg, msg_level, self.visual_progress, self.logger_list)
			self.cmd_exec_logs[-1]['parsed'] = False
			return None
		try:
			self.parsed_cmd_df[cmd] = pd.DataFrame(cmdObj_parsed.output)
			self.cmd_exec_logs[-1]['parsed'] = True
		except:
			msg_level, msg = 2, (f"{self.hn} : No ntc-template parser available for the output of command {cmd}, "
								f"data facts will not be available for this command")
			visual_print(msg, msg_level, self.visual_progress, self.logger_list)
			self.cmd_exec_logs[-1]['parsed'] = False
			return False


