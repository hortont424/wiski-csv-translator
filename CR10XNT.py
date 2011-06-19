import datetime

def convert_date(day_of_year, year):
    """Convert from day-of-year and year to MM/DD/YY."""
    year_date = datetime.datetime(int(year), 1, 1)
    day_delta = datetime.timedelta(int(day_of_year) - 1)
    return (year_date + day_delta).strftime("%m/%d/%y")

def convert_number(num):
    """Convert any number into floating point with six figures"""
    return "%0.6f" % float(num)

class CR10XNT(object):
    def __init__(self):
        super(CR10XNT, self).__init__()

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
        if row[0] == "110":
            data = {}

            try:
                # Decompose record into individual values
                # Use 0.0 as the default value if a column is missing
                remaining_fields = ["row_type", "site", "year", "day_of_year",
                                    "time", "battery", "cr10xtemp", "air_temp",
                                    "max_rh", "min_rh", "solar", "par",
                                    "ws", "wdir", "sigthet", "precip", "snow", "quality"]
                for remaining_value in row:
                    field_name = remaining_fields.pop(0)
                    data[field_name] = remaining_value
                for field_name in remaining_fields:
                    data[field_name] = "0.0"
                    print "Row {0} missing column {1}... filling in 0!".format(index, field_name)
            except:
                print "    Failed to parse row, throwing it away:\n    {0}".format(",".join(row))
                return None

            # Convert date into WISKI format
            date_string = convert_date(data["day_of_year"], data["year"])

            # Emit new row, in WISKI format
            return ["DATA", "", "", "", "G9", "S14",
                    date_string,
                    data["time"],
                    "0",
                    convert_number(data["day_of_year"]),
                    convert_number(data["battery"]),
                    convert_number(data["air_temp"]),
                    convert_number(data["max_rh"]),
                    convert_number(data["min_rh"]),
                    convert_number(data["solar"]),
                    convert_number(data["par"]),
                    convert_number(data["ws"]),
                    convert_number(data["wdir"]),
                    convert_number(data["sigthet"]),
                    convert_number(data["precip"]),
                    convert_number(data["snow"]),
                    convert_number(data["quality"])]
