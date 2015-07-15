#!/usr/bin/python
from twython import TwythonStreamer
import time, requests, json, os
from bubbles import worker

#---------------------------------------------------------------
#
# Twitter Streamer
#
#---------------------------------------------------------------
class MyStreamer(TwythonStreamer):

	def on_success(self, data):
		try:
			hashtags = [ tag['text'].encode('utf-8').lower() for tag in data['entities']['hashtags'] ]
			if hashtags: 
				r = requests.post(url='http://0.0.0.0:%d/bubbles/post' % int(os.getenv('VCAP_APP_PORT')), 
					data=json.dumps({'trends': hashtags }), headers={'Content-Type': 'application/json'})
		except Exception as e:
			print 'Bot error, found a problem parsing hashtag list: %s' % e

        def on_error(self, status_code, data):
                print 'Bot error, status code = %s' % status_code
                time.sleep(60)
                streamRun()

        def on_timeout(self):
                print 'Bot timeout, sleeping for 60 seconds. Zzzzzz....'
                time.sleep(60)
                streamRun()


def streamRun():
        try:
                stream = MyStreamer(os.getenv('APP_KEY'), os.getenv('APP_SECRET'), os.getenv('OAUTH_TOKEN'), 
			os.getenv('OAUTH_TOKEN_SECRET'), client_args={'verify':True} )
                track = sorted(set([tag.lower().strip() for tag in os.getenv('INCLUDE_TWITTER_HASH').split(',') ] ) )
                stream.statuses.filter(track=track)

        except Exception as e:
                time.sleep(60)
                streamRun()


if __name__=='__main__':
        try:
		worker.start()
                streamRun()
        except Exception as e:
                worker.stop()
                python = sys.executable
                os.execl(python, python, * sys.argv)

        worker.stop()
