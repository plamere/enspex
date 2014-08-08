# Acrostic
This is a tiny web app that hides secret messages in playlists. The is online at [Acrostic Playlist
Maker](http://static.echonest.com/enspex/acrostify).  

The app doesn't make any direct calls to Spotify or The Echo Nest API to generate the playlists. Instead it uses precrawled songs sets organized by genre. Each set is about 1000 songs in size. Frequency of the first letter in each song (which is used to create the Acrostic) matches [English letter frequency](http://en.wikipedia.org/wiki/Letter_frequency). To add a new genre crawl the song set with the build_precache.py python script like so:

    % python build_precache.py 'alternative rock'
   
add the output to the 'js' directory and add the genre name to the list of predefinedGenre found in the
fetchGenres() method in index.html
