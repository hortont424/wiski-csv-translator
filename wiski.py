#!/usr/bin/env python

import csv
import sys

def load_instructions():
    from CR10X import CR10X
    
    return [CR10X]

def apply_transforms(input_file, instruction_class):
    input_data = list(csv.reader(input_file))
    instructions = instruction_class()
    
    return instructions.process(input_data)

def main():
    if len(sys.argv) != 4:
        print "Usage: {0} INPUT_FILENAME INPUT_TYPE OUTPUT_FILENAME".format(sys.argv[0])
        return
    
    _, input_filename, input_type, output_filename = sys.argv
    
    try:
        input_file = open(input_filename, "rb")
    except IOError:
        print "Could not open input file {0}!".format(input_filename)
        return
    
    try:
        output_file = open(output_filename, "w+")
    except IOError:
        print "Could not open output file {0}!".format(output_filename)
        intput_file.close()
        return
    
    instruction_classes = load_instructions()
    instruction_class = None
    
    for c in instruction_classes:
        if input_type == c.__name__:
            instruction_class = c
    
    if instruction_class == None:
        print "Could not find loader for type '{0}'".format(input_type)
        input_file.close()
        output_file.close()
        return
    
    data = apply_transforms(input_file, instruction_class)
    
    output_writer = csv.writer(output_file)
    for row in data:
        output_writer.writerow(row)
    
    input_file.close()
    output_file.close()

if __name__ == '__main__':
    main()