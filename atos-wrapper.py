#!/usr/bin/env python

"""
  iOS crash symbolication utility
  usage: ./atos-wrapper.py {crashfile.crash}

  TODO:
    custom path to dSYM
    bundle id extraction
    extracting binaries from .dSYM.zip
    arch detection (?)
"""

import sys
import re
import subprocess

if __name__ == '__main__':

  stacktrace_entry_re = re.compile(r'(\d+)\s+(\S+)\s+(0x[0-9a-fA-F]+)\s+(\S+)\s+\+\s+([1-9]?[0-9]*)')

  for filename in sys.argv[1:]:
    with open(filename) as file:
      for line in file.readlines():
        print line.strip()
        
        match = stacktrace_entry_re.match(line)
        if match is not None:
          args = match.groups()
          mod = args[1]
          addr = args[2]
          base = args[3]

          try:
            cmdline = ['atos', '-arch', 'arm64', '-o', mod, '-l', base, addr]
            out = subprocess.check_output(cmdline, stderr=subprocess.STDOUT, universal_newlines=True)
            print out.strip()
          except subprocess.CalledProcessError:
            # this commonly indicates atos can't find some debug information (for system modules, e.g.)
            pass # don't print anything
          except OSError:
            print 'atos command is inaccessible!'
            sys.exit(1)
