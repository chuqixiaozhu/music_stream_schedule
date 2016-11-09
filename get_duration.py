######## -*- coding: utf-8 -*-
# import pylast
import csv
from urllib.request import urlopen
import json
from pprint import pprint
from urllib.parse import quote
from socket import timeout

def get_duration(mbid='', artist='', track=''):
    """User mbid or (artist name, track name) to get a song's length by Last.fm's API"""
    API_KEY = '6b4e8353c48564c23e4562ae16ab7802'
    API_SECRET = 'a1da6abe8ca8bede832d19d36d7800a8'

    # mbid = "4e78efc4-e545-47af-9617-05ff816d86e2"
    is_found = False
    if mbid != '':
        url = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo\
                    &api_key=6b4e8353c48564c23e4562ae16ab7802\
                    &mbid=" + mbid \
                 + "&format=json"
        # print("@19 url =", url) # test
        try:
            with urlopen(url) as url_response:
            # url_response = urlopen(url)
                info = json.loads(url_response.read().decode('utf-8'))
                if 'track' in info:
                    is_found = True
                    duration = info['track']['duration']
        except (HTTPError, URLError, timeout):
            print("Error: get_duration: time out")
        except:
            print("Error: get_duration: something wrong when urlopen")

        

    #if mbid == '' and not is_found:
    else:
        # artist_name = quote("Underworld")
        # track_name = quote("Composition 0919 (Live_2009_4_15)")
        # track_name = quote("Crocodile (Innervisions Orchestra Mix)")
        # track_name = unicode(track_name, "utf-8")
        # track_name = track_name.encode('UTF-8')

        artist_name = quote(artist)
        track_name = quote(track)
        url = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo\
                    &api_key=6b4e8353c48564c23e4562ae16ab7802\
                    &artist=" + artist_name \
                 + "&track=" + track_name \
                 + "&format=json"
        # url_name = url_name.encode("utf-8")
        try:
            with urlopen(url) as url_response:
            # url_response = urlopen(url)
                info = json.loads(url_response.read().decode('utf-8'))
                if 'track' in info:
                    is_found = True
                    duration = info['track']['duration']
        except (timeout):
            print("Error: get_duration: time out")
        except:
            print("Error: get_duration: something wrong when urlopen")
        # print(url_name)
        # url_response = urlopen(url_mbid)
    # url_response = urlopen(url)
    # info = json.loads(url_response.read().decode('utf-8'))
    # pprint(info)
    # print(type(info['track']))
    # print(info['track']['duration'])
    if is_found:
        return duration
    else:
        return '?'
    # return info['track']['duration']
    # pprint(info)



