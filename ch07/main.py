#!/usr/bin/env python3

# Converts VM files to Hack compatibale ASM files

import sys
import os
from writer import writer

if not sys.argv[1]:
    raise ValueError("Filename is required.")

source_file = sys.argv[1]
file_name = os.path.splitext(os.path.basename(source_file))[0]
asm = []

with open(source_file, 'r') as f:
    line_number = 0
    for line in f:
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
            asm.append(writer(command, parts, file_name, line_number))

with open(file_name + '.asm', 'w') as f:
    f.write(''.join(asm))


