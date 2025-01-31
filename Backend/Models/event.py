class event:
    def __init__(self, apikey, latlong, radius, unit, locale, countrycode, local_start_date_time):
        self.apikey = apikey
        self.latlong = latlong
        self.radius = radius
        self.unit = unit
        self.locale = locale
        self.countrycode = countrycode
        self. local_start_date_time = local_start_date_time


    def fetch_info(self):
        """
        Vis adgang til informationer for det enkelte event. 

        Retunere 'event'
        """
        pass