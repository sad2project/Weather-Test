from datetime import datetime, date, time
from dataclasses import dataclass
from enum import Enum


class MessageType(Enum):
	SMS = 0
	EMAIL = 1
	CALL = 2


RAIN_CODES = ['Drizzle', 'Rain', 'Thunderstorm']


class Weather:
	DEFAULT_MESSAGE_TYPE = None

	def __init__(self, dt: datetime, temp: float, condition: str):
		self.dt = dt
		self.temp = temp
		self.condition = condition

	def date(self) -> date:
		return self.dt.date()

	def time(self) -> time:
		return self.dt.time()

	def default_msg_type(self):
		if self.DEFAULT_MESSAGE_TYPE is None:  # lazily load the config to avoid circular import
			from weather.config import get_config, DEFAULT_MESSAGE_TYPE as default
			self.DEFAULT_MESSAGE_TYPE = get_config()[default]
		return self.DEFAULT_MESSAGE_TYPE

	def message_type(self) -> MessageType:
		if self.temp < 55.0 or self.condition in RAIN_CODES:
			return MessageType.CALL
		if self.temp > 75.0 and self.condition == 'Clear':
			return MessageType.SMS
		if 55.0 <= self.temp <= 75.0:
			return MessageType.EMAIL
		return self.default_msg_type()  # The specs don't specify what to do when it's hot, but not sunny or rainy

	def __eq__(self, other):
		return (
			self.dt == other.dt and
			self.temp == other.temp and
			self.condition == other.condition)

	def __hash__(self):
		return hash((self.dt, self.temp, self.condition))

	def __str__(self):
		return f'Weather({self.dt}, {self.temp}, {self.condition})'
