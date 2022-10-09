import os
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional


@dataclass
class Birthdate:
    value: str
    date_format: str = os.getenv('DATE_FORMAT', default='%Y-%m-%d')

    def is_today(self) -> bool:
        """Returns true if day and month of date_of_birth matches today's day and month"""
        try:
            date_of_birth_converted = datetime.strptime(self.value, self.date_format)
            today = date.today()
            return today.month == date_of_birth_converted.month and today.day == date_of_birth_converted.day
        except ValueError:
            raise False

    def get_next_birthday(self) -> Optional[date]:
        """Returns next birthday date"""
        try:
            date_of_birth_converted = datetime.strptime(self.value, self.date_format).date()
            today = date.today()

            if today.month > date_of_birth_converted.month or (
                    date_of_birth_converted.month == today.month and today.day > date_of_birth_converted.day):
                return date_of_birth_converted.replace(year=today.year + 1)

            return date_of_birth_converted.replace(year=today.year)
        except ValueError:
            raise None

    def get_days_until_next_birthday(self) -> int:
        """Returns number of days until next birthday"""
        if self.is_today():
            return 0

        next_birthday_date = self.get_next_birthday()
        return (next_birthday_date - date.today()).days

    def is_valid(self) -> bool:
        """
        Returns true if date_of_birth is valid date format and is before today
        """
        try:
            date_of_birth_converted = datetime.strptime(self.value, self.date_format).date()
            return date_of_birth_converted < date.today()
        except ValueError:
            return False
