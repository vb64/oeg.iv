"""
Orientation object
"""
import math


class Error(Exception):
    """
    Orientation exception
    """
    pass


class Orientation(object):
    """
    orientation units conversions
    """
    def __init__(self, hours, minutes):

        if not(0 <= hours <= 12):
            raise Error("Wrong hours: {}. Must be 0-12".format(hours))

        if not(0 <= minutes <= 59):
            raise Error("Wrong minutes: {}. Must be 0-59".format(minutes))

        self.hours = hours
        self.minutes = minutes

    def __unicode__(self):
        hours = self.hours
        if hours == 0:
            hours = '12'

        minutes = self.minutes
        if minutes < 10:
            minutes = '0{}'.format(minutes)

        return "{},{}".format(hours, minutes)

    def __str__(self):
        return self.__unicode__()

    @classmethod
    def from_hour_float(cls, hour_float):
        """
        construct object from hours as float
        """
        parttial_hour, hours = math.modf(hour_float)
        minutes = parttial_hour * 60
        return cls(int(hours), int(minutes))


def from_infotech_html(text):
    """
    return orientation from infotech string
    """
    return Orientation.from_hour_float(float(text.replace(',', '.')))
