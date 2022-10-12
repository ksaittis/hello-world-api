import json

from python.src.models.birthdate import Birthdate
from python.src.models.username import Username


class EventParsingError(Exception):
    """Raised when unable to parse event data"""
    pass


class User:

    def __init__(self, username: str, date_of_birth: str = None):
        self.username = Username(username)
        self.birthdate = None
        if date_of_birth is not None:
            self.birthdate = Birthdate(date_of_birth)

    def set_birthdate(self, date_of_birth: str) -> None:
        self.birthdate = Birthdate(date_of_birth)

    def is_valid(self) -> bool:
        return self.is_username_valid() and self.is_birthdate_valid()

    def is_username_valid(self) -> bool:
        return self.username.is_valid()

    def is_birthdate_valid(self) -> bool:
        if self.birthdate is None:
            return False
        return self.birthdate.is_valid()

    def get_greeting(self) -> str:
        if self.birthdate.is_today():
            return f"Hello {self.username.value}! Happy birthday!"

        days_until_next_birthday = self.birthdate.get_days_until_next_birthday()
        return f"Hello {self.username.value}! Your birthday is in {days_until_next_birthday} day(s)!"

    @classmethod
    def from_event(cls, event):
        try:
            username = event['pathParameters']['username']
            if event['body'] is not None and 'dateOfBirth' in json.loads(event['body']):
                return cls(username=username,
                           date_of_birth=json.loads(event['body'])['dateOfBirth'])

            return cls(username=username)
        except Exception:
            raise EventParsingError
