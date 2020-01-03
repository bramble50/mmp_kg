# -*- coding: utf-8 -*-
"""

"""
import logging
from subprocess import Popen, PIPE, STDOUT

def run_and_log_process(cmd):
    process = Popen(cmd, stdout=PIPE, stderr=STDOUT, universal_newlines=True)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc