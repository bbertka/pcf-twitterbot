#!/usr/bin/python

from flask import Flask, request, redirect, url_for, send_from_directory
from collections import Counter
import json, os, logging
import cfworker

#---------------------------------------------------------------
#
# bubblestats: keeps track of the tag count in the bubble chart
#
#---------------------------------------------------------------
class bubblestats:
        def __init__(self):
                self.trend_raw = []
                self.trend_count = Counter()
        def update(self, trends=[]):
                # this keeps track of the size of the bubble chart
                if len(self.trend_raw) >= int( os.getenv('MAX_CHART_SIZE') ):
                        self.trend_raw = []
                        self.trend_count = Counter()
                else:
			self.trend_raw.extend(trends)
                        self.trend_count = Counter( self.trend_raw )
                        self.trend_count.most_common()
        def add(self, trends=[]):
                # this lets the bubble chart grow bigger
                self.trend_count = Counter(trends) + self.trend_count

BUBBLE_STATS = bubblestats()


#---------------------------------------------------------------
#
# app routes: end points for the app's web interface
#
#---------------------------------------------------------------
worker = cfworker.cfworker( port=int(os.getenv('VCAP_APP_PORT')) )
worker.app = Flask(__name__, static_url_path='')

@worker.app.route('/bubbles/post', methods=['POST'])
def post_bubbles():
        global BUBBLE_STATS
        try:
		trends = [str(f).lower() for f in request.get_json()['trends'] ]
                BUBBLE_STATS.update( trends=trends )
		print trends
        except Exception as e:
                print e
        finally:
                return json.dumps( BUBBLE_STATS.trend_count )

@worker.app.route('/metrics/field-value-counters/hashtags')
def metric_counter():
        global BUBBLE_STATS
        url = 'http://0.0.0.0:%d/metrics/field-value-counters/hashtags' % int(os.getenv('VCAP_APP_PORT'))
        return json.dumps({"name":"hashtags","links":[{"rel":"self","href": url}],"counts": BUBBLE_STATS.trend_count })

@worker.app.route('/metrics/field-value-counters')
def field_counter():
        return ""

@worker.app.route('/')
def bubble_chart():
        return worker.app.send_static_file('index.html')


#---------------------------------------------------------------
#
# logging: suppresses some of the annoying Flask output
#
#---------------------------------------------------------------
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
