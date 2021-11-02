from dotenv import load_dotenv
import os

from weather.model import MessageType

load_dotenv()

API_KEY = 'api-key'
DEFAULT_LOCATION = 'default-location'
DEFAULT_MESSAGE_TYPE = 'default-msg-type'

def get_config():
	return {
		API_KEY: os.getenv('API-KEY'),
		DEFAULT_LOCATION: os.getenv('DEFAULT-LOCATION'),
		DEFAULT_MESSAGE_TYPE: look_up_Enum(MessageType, os.getenv('DEFAULT-MESSAGE-TYPE'))
	}

def look_up_Enum(enumType, str_name):
	for enum in enumType:
		if str_name == enum.name:
			return enum
	return None