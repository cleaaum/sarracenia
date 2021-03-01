import sarracenia.moth
import sarracenia.moth.amqp

import time
import socket
from urllib.parse import urlparse
import urllib.request
import xml.etree.ElementTree as ET

broker = urlparse('amqps://anonymous:anonymous@hpfx.collab.science.gc.ca')

options = sarracenia.moth.default_options
options.update(sarracenia.moth.amqp.default_options)
options['topic_prefix'] = [ 'v02', 'post' ]
options['bindings'] = [( 'xpublic', ['v02', 'post'] , ['*', 'WXO-DD', 'observations', 'swob-ml', '#'] )]
options['queue_name'] = 'q_anonymous_' + socket.getfqdn() + '_SomethingHelpfulToYou'

#print('options: %s' % options)

h = sarracenia.moth.Moth.subFactory(broker, options)

count=0

while count < 10:
    messages = h.newMessages()
    for m in messages:
        dataUrl = m['baseUrl']
        if 'retPath' in m:
           dataUrl += m['retPath']
        else:
           dataUrl += m['relPath']

        print("url %d: %s" % (count,dataUrl) )
        with urllib.request.urlopen( dataUrl ) as f:
            vxml = f.read().decode('utf-8')
            xmlData = ET.fromstring(vxml)
            
            stn_name=''
            tc_id=''
            lat=''
            lon=''
            air_temp=''
            
            for i in xmlData.iter():
                name = i.get('name')
                if name == 'stn_nam' :
                   stn_name= i.get('value')
                elif name == 'tc_id' :
                   tc_id = i.get('value')
                elif name == 'lat' :
                   lat =  i.get('value')
                elif name == 'long' :
                   lon  = i.get('value')
                elif name == 'air_temp' :
                   air_temp = i.get('value')

            print( 'station: %s, tc_id: %s, lat: %s, long: %s, air_temp: %s' % 
                   ( stn_name, tc_id, lat, lon, air_temp  ))
        h.ack(m)
        count += 1
        if count > 10:
            break
    time.sleep(1)

h.cleanup() # remove server-side queue defined by Factory.
h.close()
print("obtained 10 product announcements")
