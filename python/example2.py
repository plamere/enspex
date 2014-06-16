import pyen
import spotipy
import sys

'''
 generates a playlist web page given a seed artist
'''

en = pyen.Pyen()
sp = spotipy.Spotify()

def get_cover_art(song):
    response = sp.track(song['tracks'][0]['foreign_id'])
    return response['album']['images'][0]['url']

def dump(song):
    print "<div>"
    print "  <img src='%s'>" % (get_cover_art(song), )
    print "  <h1>", song['title'], '<h1>'
    print "  <h2>", song['artist_name'], '<h2>'
    print "</div>"
    print "<hr>"

def generate_playlist():
    name = 'weezer'
    if len(sys.argv) > 1:
        name = ' '.join(sys.argv[1:])

    spids = []
    response = en.get('playlist/static', artist=name, type='artist-radio', \
        bucket=['tracks', 'id:spotify'], limit=True)

    print "<html><body>"
    for song in response['songs']:
        dump(song)
    print "</body></html>"

generate_playlist()
