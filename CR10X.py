import datetime

def convert_time(short_form):
    """Convert from CR10X to WISKI time formats.
    For example, 359 becomes 03:59:00 AM"""
    minutes = short_form[-2:]
    hours = short_form[:-2]

    if hours == "": hours = 0

    return datetime.time(int(hours), int(minutes)).strftime("%H:%M:%S")

def convert_date(day_of_year, year):
    """Convert from day-of-year and year to MM/DD/YY."""
    year_date = datetime.datetime(int(year), 1, 1)
    day_delta = datetime.timedelta(int(day_of_year) - 1)
    return (year_date + day_delta).strftime("%m/%d/%y")

def convert_number(num):
    """Convert any number into floating point with six figures"""
    return "%0.6f" % float(num)

class CR10X(object):
    def __init__(self):
        super(CR10X, self).__init__()

    def process(self, data):
        """Given a two dimensional array of data, return a new,
        filtered two-dimensional array of data."""
        new_data = []

        # Grab the current year from the first "13" record
        self.current_year = [row[12] for row in data if row[0] == "13"][0]

        for index, row in enumerate(data):
            new_row = self.process_row(row, index)

            # Only re-add the row if process_row returns *something*
            if new_row:
                new_data.append(new_row)

        return new_data

    def process_row(self, row, index):
        """Given a single row of data, translate it into the new format.
        Return None if the row should be dropped in the output table."""
        # If we run into another "13" record, update the current year
        if row[0] == "13":
            self.current_year = row[12]
            return None

        # If we run into a "9" record, emit a new WISKI record
        if row[0] == "9":
            data = {}

            try:
                # Decompose record into individual values
                # Use 0.0 as the default value if a column is missing
                (row_type, day_of_year, timestamp) = row[:3]
                remaining_fields = ["id_num", "day_of_year2", "batt_volt_min", "air_temp_avg",
                                    "rel_humid_max", "rel_humid_min", "avg_rad_avg", "avg_par_avg",
                                    "wind_spd_wvc1", "wind_spd_wvc2", "wind_spd_wvc3", "inten_tot",
                                    "snow_depth", "quality"]
                for remaining_value in row[3:]:
                    field_name = remaining_fields.pop(0)
                    data[field_name] = remaining_value
                for field_name in remaining_fields:
                    data[field_name] = "0.0"
                    print "Row {0} missing column {1}... filling in 0!".format(index, field_name)
            except:
                print "    Failed to parse row, throwing it away:\n    {0}".format(",".join(row))
                return None

            # Convert time and date into WISKI formats
            time_string = convert_time(timestamp)
            date_string = convert_date(day_of_year, self.current_year)

            # Emit new row, in WISKI format
            return ["DATA", "", "", "", "G9", "S14",
                    date_string,
                    time_string,
                    convert_number(data["id_num"]),
                    convert_number(data["day_of_year2"]),
                    convert_number(data["batt_volt_min"]),
                    convert_number(data["air_temp_avg"]),
                    convert_number(data["rel_humid_max"]),
                    convert_number(data["rel_humid_min"]),
                    convert_number(data["avg_rad_avg"]),
                    convert_number(data["avg_par_avg"]),
                    convert_number(data["wind_spd_wvc1"]),
                    convert_number(data["wind_spd_wvc2"]),
                    convert_number(data["wind_spd_wvc3"]),
                    convert_number(data["inten_tot"]),
                    convert_number(data["snow_depth"]),
                    convert_number(data["quality"])]
