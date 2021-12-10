import os

# TO BE DEPERCATED
# This class is a wrapper for the autoit scripts for HAP42

def start_HAP():
    os.system("autoit3 .\main.au3 " + '"startHAP"' + ' "hello!"' + ' "testing"')

def create_space():
    return