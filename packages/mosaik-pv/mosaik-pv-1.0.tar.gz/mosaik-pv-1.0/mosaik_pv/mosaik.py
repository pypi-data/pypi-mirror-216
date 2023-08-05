import itertools
import mosaik_api
import arrow

from mosaik_pv import pvpanel

meta = {
    'type': 'time-based',
    'models': {
        'PV': {
            'public': True,
            'params': [
                'lat',          # latitude of data measurement location [°]
                'area',         # area of panel [m2]
                'efficiency',   # panel efficiency
                'el_tilt',      # panel elevation tilt [°]
                'az_tilt',      # panel azimuth tilt [°]
            ],
            'attrs': ['P',      # output active power [W]
                      'DNI'],   # input direct normal insolation [W/m2]
        },
    },
}

DATE_FORMAT = 'YYYY-MM-DD HH:mm:ss'


class PvAdapter(mosaik_api.Simulator):
    def __init__(self):
        super(PvAdapter, self).__init__(meta)
        self.sid = None

        self.gen_neg = True     # true if generation is negative
        self.cache = None

        self._entities = {}
        self.eid_counters = {}

    def init(self, sid, time_resolution, datefile=None, start_date=None, gen_neg=True):
        self.sid = sid
        self.gen_neg = gen_neg

        self.year_start = None
        self.day_arrow = None
        self.datedata = open(datefile)
        self.date = None
        self.organize_date(start_date)
        self.step_size = 3600

        return self.meta

    def create(self, num, model, **model_params):
        counter = self.eid_counters.setdefault(model, itertools.count())

        entities = []

        # creation of the entities:
        for i in range(num):
            eid = '%s_%s' % (model, next(counter))

            self._entities[eid] = pvpanel.PVpanel(**model_params)

            entities.append({'eid': eid, 'type': model, 'rel': []})

        return entities

    def step(self, t, inputs, max_advance):
        self.cache = {}
        for eid, attrs in inputs.items():
            for attr, vals in attrs.items():
                if attr == 'DNI':
                    dni = list(vals.values())[0] # only one source expected
                    self.cache[eid] = self._entities[eid].power(dni, self.date)
                    if self.gen_neg:
                        self.cache[eid] *= (-1)

        self._read_next_row()
        return t + self.step_size

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            if eid not in self._entities.keys():
                raise ValueError('Unknown entity ID "%s"' % eid)

            data[eid] = {}
            for attr in attrs:
                if attr != 'P':
                    raise ValueError('Unknown output attribute "%s"' % attr)
                data[eid][attr] = self.cache[eid]

        return data

    def finalize(self):
        self.datedata.close()

    def organize_date(self, start_date):
        start_date = arrow.get(start_date, DATE_FORMAT)
        date_str = str(start_date.year) + '-01-01 00:00:00'
        self.year_start = arrow.get(date_str, DATE_FORMAT)
        row = next(self.datedata).strip().split(',')
        self.day_arrow = arrow.get(row[0], DATE_FORMAT)
        while self.day_arrow < start_date:
            row = next(self.datedata).strip().split(',')
            self.day_arrow = arrow.get(row[0], DATE_FORMAT)
        self.date = {'day': (self.day_arrow-self.year_start).days+1,
                     'hour': self.day_arrow.hour,
                     'minute': self.day_arrow.minute}

    def _read_next_row(self):
        try:
            row = next(self.datedata).strip().split(',')
            new_day_arrow = arrow.get(row[0], DATE_FORMAT)
            self.step_size = (new_day_arrow - self.day_arrow).seconds
            self.day_arrow = new_day_arrow

            self.date['day'] = (self.day_arrow-self.year_start).days+1
            self.date['hour'] = self.day_arrow.hour
            self.date['minute'] = self.day_arrow.minute
        except StopIteration:
            print("No new data available")


def main():
    mosaik_api.start_simulation(PvAdapter(), 'PV-Simulator')
