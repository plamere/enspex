

function getConfig() {
    return {
        apiKey: "ECLJI0GPBJVEXSZDT",
        spotifySpace: "spotify",
        echoNestHost: "http://developer.echonest.com/"
    };
}

/* Tools for making working with the Spotify and Echo Nest APIs easier */
function getSpotifyPlayButtonForPlaylist(title, playlist) {
    var embed = '<iframe src="https://embed.spotify.com/?uri=spotify:trackset:PREFEREDTITLE:TRACKS" style="width:640px; height:520px;" frameborder="0" allowtransparency="true"></iframe>';
    var tids = [];
    playlist.forEach(function(song) {
        var tid = fidToSpid(song.tracks[0].foreign_id);
        tids.push(tid);
    });
    var tracks = tids.join(',');
    var tembed = embed.replace('TRACKS', tracks);
    tembed = tembed.replace('PREFEREDTITLE', title);
    var li = $("<span>").html(tembed);
    return $("<span>").html(tembed);
}

/* converts full URI to just the simple spotify id */

function fidToSpid(fid) {
    var fields = fid.split(':');
    return fields[fields.length - 1];
}

function getSpotifyPlayer(inPlaylist, callback) {
    var curSong = 0;
    var audio = null;
    var player = createPlayer();
    var playlist = null;

    function addSpotifyInfoToPlaylist() {
        var tids = [];
        inPlaylist.forEach(function(song) {
            var tid = fidToSpid(song.tracks[0].foreign_id);
            tids.push(tid);
        });

        $.getJSON("https://api.spotify.com/v1/tracks/", { 'ids': tids.join(',')}) 
            .done(function(data) {
                console.log('sptracks', tids, data);
                data.tracks.forEach(function(track, i) {
                    inPlaylist[i].spotifyTrackInfo = track;
                });

                console.log('inPlaylist', inPlaylist);
                playlist = filterSongs(inPlaylist);
                showCurSong(false);
                callback(player);
            })
            .error( function() {
                info("Whoops, had some trouble getting that playlist");
            }) ;
    }

    function filterSongs(songs) {
        var out = [];

        function isGoodSong(song) {
            return song.spotifyTrackInfo.preview_url != null;
        }

        songs.forEach(function(song) {
            if (isGoodSong(song)) {
                out.push(song);
            }
        });

        return out;
    }

    function showSong(song, autoplay) {
        $(player).find(".sp-album-art").attr('src', getBestImage(song.spotifyTrackInfo.album.images, 300).url);
        $(player).find(".sp-title").text(song.title);
        $(player).find(".sp-artist").text(song.artist_name);
        audio.attr('src', song.spotifyTrackInfo.preview_url);
        if (autoplay) { 
            audio.get(0).play();
        }
    }


    function getBestImage(images, maxWidth) {
        var best = images[0];
        images.reverse().forEach(
            function(image) {
                if (image.width <= maxWidth) {
                    best = image;
                }
            }
        );
        return best;
    }

    function showCurSong(autoplay) {
        showSong(playlist[curSong], autoplay);
    }

    function nextSong() {
        if (curSong < playlist.length - 1) {
            curSong++;
            showCurSong(true);
        } else {
        }
    }

    function prevSong() {
        if (curSong > 0) {
            curSong--;
            showCurSong(true);
        }
    }

    function togglePausePlay() {
        console.log('tpp', audio.get(0).paused);
        if (audio.get(0).paused) {
            audio.get(0).play();
        } else {
            audio.get(0).pause();
        }
    }

    function createPlayer() {
        var main = $("<div class='sp-player'>");
        var img = $("<img class='sp-album-art'>");
        var info  = $("<div class='sp-info'>");
        var title = $("<div class='sp-title'>");
        var artist = $("<div class='sp-artist'>");
        var controls = $("<div class='btn-group sp-controls'>");

        var next = $('<button class="btn btn-primary btn-sm" type="button"><span class="glyphicon glyphicon-forward"></span></button>');
        var prev = $('<button class="btn btn-primary btn-sm" type="button"><span class="glyphicon glyphicon-backward"></span></button>');
        var pausePlay = $('<button class="btn btn-primary btn-sm" type="button"><span class="glyphicon glyphicon-play"></span></button>');


        audio = $("<audio>");
        audio.on('pause', function() {
            var pp = pausePlay.find("span");
            pp.removeClass('glyphicon-pause');
            pp.addClass('glyphicon-play');
        });

        audio.on('play', function() {
            var pp = pausePlay.find("span");
            pp.addClass('glyphicon-pause');
            pp.removeClass('glyphicon-play');
        });

        audio.on('ended', function() {
            console.log('ended');
            nextSong();
        });

        next.on('click', function() {
            nextSong();
        });

        pausePlay.on('click', function() {
            togglePausePlay();
        });

        prev.on('click', function() {
            prevSong();
        });


        info.append(title);
        info.append(artist);

        controls.append(prev);
        controls.append(pausePlay);
        controls.append(next);

        main.append(img);
        main.append(info);
        main.append(controls);
    
        main.bind('destroyed', function() {
            console.log('player destroyed');
            audio.pause();
        });
        return main;
    }

    addSpotifyInfoToPlaylist();
    return player;
}

// set up a handler so if an element is destroyed,
// the 'destroyed' handler is invoked.
// See // http://stackoverflow.com/questions/2200494/jquery-trigger-event-when-an-element-is-removed-from-the-dom

(function($){
  $.event.special.destroyed = {
    remove: function(o) {
      if (o.handler) {
        o.handler()
      }
    }
  }
})(jQuery);
