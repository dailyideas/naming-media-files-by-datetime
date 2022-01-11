import datetime, os, sys, time
import subprocess


def CallExternalProgramAndGetOutput(command:list):
    """ Retrieving the output of subprocess.call()
    
        References
        ---- ----
        1. https://stackoverflow.com/questions/2502833/store-output-of-subprocess-popen-call-in-a-string
    """
    resultBytes = subprocess.check_output(command)
    resultStr = resultBytes.decode("utf-8")
    return resultStr.rstrip("\r\n")
