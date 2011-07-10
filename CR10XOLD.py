import datetime
import re

def convert_number(num):
    """Convert any number into floating point with six figures"""
    if not num:
        return "%0.6f" % 0.0
    return "%0.6f" % float(num)

class CR10XOLD(object):
    def __init__(self):
        super(CR10XOLD, self).__init__()

    def process(self, data):
        """Given a two dimensional array of data, return a new,
        filtered two-dimensional array of data."""
        new_data = []

        for index, row in enumerate(data):
            if row:
                new_row = self.process_row(row, index)

            # Only re-add the row if process_row returns *something*
            if new_row:
                new_data.append(new_row)

        return new_data

    def process_row(self, row, index):
        """Given a single row of data, translate it into the new format.
        Return None if the row should be dropped in the output table."""
        # If we run into a "9" record, emit a new WISKI record
        data = {}

        if not row[0].isdigit():
            return None

        try:
            # Decompose record into individual values
            # Use 0.0 as the default value if a column is missing
            remaining_fields = ["site", "date", "time", "air_temp_avg",
                                "rel_humid_max", "rel_humid_min", "avg_rad_avg", "avg_par_avg",
                                "wind_spd_wvc1", "wind_spd_wvc2", "wind_spd_wvc3", "inten_tot",
                                "snow_depth"]
            for remaining_value in row:
                field_name = remaining_fields.pop(0)
                data[field_name] = remaining_value
            for field_name in remaining_fields:
                data[field_name] = "0.0"
                print "Row {0} missing column {1}... filling in 0!".format(index, field_name)
        except:
            print "    Failed to parse row, throwing it away:\n    {0}".format(",".join(row))
            return None

        try:
            # Convert date into WISKI format
            dt = datetime.datetime.strptime(data["date"], "%d%b%Y")
            date_string = dt.strftime("%m/%d/%y")
            day_of_year = dt.strftime("%j")
        except:
            print "    There's something wrong with the row's date format, throwing it away: \n    {0}".format(",".join(row))
            return None

        # Emit new row, in WISKI format
        return ["DATA", "", "", "", "G9", "S14",
                date_string,
                data["time"] + ":00",
                convert_number(data["site"]),
                convert_number(day_of_year),
                convert_number(0.0),
                convert_number(data["air_temp_avg"]),
                convert_number(data["rel_humid_max"]),
                convert_number(data["rel_humid_min"]),
                convert_number(data["avg_rad_avg"]),
                convert_number(data["avg_par_avg"]),
                convert_number(data["wind_spd_wvc1"]),
                convert_number(data["wind_spd_wvc2"]),
                convert_number(data["wind_spd_wvc3"]),
                convert_number(data["inten_tot"]),
                convert_number(data["snow_depth"])]
