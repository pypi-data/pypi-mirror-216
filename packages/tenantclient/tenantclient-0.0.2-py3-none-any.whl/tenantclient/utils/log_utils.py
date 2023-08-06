from datetime import datetime


class LogUtils(object):

	@classmethod
	def log(cls, logger, message):
		logger('at:{}'.format(datetime.utcnow()))
		logger(message)
