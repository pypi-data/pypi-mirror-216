#!/usr/bin/env python3

# Copyright (c) 2020-2022 NCC Group,
#               2023 Jeff Dileo.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# $ pandoc -t json blog.md | python3 path/to/this/repo/pandoc.py html | pandoc -f json -t html -o blog.html
# $ bloggerer -o blog.html blog.md

import sys
import argparse
import os
import os.path
import io
import subprocess
from .pf import entrypoint

def parse_args():
  parser = argparse.ArgumentParser(
    description='Transforms markdown (and probably other things too) into ' +
                'WordPress-compatible "Custom HTML" with pandoc and ' +
                'additional magic.'
  )
  parser.add_argument('-o', '--output', metavar='<output>', type=str,
                      default="",
                      help='Output path. Defaults to <inpath>.<outformat>')
  parser.add_argument('-f', '--outformat', metavar='<outformat>', type=str,
                      default="html",
                      help='Output format.')
  parser.add_argument('path', metavar='<path>', type=str,
                      help='Input path to convert.')
  args = parser.parse_args()
  if args.output == "":
    args.output = args.path + "." + args.outformat
  return args

def main():
  bn = os.environ.get("__BLOGGERER_NESTED")
  if bn is None:
    # top level call
    args = parse_args()

    # call pandoc to get json ast
    proc1 = subprocess.run(['pandoc', '-t', 'json', args.path], capture_output=True)
    if proc1.returncode != 0:
      sys.stderr.write("error running initial pandoc command: \n")
      sys.stderr.buffer.write(proc1.stderr)
      sys.stderr.write("\n")
      sys.exit(1)
    o1 = proc1.stdout.decode('utf-8')

    # move to input file's dir for relative access
    dir, fname = os.path.split(args.path)
    wd = os.getcwd()
    os.chdir(dir)

    # run the panflute filter
    sys.argv = [args.outformat]
    iw = io.StringIO(o1)
    ow = io.StringIO("")
    r = entrypoint(iw, ow)
    ow.seek(0)
    o2 = ow.read()

    # pass back to pandoc
    os.chdir(wd)
    proc2 = subprocess.run(['pandoc', '-f', 'json',
                            '-t', args.outformat,
                            '--wrap=none',
                            '-o', args.output],
                           input=o2, text=True,
                           capture_output=True)
    if proc2.returncode != 0:
      sys.stderr.write("error running initial pandoc command: \n")
      sys.stderr.write(proc2.stderr)
      sys.stderr.write("\n")
      sys.exit(1)
    sys.stdout.write(proc2.stdout)

  else:
    # call into panflute handler directly for testing
    entrypoint()

if __name__ == "__main__":
  main()
