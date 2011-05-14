#!/usr/bin/env python

import csv
import sys
import json

instruction_methods = {}
instruction_loaders = {}

def instruction_method(g):
    def wrap(cls):
        instruction_methods[g] = cls
        return cls
    return wrap

def instruction_loader(g):
    def wrap(cls):
        instruction_loaders[g] = cls
        return cls
    return wrap
    
@instruction_method("select")
def select_operation(row, context):
    column, func = context
    
    if func(row[column]):
        return row
    
    return None

@instruction_loader("select")
def select_loader(instruction_row):
    return (instruction_row["column"], lambda x : x == str(instruction_row["equals"]))

def load_instructions(instruction_file):
    instructions = []
    
    for instruction in json.loads(instruction_file.read()):
        method = instruction_methods[instruction["type"]]
        args = instruction_loaders[instruction["type"]](instruction)
        
        instructions.append((method, args))
    
    return instructions

def apply_transforms(input_file, instruction_file):
    input_reader = csv.reader(input_file)
    instructions = load_instructions(instruction_file)
    
    print instructions
    
    for row in input_reader:
        pass

def main():
    if len(sys.argv) != 3:
        print "Usage: {0} INPUT_FILENAME INSTRUCTION_FILENAME".format(sys.argv[0])
        return
    
    input_filename = sys.argv[1]
    instruction_filename = sys.argv[2]
    
    try:
        input_file = open(input_filename, "rb")
    except IOError:
        print "Could not open input file {0}!".format(input_filename)
    
    try:
        instruction_file = open(instruction_filename, "rb")
    except IOError:
        print "Could not open instruction file {0}!".format(instruction_filename)
    
    apply_transforms(input_file, instruction_file)

if __name__ == '__main__':
    main()