#!/usr/bin/env python

import csv
import sys
from cStringIO import StringIO

def load_instructions():
    from CR10X import CR10X
    from CR10XNT import CR10XNT
    from CR10XOLD import CR10XOLD
    from CR1000_1 import CR1000_1
    from CR1000_2 import CR1000_2
    from Passthrough import Passthrough
    return [CR10X, CR10XNT, CR10XOLD, CR1000_1, CR1000_2, Passthrough]

def main():
    # Make sure the user supplies three command line arguments
    if len(sys.argv) != 4:
        print "Usage: {0} INPUT_FILENAME INPUT_TYPE OUTPUT_FILENAME".format(sys.argv[0])
        return

    _, input_filename, input_type, output_filename = sys.argv

    # Attempt to open the input and output files
    try:
        input_file = open(input_filename, "rb")
    except IOError:
        print "Could not open input file {0}!".format(input_filename)
        return

    try:
        output_file = open(output_filename, "w+")
    except IOError:
        print "Could not open output file {0}!".format(output_filename)
        input_file.close()
        return

    # Load all conversion instruction modules
    instruction_classes = load_instructions()
    instruction_class = None

    # Find (case-insensitive) the module that
    # matches the INPUT_TYPE argument
    for c in instruction_classes:
        if input_type.lower() == c.__name__.lower():
            instruction_class = c

    # Complain if we don't have a match for INPUT_TYPE
    if instruction_class == None:
        print "Could not find loader for type '{0}'".format(input_type)
        print "Known loaders: {0}".format(", ".join([i.__name__ for i in instruction_classes]))
        input_file.close()
        output_file.close()
        return

    # Transorm the data!
    input_data = csv.reader(input_file)
    #print "Read {0} rows.".format(len(input_data))
    instructions = instruction_class()
    data = instructions.process(input_data)

    # Write the new data to a file, as a CSV
    output_string_buffer = StringIO()
    output_writer = csv.writer(output_string_buffer)
    row_count = 0
    output_writer.writerows(data)
    #print "Wrote {0} rows.".format(row_count)

    input_file.close()

    output_file.write(output_string_buffer.getvalue().replace("\r\r\n","\r\n"))
    output_file.close()

if __name__ == '__main__':
    main()