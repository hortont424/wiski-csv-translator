class Passthrough(object):
    def __init__(self):
        super(Passthrough, self).__init__()

    def process(self, data):
        """Given a two dimensional array of data, return a new,
        filtered two-dimensional array of data."""
        new_data = []

        for row in data:
            new_row = self.process_row(row)
            
            # Only re-add the row if process_row returns *something*
            if new_row:
                new_data.append(new_row)
            
        return new_data
    
    def process_row(self, row):
        """Given a single row of data, translate it into the new format.
        Return None if the row should be dropped in the output table."""
        
        return row