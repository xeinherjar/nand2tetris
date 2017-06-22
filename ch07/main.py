#!/usr/bin/env python

# Converts VM files to Hack compatibale ASM files

import sys
import os
from writer import ASMWriter

if not sys.argv[1]:
    raise ValueError("Filename is required.")

source_file = sys.argv[1]
file_name = os.path.splitext(os.path.basename(source_file))[0]

with open(source_file, 'r') as infile:
    with open(file_name + '.asm', 'w') as outfile:
        line_number = 0
        asmwriter = ASMWriter()
        for line in infile:
            # Remove whitespace
            line = line.strip()
            line_number = line_number + 1
            # Ignore lines that are comments
            if line[:2].startswith('//'):
                continue
            if line:
                parts = line.split(' ')
                command = parts[0]
                parts = parts[1:]
                outfile.write(asmwriter.vm_to_asm(command, parts, file_name, line_number))



