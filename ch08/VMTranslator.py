#!/usr/bin/env python

# Converts VM files to Hack compatibale ASM files

import sys
import os
import itertools
from writer import ASMWriter

def main():
    if not sys.argv[1]:
        raise ValueError("Filename is required.")

    source_file = sys.argv[1]

    # If directory, open each File.vm
    is_directory = os.path.isdir(source_file)
    if is_directory:
        dir_name = os.path.splitext(os.path.basename(source_file))[0]
        # Name the file the directory_name.asm
        file_output = os.path.join(os.path.dirname(source_file), dir_name, dir_name + '.asm')

        if os.path.exists(file_output):
            os.remove(file_output)

        # Add startup code
        initVM(file_output);
        for root, directory, files in os.walk(dir_name):
            for f in files:
                if f.endswith('.vm'):
                    file_path = os.path.join(root, f)
                    file_name = os.path.splitext(os.path.basename(f))[0]
                    processVMFile(file_path, file_name, file_output)
    else:
        file_name = os.path.splitext(os.path.basename(source_file))[0]
        file_output = os.path.join(os.path.dirname(source_file), file_name + '.asm')

        if os.path.exists(file_output):
            os.remove(file_output)

        processVMFile(source_file, file_name, file_output)

def initVM(file_output):
    asmwriter = ASMWriter()
    asm = '\n'.join([
        "@256",
        "D=A",
        "@SP",
        "M=D",
    ]) + '\n'
    with open(file_output, 'a') as outfile:
        outfile.write(asm)
        outfile.write(asmwriter.vm_to_asm('call', ['Sys.init', '0'], 'init-code', 0))


def processVMFile(source_file, file_name, file_output):
    with open(source_file, 'r') as infile:
        with open(file_output, 'a') as outfile:
            asmwriter = ASMWriter()
            line_number = 0
            for line in infile:
                # Remove whitespace
                line = line.strip()
                line_number = line_number + 1
                # Ignore lines that are comments
                if line[:2].startswith('//'):
                    continue
                if line:
                    parts = line.split()
                    command = parts[0]
                    parts = parts[1:]
                    parts = [i for i in itertools.takewhile(lambda p: p != '//', parts)]
                    outfile.write(asmwriter.vm_to_asm(command, parts, file_name, line_number))



if __name__ == "__main__":
    main()
