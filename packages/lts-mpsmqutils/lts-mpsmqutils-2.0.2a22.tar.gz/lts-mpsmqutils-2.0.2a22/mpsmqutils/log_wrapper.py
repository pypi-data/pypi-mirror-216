import os

class LogWrapper():
	def __init__(self):
		configured_log_level = os.getenv('APP_LOG_LEVEL', 'INFO')
		if configured_log_level == 'DEBUG':
			self.log_level = 0
		elif configured_log_level == 'INFO':
			self.log_level = 1
		elif configured_log_level == 'WARNING':
			self.log_level = 2
		elif configured_log_level == 'ERROR':
			self.log_level = 3
		else:
			# if configured wrong, we default to info
			print("log level configured incorrectly, defaulting to INFO")
			self.log_level = 1

	def debug(self, message):
		# We strip the default newline from the end of the print statements, because these logs will come through
		# the celery logger. Via that output method, the newline causes lots of empty lines in the logs.
		if self.log_level <= 0:
			print(message, end='', flush=True)

	def info(self, message):
		if self.log_level <= 1:
			print(message, end='', flush=True)

	def warning(self, message):
		if self.log_level <= 2:
			print(message, end='', flush=True)

	def error(self, message):
		if self.log_level <= 3:
			print(message, end='', flush=True)
