### Script br Brandon Crowe
import Live
from .v10.MPCStudioMk2 import MPCStudioMk2 as v10
from .v11.MPCStudioMk2 import MPCStudioMk2 as v11
import logging
logger = logging.getLogger(__name__)



def create_instance(c_instance):
	
	major_version = Live.Application.get_application().get_major_version()
	if major_version == 10:
		logger.warn('=======================Load v10 of MPC Studio Mk2 Script===============================')
		return v10(c_instance)
	elif major_version == 11:
		logger.warn('=======================Load v11 of MPC Studio Mk2 Script===============================')
		return v11(c_instance)