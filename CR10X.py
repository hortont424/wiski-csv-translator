import datetime

def convert_time(short_form):
    minutes = short_form[-2:]
    hours = short_form[:-2]
    
    if hours == "": hours = 0
    
    minutes = int(minutes)
    hours = int(hours)
    
    return datetime.time(hours, minutes).strftime("%I:%M:%S %p")

def convert_date(day_of_year, year):
    day_of_year = int(day_of_year)
    year = int(year)
    return (datetime.datetime(year, 1, 1) + datetime.timedelta(day_of_year - 1)).strftime("%m/%d/%y")

class CR10X(object):
    def __init__(self):
        super(CR10X, self).__init__()

    def process(self, data):
        """Given a two dimensional array of data, return a new,
        filtered two-dimensional array of data."""
        new_data = []
        
        # Grab the current year from the first "13" record
        self.current_year = [row[12] for row in data if row[0] == "13"][0]
        
        for row in data:
            new_row = self.process_row(row)
            
            # Only re-add the row if process_row returns *something*
            if new_row:
                new_data.append(new_row)
            
        return new_data
    
    def process_row(self, row):
        """Given a single row of data, translate it into the new format.
        Return None if the row should be dropped in the output table."""
        # If we run into another "13" record, update the current year
        if row[0] == "13":
            self.current_year = row[12]
        
        # If we run into a "9" record, emit a new WISKI record
        if row[0] == "9":
            (row_type, day_of_year, timestamp, id_num, day_of_year2,
             batt_volt_min, air_temp_avg, rel_humid_max, rel_humid_min,
             avg_rad_avg, avg_par_avg, wind_spd_wvc1, wind_spd_wvc2,
             wind_spd_wvc3, inten_tot, snow_depth, quality) = row
            
            time_string = convert_time(timestamp)
            date_string = convert_date(day_of_year, self.current_year)
            
            return ["DATA", "", "", "", "G9", "S14",
                    date_string, time_string, id_num, day_of_year,
                    batt_volt_min, air_temp_avg, rel_humid_max,
                    rel_humid_min, avg_rad_avg, avg_par_avg,
                    wind_spd_wvc1, wind_spd_wvc2, wind_spd_wvc3,
                    inten_tot, snow_depth, quality]
