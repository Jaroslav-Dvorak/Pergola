from datetime import datetime, timedelta


class Energy:
    def __init__(self, read_enery_func):
        self.read_energy = read_enery_func
        self.dayhours = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
        self.hours = self.populate_hours()
        self.days = []
        self.months = []

    @staticmethod
    def get_hours_date(dayhour):
        date_from = datetime.now().replace(hour=dayhour-1, minute=0, second=0, microsecond=0)
        if datetime.now().hour < 7:
            date_from = date_from - timedelta(days=1)
        date_to = date_from + timedelta(hours=1)
        return date_from, date_to

    def populate_hours(self):
        bar_production = {}
        for index, dayhour in enumerate(self.dayhours):
            if dayhour > datetime.now().hour:
                break
            index = len(self.dayhours)-index
            date_from, date_to = self.get_hours_date(dayhour)
            produced = self.read_energy(date_from, date_to)
            if not produced:
                produced = 0
            print(index, produced)
            bar_production[f"{index}"] = produced*1000
        return bar_production

    def get_hours(self):
        try:
            index = self.dayhours.index(datetime.now().hour)
        except ValueError:
            return self.hours
        index = len(self.dayhours)-index
        date_from, date_to = self.get_hours_date(datetime.now().hour)
        actual_bar = self.read_energy(date_from, date_to)
        self.hours[f"{index}"] = actual_bar*1000
        _ = [print(h) for h in self.hours]
        return self.hours

