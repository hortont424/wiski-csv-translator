class CR10X(object):
    def __init__(self):
        super(CR10X, self).__init__()

    def process(self, data):
        new_data = []
        
        for row in data:
            new_row = self.process_row(row)
            
            if new_row:
                new_data.append(new_row)
            
        return new_data
    
    def process_row(self, row):
        if row[0] == "9":
            return row
