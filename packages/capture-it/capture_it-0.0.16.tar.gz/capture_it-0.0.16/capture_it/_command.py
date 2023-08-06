# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from nettoolkit import STR, IO
from .common import visual_print

# -----------------------------------------------------------------------------
# Command Execution on a conn(connection) object, store to file
# -----------------------------------------------------------------------------

class COMMAND():
	"""CAPTURE OUTPUT FOR GIVEN COMMAND - RETURN CONTROL/OUTPUT 

	Args:
		conn (conn): connection object
		cmd (str): a command to be executed
		path (str): path where output to be stored
		parsed_output(bool): Need to parse output and generate excel or not.
		visual_progress (int): scale 0 to 10. 0 being no output, 10 all.
		logger(list): device logging messages list


	Properties:
		cmd (str): command executed
		commandOP, output (str) - command output
		fname (filename): full filename with path where output stored
	"""    	

	# INITIALIZE class vars
	def __init__(self, conn, cmd, path, parsed_output, visual_progress, logger_list):
		"""initialize a command object

		Args:
			conn (conn): connection object
			cmd (str): a command to be executed
			path (str): path where output to be stored
			parsed_output(bool): Need to parse output and generate excel or not.
			visual_progress (int): scale 0 to 10. 0 being no output, 10 all.
			logger(list): device logging messages list
		"""    		
		self.conn = conn
		self.cmd = cmd
		self.path = path
		self.parsed_output = parsed_output
		self.visual_progress = visual_progress
		self.logger_list = logger_list
		self._commandOP(conn)


	def op_to_file(self, cumulative=False):
		"""store output of command to file, cumulative (True,False,both) to store output in a single file, individual files, both

		Args:
			cumulative (bool, optional): True,False,both. Defaults to False.

		Returns:
			str: file name where output get stored
		"""    		
		if cumulative:
			self.cumulative_filename = self.add_to_file(self.commandOP)    # add to file
			self.fname = self.cumulative_filename
			msg_level, msg = 3, f"{self.conn.hn} : {self.cmd} >> {self.fname}"
			visual_print(msg, msg_level, self.visual_progress, self.logger_list)
		else:
			self.fname = self.send_to_file(self.commandOP)    # save to file
			msg_level, msg = 3, f"{self.conn.hn} : {self.cmd} >> {self.fname}"
			visual_print(msg, msg_level, self.visual_progress, self.logger_list)
		if isinstance(cumulative, str) and cumulative=='both':
			self.fname = self.send_to_file(self.commandOP)    # save to file
		return self.fname

	# Representation of Command object
	def __repr__(self):
		return f'object: Output for \n{self.conn} \ncommand: {self.cmd}'

	# RETURNS ---> Command output
	@property
	def commandOP(self):
		'''command output'''
		return self.output

	# capture output from connection
	def _commandOP(self, conn):
		self.output = ''

		op = self.conn.net_connect.send_command(self.cmd, 
				read_timeout=20, 
				delay_factor=self.conn.delay_factor,
				use_textfsm=self.parsed_output,
				)

		# exclude missed ones
		if any([								
			STR.found(op,'Connection refused')
			]):                                 ### ADD More as needed ###
			msg_level, msg = 0, f"{self.conn.hn} : Connection was refused by remote host.."
			visual_print(msg, msg_level, self.visual_progress, self.logger_list)
			return None

		self.output = op

	# send output to textfile
	def send_to_file(self, output):
		"""send output to a text file

		Args:
			output (str): captured output

		Returns:
			str: filename where output got stored
		"""    		
		fname = STR.get_logfile_name(self.path, hn=self.conn.hn, cmd=self.cmd, ts=self.conn.conn_time_stamp)
		msg_level, msg = 3, f"{self.conn.hn} : sending output to file, {fname}"
		visual_print(msg, msg_level, self.visual_progress, self.logger_list)

		IO.to_file(filename=fname, matter=output)
		return fname

	# send output to textfile
	def add_to_file(self, output):
		"""add output to a text file

		Args:
			output (str): captured output

		Returns:
			str: filename where output got appended
		"""    		
		banner = self.banner if self.banner else ""
		rem = "#" if self.conn.devtype == 'juniper_junos' else "!"
		cmd_header = f"\n{rem}{'='*80}\n{rem} output for command: {self.cmd}\n{rem}{'='*80}\n\n"
		fname = STR.get_logfile_name(self.path, hn=self.conn.hn, cmd="", ts=self.conn.conn_time_stamp)
		msg_level, msg = 3, f"{self.conn.hn} : adding output to a file {fname}"
		visual_print(msg, msg_level, self.visual_progress, self.logger_list)

		IO.add_to_file(filename=fname, matter=banner+cmd_header+output)
		return fname
