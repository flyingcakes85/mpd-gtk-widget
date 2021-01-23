import musicpd
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


builder = Gtk.Builder()
builder.add_from_file("./glade/mpd_popup.glade")

g_lbl_track_title = builder.get_object("lbl_track_title")
g_lbl_artist_name = builder.get_object("lbl_artist_name")
g_img_play = builder.get_object("img_play")
g_img_pause = builder.get_object("img_pause")
g_play_pause_button = builder.get_object("btn_play_pause")
mpd_client = musicpd.MPDClient()
mpd_client.connect()


def update():
    current_song_data = mpd_client.currentsong()
    if 'title' in current_song_data:
        #print(current_song_data['title'])
        song_title = current_song_data['title']
        if len(song_title) > 38:
            song_title = song_title[0:37] + "..."
        g_lbl_track_title.set_markup("<b>" + song_title + "</b>")
    else:
        #print(current_song_data['file'])
        song_title = current_song_data['file']
        if len(song_title) > 39:
            song_title = song_title[0:36] + "..."
        g_lbl_track_title.set_markup("<b>" + song_title + "</b>")

    if 'artist' in current_song_data:
        #print(current_song_data['artist'])
        song_artist = current_song_data['artist']
        if len(song_artist) > 39:
            song_artist = song_artist[0:37] + "..."
        g_lbl_artist_name.set_markup("<i>" + song_artist + "</i>")
    else:
        #print("Unknown")
        g_lbl_artist_name.set_markup("<i>Unknown</i>")


def on_next_click(button):
    mpd_client.next()
    update()


def on_prev_click(button):
    mpd_client.previous()
    update()

def on_play_pause_click(button):
    if(mpd_client.status()['state']) == "play":
        mpd_client.pause()
        button.set_image(g_img_play)
    else:
        mpd_client.pause()
        button.set_image(g_img_pause)

def set_play_button_icon():
    if mpd_client.status()['state'] == "play":
        g_play_pause_button.set_image(g_img_pause)
    else:
        g_play_pause_button.set_image(g_img_play)

window = builder.get_object("window_main")
window.show_all()

handlers = {"on_window_main_destroy": Gtk.main_quit,
            "on_prev_click": on_prev_click,
            "on_next_click": on_next_click,
            "on_play_pause_click": on_play_pause_click}

builder.connect_signals(handlers)
set_play_button_icon()
update()
Gtk.main()
