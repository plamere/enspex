import pyen
import spotipy
import sys

'''
 get a set of images for artists that are similar to 
 the given seed artist
'''

en = pyen.Pyen()
sp = spotipy.Spotify()

name = 'weezer'
if len(sys.argv) > 1:
    name = ' '.joi(sys.argv[1:])

spids = []
response = en.get('artist/similar', name=name, bucket='id:spotify', limit=True)
for artist in response['artists']:
    spids.append(artist['foreign_ids'][0]['foreign_id'])

for artist in sp.artists(spids)['artists']:
    print artist['images'][0]['url'], artist['name']


