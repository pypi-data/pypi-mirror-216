from mosaik_pv import mosaik

DF = 'datefile.csv'
LAT = 32.0
AREA = 1
EFF = 0.5
EL = 32.0
AZ = 0.0
SD = '2014-01-12 15:00:00'

def test_init_create():
    sim = mosaik.PvAdapter()
    meta = sim.init(0, gen_neg=True)
    assert meta['models']['PV']['params'] == [
        'datefile', 'lat', 'area', 'efficiency', 'el_tilt', 'az_tilt',
        'start_date']

    entities = sim.create(2, 'PV', datefile=DF, lat=LAT, area=AREA,
                          efficiency=EFF, el_tilt=EL, az_tilt=AZ, start_date=SD)
    print(entities)

test_init_create()
