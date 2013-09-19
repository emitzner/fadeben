"""
If there's games going on right now, lets try and see if they're over by grabbing the scores from NFL's site
"""
import sys
import datetime
import logging
import os
import urllib2
import pytz

from bs4 import BeautifulSoup

from fadeben.lib.script import bootstrap
from fadeben import api
from fadeben.lib import dt

from fadeben.model import Session, Team

from pylons import app_globals as g, url

log = logging.getLogger("fadeben.spread_scraper")

def run_it():
    print "Hi"
    log.debug("URL: {0}".format(url("homepage", qualified=True)))
    

if __name__ == '__main__':
    config_file = 'development.ini'
    
    proj_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    bootstrap(config_file, proj_dir)
    run_it()
