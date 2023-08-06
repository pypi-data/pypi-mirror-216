"""
Absfuyu: Human
---
Human related stuff

Version: 1.0.0
Date updated: 19/04/2023 (dd/mm/yyyy)
"""


# Module level
###########################################################################
__all__ = [
    "Human", "Person"
]


# Library
###########################################################################
from datetime import datetime

try:
    from dateutil.relativedelta import relativedelta
except:
    import subprocess
    subprocess.run("pip install -U python-dateutil".split())

from absfuyu.calculation import add_to_one_digit
from absfuyu.fun import zodiac_sign


# Class
###########################################################################
class Human:
    """
    Basic human data

    Birthday in yyyy/mm/dd format
    """

    __MEASUREMENT = "m|kg" # Metric system
    __VERSION = {"major": 1, "minor": 0, "patch": 4} # Internal version class check

    def __init__(self,
                 first_name: str,
                 last_name: str = None,
                 birthday: str = None
        ) -> None:
        # Name
        self.first_name = first_name
        self.last_name = last_name
        self.name = f"{self.last_name}, {self.first_name}" if self.last_name is not None else self.first_name

        # Birthday
        self.birthday = birthday
        date_str = self.birthday
        if date_str is None:
            # date_str = "1970/01/01"
            self.birthday = datetime.now().date()
        else:
            for x in ["/", "-"]:
                date_str = date_str.replace(x, "/")
        # split = date_str.split("/")
            date = datetime.strptime(date_str, "%Y/%m/%d")
            self.birthday = date

        # Others
        self.gender: bool = None # True: Male; False: Female
        self.height: float = None # centimeter
        self.weight: float = None # kilogram
        self.blood_type: str = None # ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    
    def __str__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}({str(self.name)})"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        name = str(self.name)
        gender = "M" if self.is_male else "F"
        return f"{class_name}({name} ({self.age}|{gender}))"
    
    @classmethod
    def JohnDoe(cls):
        """Dummy Human for test"""
        temp = cls("John", "Doe", "1980/01/01")
        temp.update({"gender": True, "height": 180, "weight": 80, "blood_type": "O+"})
        return temp
    
    @property
    def is_male(self) -> bool:
        """
        True: Male; False: Female
        """
        return self.gender
    
    @property
    def age(self):
        """
        Calculate age based on birthday
        """
        if self.birthday is not None:
            now = datetime.now()
            # age = now - self.birthday
            try:
                rdelta = relativedelta(now, self.birthday)
            except:
                date_str = self.birthday
                if date_str is None:
                    self.birthday = datetime.now().date()
                else:
                    for x in ["/", "-"]:
                        date_str = date_str.replace(x, "/")
                    date = datetime.strptime(date_str, "%Y/%m/%d")
                    self.birthday = date
                rdelta = relativedelta(now, self.birthday)
            return round(rdelta.years + rdelta.months/12, 2)
        else:
            return None
    
    @property
    def is_adult(self):
        return self.age > 18
    
    @property
    def bmi(self):
        r"""
        Body Mass Index (kg/m^2)

        Formula: $\frac{weight (kg)}{height (m)^2}$

        - BMI < 18.5: Skinny
        - 18.5 < BMI < 25: normal
        - BMI > 30: Obesse
        """
        try:
            temp = self.height / 100
            bmi = self.weight / (temp * temp)
            return round(bmi, 2)
        except:
            return None
    
    # @property
    def dir_(self):
        """
        List property
        """
        return [x for x in self.__dir__() if not x.startswith("_")]
    
    def update(self, data: dict) -> None:
        """
        Update Human data
        """
        self.__dict__.update(data)
        # return self



class Person(Human):
    """
    More detail Human data
    """

    __VERSION = {"major": 1, "minor": 0, "patch": 1} # Internal version class check

    def __init__(self, first_name: str, last_name: str = None, birthday: str = None) -> None:
        super().__init__(first_name, last_name, birthday)
        self.address: str = None
        self.hometown: str = None
        self.email: str = None
        self.phone_number: str = None
        self.nationality = None
        self.likes: list = None
        self.hates: list = None
        self.education = None
        self.occupation: str = None
        self.personality = None
        self.note: str = None
    
    @property
    def zodiac_sign(self):
        try:
            return zodiac_sign(self.birthday.day, self.birthday.month)
        except:
            return None
    
    @property
    def zodiac_sign_13(self):
        try:
            return zodiac_sign(self.birthday.day, self.birthday.month, zodiac13=True)
        except:
            return None
    
    @property
    def numerology(self) -> int:
        temp = f"{self.birthday.year}{self.birthday.month}{self.birthday.day}"
        return add_to_one_digit(temp, master_number=True)


# Run
###########################################################################
if __name__ == "__main__":
    print(Person.JohnDoe().dir_())