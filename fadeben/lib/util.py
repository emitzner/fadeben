import os
import logging
import string
import hashlib

log = logging.getLogger(__name__)

def create_random_string(length):
    chars = string.letters + string.digits
    
    rtn_str = u''
    while len(rtn_str) <= length:
        rtn_str += chars[ord(os.urandom(1)) % len(chars)]
        
    return unicode(rtn_str)

def get_random_number(minimum, maximum):
    num_range = range(minimum, maximum+1)

    return num_range[ord(os.urandom(1)) % len(num_range)]

def generate_password(password, salt):
    delim = "::"
    ss = hashlib.sha256()
    ss.update(salt)
    salt_sha = ss.hexdigest()
    m = hashlib.sha256()
    m.update(password)
    m.update(delim)
    m.update(salt_sha)
    password = m.hexdigest()
    return password

def irange(start, end):
    """Inclusive range."""
    return range(start, end+1)
