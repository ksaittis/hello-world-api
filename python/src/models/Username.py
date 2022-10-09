from dataclasses import dataclass


@dataclass
class Username:
    value: str

    def is_valid(self) -> bool:
        """
        Returns true if username contains only letters
        """
        if not isinstance(self.value, str) or not self.value.isalpha():
            return False
        return True
