



# -----------------------------------------------------------------------------

def juniper_add_no_more(cmd):
	"""returns updated juniper command with proper full | no-more statement if missing or trunkated found.

	Args:
		cmd (str): juniper show command

	Returns:
		str: updated command with | no-more
	"""	
	spl = cmd.split("|")
	no_more_found = False
	for i, item in enumerate(spl):
		if i == 0: continue
		no_more_found = item.strip().startswith("n")
		if no_more_found:
			spl[i] = " no-more "
			break
	if not no_more_found:
		spl.append( " no-more ")
	ucmd = "|".join(spl)
	return ucmd

# -----------------------------------------------------------------------------------------

def visual_print(msg, msg_level, visual_progress, logger_list):
	"""Prints message on console based on input visual progress level.  If input visual progress level is greater or equal
	to msg_level then the message (msg) will be printed.

	Args:
		msg (str): message to be printed on console
		msg_level (int): static message level for the particular message
		visual_progress (int): visual progress level number
		logger(list): device logging messages list

	Returns:
		None

	"""
	logger_list.append(msg)
	if msg_level > visual_progress: return None
	print(msg)

# -----------------------------------------------------------------------------------------

class Log():
	"""Execution Debug Logging class
	"""	

	def __init__(self):
		"""initialize a Log object instance
		"""		
		self.log = {}

	def add_host(self, hostname):
		"""adds a device ip address (hostname) to Logging dictionary

		Args:
			hostname (str): device ip/hostname
		"""		
		if hostname:
			self.log[hostname] = []

	def add_log(self, hostname, msg):
		"""appends log message `msg` to given hostname/ip log list.

		Args:
			hostname (str): device ip/hostname
			msg (str): log message
		"""		
		if not self.log.get(hostname):
			self.add_host(hostname)
		if msg:
			self.log[hostname].append(msg)

	def get_log(self, hostname):
		"""retrive log for given ip/hostname 

		Args:
			hostname (str): device ip/hostname

		Returns:
			str: multiline host logging entries.
		"""		
		s = ""
		if self.log.get(hostname):
			for _ in self.log[hostname]:
				s += _ + "\n"
		return s

	def get_logs(self):
		"""retrive log for all hosts/ips

		Returns:
			str: multiline host logging entries.
		"""		
		s = ""
		for hostname in self.log.keys():
			s += self.get_log(hostname)
		return s

	def write_log(self, file):
		"""write out log for all devices to given file.

		Args:
			file (str): filename/with location to write log out to.
		"""		
		s = self.get_logs()
		with open(file, 'w') as f:
			f.write(s)

	def write_individuals(self, capture_folder):
		"""write out log for all devices to each individual files at given capture folder.

		Args:
			capture_folder (str): path / location to where all device log to be written.
		"""		
		for hostname in self.log.keys():
			s = self.get_log(hostname)
			with open(f'{capture_folder}/{hostname}-debug.log', 'w') as f:
				f.write(s)


def write_log(lg, log_type, common_log_file, capture_folder):
	"""writes Logger output to a text log file(s). 

		Args:
			lg (Log): Logger class from common module
			log_type (str): what type of log output requires. choices are = common, individual, both
			common_log_file (str): output file name of a common log file
			capture_folder (str): output capture folder where log(s) will also be generated.

		Returns:
			None
	"""
	if log_type and log_type.lower() in ('common', 'both') and common_log_file:
		lg.write_log(f'{capture_folder}/{common_log_file}')

