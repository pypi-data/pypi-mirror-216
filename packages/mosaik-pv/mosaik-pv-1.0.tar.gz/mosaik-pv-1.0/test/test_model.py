import arrow

from mosaik_pv import pvpanel


def round_decimal(value, position):
    new_val = value * (10**position)
    new_val = float(int(new_val))
    return new_val / (10**position)


DATEFORMAT = 'YYYY-MM-DD HH:mm:ss'

start_date = '2014-01-12 15:00:00'
datefile = 'datefile.csv'
latitude = 32.2
area = 1
efficiency = 0.2
el_tilt = 32
az_tilt = 0

pv = pvpanel.PVpanel(datefile, latitude, start_date, area=area,
                     efficiency=efficiency, el_tilt=el_tilt, az_tilt=az_tilt)

# check time parameters after init:
assert pv.mosaik_time == 0
assert pv.darrow == arrow.get(start_date, DATEFORMAT)
date_dict = {'day': 12, 'hour': 15, 'minute': 0}
shared_items = set(pv.date.items()) & set(date_dict.items())
assert len(shared_items) == 3

# declination at 12th day of the year:
decl = pv.declination()
assert round_decimal(decl, 5) == -0.37962

# sun angle at 15th hour of the day:
ha = pv.hour_angle()
assert round_decimal(ha, 5) == 0.78539

# sun elevation at 12th day and 15th hour:
el = pv.elevation()
assert round_decimal(el, 5) == 0.36642

az = pv.azimuth()
assert round_decimal(az, 5) == 0.78025

ia = pv.incidence_angle()
assert round_decimal(ia, 5) == 0.85599

rn = pv.radiation_normal(100)
assert round_decimal(rn, 5) == 65.54660

# output power at 12th day and 15th hour:
p_out = pv.power(100)
assert round_decimal(p_out, 5) == 13.10932
# updated time parameters:
assert pv.mosaik_time == 3600
assert pv.darrow == arrow.get('2014-01-12 16:00:00', DATEFORMAT)
date_dict = {'day': 12, 'hour': 16, 'minute': 0}
shared_items = set(pv.date.items()) & set(date_dict.items())
assert len(shared_items) == 3
