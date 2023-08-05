# pvpanel.py is an adaption of PyPVSim by Daniel Soto licensed under CC-BY 3.0
# (https://github.com/dsoto/PyPVSim/blob/master/LICENSE.txt).

from numpy import sin, cos, tan, arcsin, arccos, arctan2, nan, pi, isnan
from scipy import radians


class PVpanel:

    def __init__(self, lat, area=1, efficiency=0.2,
                 el_tilt=0, az_tilt=0):
        self.area = area
        self.efficiency = efficiency
        self.el_tilt = radians(el_tilt)
        self.az_tilt = radians(az_tilt)
        self.lat = radians(lat)
        self.date = None

    def power(self, dni, datedict):
        '''Calculate the PV panels active power output based on the
        irradiation input and current time.'''
        self.date = datedict
        p = self.area * self.efficiency * self.radiation_normal(dni)
        return p

    def radiation_normal(self, dni):
        '''Calculate the normal radiation needed for the power calculation.'''
        ang = self.incidence_angle()
        if isnan(ang):
            return 0
        else:
            rn = dni * cos(self.incidence_angle())
            return max(0, rn)

    def incidence_angle(self):
        el = self.elevation()
        az = self.azimuth()
        ang = arccos(cos(el) * cos(az - self.az_tilt) * sin(self.el_tilt)
                     + sin(el) * cos(self.el_tilt))
        return float(ang) # conversion from numpy float

    def elevation(self):
        '''Calculate the sun's elevation at current time.'''
        dec = self.declination()
        ha = self.hour_angle()
        arg = cos(self.lat) * cos(dec) * cos(ha) + sin(self.lat) * sin(dec)
        el = arcsin(arg)
        if arg > 0:
            return el
        else:
            return nan

    def azimuth(self):
        dec = self.declination()
        ha = self.hour_angle()
        el = self.elevation()
        # Formula from "Fundamentals of Renewable Energy Processes" (da Rosa)
        az = arctan2(sin(ha), sin(self.lat)*cos(ha) - cos(self.lat)
                     *tan(dec))
        if isnan(el):
            return nan
        else:
            return az

    def hour_angle(self):
        arg = self.date['hour'] + self.date['minute'] / 60.0
        return radians(15 * (arg-12))

    def declination(self):
        arg = 23.45 * sin(2 * pi * (self.date['day'] - 81) / 365.0)
        return radians(arg)
