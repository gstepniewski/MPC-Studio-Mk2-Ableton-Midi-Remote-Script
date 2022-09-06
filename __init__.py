### Script br Brandon Crowe
import Live
import logging

logger = logging.getLogger(__name__)


def create_instance(c_instance):
	
	major_version = Live.Application.get_application().get_major_version()
	if major_version == 10:
		from .v10.MPCStudioMk2 import MPCStudioMk2 as v10
		logger.info('=======================Load v10 of MPC Studio Mk2 Script===============================')
		return v10(c_instance)
	elif major_version == 11:
		from .v11.MPCStudioMk2 import MPCStudioMk2 as v11
		logger.info('=======================Load v11 of MPC Studio Mk2 Script===============================')
		return v11(c_instance)