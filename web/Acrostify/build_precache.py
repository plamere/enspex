#
# builds track lists for the acrostic playlist maker.
# ensures that we have enough tracks for each letter
# based on letter frequencies


import sys
import pyen
import simplejson as json
import collections
import spotipy


en = pyen.Pyen()
sp = spotipy.Spotify()
sp.trace=False

#total = 1000
total = 1000
#max_calls = 1000
max_calls = 1000

session_id = None

frequency_table = {
    'a':   8.167  ,
    'b':   1.492  ,
    'c':   2.782  ,
    'd':   4.253  ,
    'e':   12.702 ,
    'f':   2.228  ,
    'g':   2.015  ,
    'h':   6.094  ,
    'i':   6.966  ,
    'j':   0.153  ,
    'k':   0.772  ,
    'l':   4.025  ,
    'm':   2.406  ,
    'n':   6.749  ,
    'o':   7.507  ,
    'p':   1.929  ,
    'q':   0.095  ,
    'r':   5.987  ,
    's':   6.327  ,
    't':   9.056  ,
    'u':   2.758  ,
    'v':   0.978  ,
    'w':   2.360  ,
    'x':   0.150  ,
    'y':   1.974  ,
    'z':   0.074  ,
}     

norm_freq_table = {}


x_songs = [
    {
        'title' : 'X',
        'uri':'spotify:track:4HIKcEKSijQLW5YNLsdLzt'
    },
    {
        'title' : 'XO',
        'uri':'spotify:track:7cpCU3Denug5NGZsSpQl8v'
    },
    {
        'title' : 'X',
        'uri':'spotify:track:1BvVorSqFQwZS9opIpKmUV'
    },
    {
        'title' : 'Xscape',
        'uri':'spotify:track:0xzSpvDboL5Imo8cP1vMXm'
    },
    {
        'title' : 'X You',
        'uri':'spotify:track:73ExUbskoIkjU0llIwsSzu'
    },
    {
        'title' : "X Gon' Give It To Ya",
        'uri':'spotify:track:6uP0XLqjRqFx8HAfesdcAg'
    },
    {
        'title' : 'Xxplosive',
        'uri':'spotify:track:0Ed7MeXx64f6OcIuoTRCg1'
    },
    {
        'title' : 'XOXO',
        'uri':'spotify:track:1YzIe5I0UNPgPRPxYpe92f'
    },
    {
        'title' : 'X&Y',
        'uri':'spotify:track:2rxp56vVQp1zzumJ0eHLmw'
    },
    {
        'title' : 'Queen of California',
        'uri':'spotify:track:0CETmgFGt8Ne8vLnaLcduU'
    },
    {
        'title' : 'Que Sera',
        'uri':'spotify:track:10kcfnWl3qEaKJNGP28AKy'
    },
    {
        'title' : 'Que Lloro',
        'uri':'spotify:track:10fHq85ktXp1K8mO45bugT'
    },
]

def build_norm_table():
    total_count = 0
    for key, percent in frequency_table.items():
        count = int(total * percent / 100.)
        if key <> 'x' and count < 4:
            count = 4
        elif  count < 4:
            count = 4

        total_count += count
        norm_freq_table[key] = count
    return total_count

def populate_songs(songs):
    page_size = 50

    for start in xrange(0, len(songs), page_size):
        bsongs = songs[start:start + page_size]
        ids = [ song['uri'] for song in bsongs]
        response = sp.tracks(ids)
        for track, song in zip(response['tracks'], bsongs):
            song['audio'] = track['preview_url']
            song['artist_uri'] = track['artists'][0]['uri']
            song['artist_name'] = track['artists'][0]['name']
    

def build_precache(genre):
    ''' gets mores songs in the genre
    '''

    cur_calls = 0
    total_count = build_norm_table()
    response = en.get('playlist/dynamic/create', type='genre-radio', genre=genre, 
        variety=1, distribution='wandering', bucket=['id:spotify', 'tracks'], limit=True)
    session_id = response['session_id']

    songs = []
    while len(songs) < total_count and cur_calls < max_calls:
        cur_calls += 1
        print 'calls', cur_calls
        report_hist(songs)
        response = en.get('playlist/dynamic/next', session_id=session_id, results=5)

        for song in response['songs']:
            if ok_to_add(song, songs):
                song = filter_song(song)
                songs.append(song)
            # print '      ', song['title'] + ' by' + song['artist_name']

    songs.extend(x_songs)
    report_hist(songs)
    songs.sort(key=lambda s:s['title'])
    populate_songs(songs)
    f = open(genre +'.js', 'w')
    print >>f, json.dumps(songs)
    f.close()

def ok_to_add(song, songs):
    letter = get_first_letter(song)
    letter = letter.lower()

    if letter in norm_freq_table:
        target = norm_freq_table[letter]
        cur = count_songs_that_start_with(letter, songs)
        return cur < target
    else:
        return False

def report_hist(songs):
    counts = collections.defaultdict(int)
    for s in songs:
        counts[ get_first_letter(s)] += 1

    list = [(c, l) for l, c in counts.items()]
    list.sort()

    for alpha in xrange(ord('a'), ord('z')):
        l = chr(alpha)
        print counts[l], norm_freq_table[l], l, '**' if counts[l] < norm_freq_table[l] else ''
    print

def get_first_letter(song):
    return song['title'][0].lower()

def count_songs_that_start_with(c, songs):
    count = 0
    for s in songs:
        if get_first_letter(s) == c:
            count += 1
    return count
        

    return True

def filter_song(song):
    '''
        {
            "artist_foreign_ids": [
                {
                    "catalog": "spotify",
                    "foreign_id": "spotify:artist:194376"
                }
            ],
            "artist_id": "ARAAQLO1187B993017",
            "artist_name": "Richie Sambora",
            "id": "SODYXGC12A6D4F6F3C",
            "title": "Ballad Of Youth",
            "tracks": [
                {
                    "catalog": "spotify",
                    "foreign_id": "S:track:t2715655",
                    "foreign_release_id": "rdio-US:release:a224436",
                    "id": "TRQHGUL136E83607C1"
                }
            ]
        }
    '''
    new_song = {
        'title': song['title'],
        'uri': song['tracks'][0]['foreign_id']
    }
    return new_song

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "python build_precache.py  genre'"
    else:
        build_precache(sys.argv[1])
