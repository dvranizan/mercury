import string
import random
import os
import logging

box = ()
base_file_path = ""
base_http_path = ""
app = None

def set_base_file_path(s):
    global base_file_path
    base_file_path = s

def set_base_http_path(s):
    global base_http_path
    base_http_path = s

def get_http_path(s):
    global base_http_path
    logging.debug("Using "+base_http_path)
    ret = base_http_path
    ret += '/'
    ret += os.path.basename(s)
    return ret

def get_file_path():
    global base_file_path
    random_name = ''
    while True:
        random_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
        random_name += ".png"
        if not os.path.isfile(base_file_path+'/'+random_name):
            break
        
    return base_file_path+'/'+random_name
