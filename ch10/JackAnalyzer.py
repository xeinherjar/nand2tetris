#!/usr/bin/env python3

import sys
import os
from tokenizer import Tokenizer
from parser import Parser

def main():
    if not sys.argv[1]:
        raise ValueError("Filename is required.")

    source_file = sys.argv[1]

#    file_name = os.path.splitext(os.path.basename(source_file))[0]
#    file_output = os.path.join(os.path.dirname(source_file), file_name + '.xml')

#    if os.path.exists(file_output):
#        os.remove(file_output)

    tokenizer = Tokenizer()
    parser = Parser()
    tokens = tokenizer.process_file(source_file);
    parser.process_tokens(tokens)


if __name__ == "__main__":
    main()
