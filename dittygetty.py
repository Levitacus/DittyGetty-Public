import click
import os
from config import Config
from playlist import *
from songInfo import *

APP_NAME = 'dittygetty'
CONFIG_NAME = 'config.json'

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@pass_config
def entry_point(config):
    '''entry point to the cli'''
    if not config.load():
	config.save()
    pass #entry point to the cli

@entry_point.group()
def playlist():
    '''test'''
    if not os.path.exists(click.get_app_dir(APP_NAME)):
	os.makedirs(click.get_app_dir(APP_NAME))
    pass
    


#@playlist.group('modify')
#def playlist_modify():
#    pass
    
@playlist.command('add')
@click.argument('song')
@click.argument('artist')
@pass_config
def playlist_add(config, song, artist):
    '''Adds a song to the current playlist'''
    song_obj = SongInfo(song, artist)

    temp_playlist = Playlist()
    try:
        temp_playlist.to_playlist((config['playlist']))
        #print playlist
    except KeyError:
        print "Hey"
    
    temp_playlist.add(song_obj)

    playlist_dict = temp_playlist.to_dict()
    #print playlist_dict
    config['playlist_cli'] = playlist_dict
    config.save()

    click.echo('Song: %s. Artist: %s. \n' %(song, artist))

@playlist.command('display')
@pass_config
def playlist_get_dir(config):
    '''Displays playlist, default is active playlist'''
    temp_playlist = Playlist()

    try:
        temp_playlist.to_playlist((config['playlist_cli']))
        #print playlist
    except KeyError:
        print "Hey"

    for songs in temp_playlist.get():
	print(songs.toString())

@playlist.command('clear')
@pass_config
def playlist_get_dir(config):
    '''Clears playlist, default is active playlist'''

    try:
        temp_playlist = Playlist()

        config['playlist'] = temp_playlist.to_dict()
        config.save()

        click.echo('Active playlist clear successful')
    except:
        click.echo('ERROR: Active playlist clear unsuccessful') 

@playlist.command('get_dir')
@pass_config
def playlist_get_dir(config):
    '''Gets current app directory'''
    print(click.get_app_dir(APP_NAME))
    print(config.get('test', 'Does not exist'))

@playlist.command('write_test')
@pass_config
def playlist_write_dir(config):
    '''Writes test to current directory'''


    config['test'] = 'it works!!!'
    config.save()
    #click.echo('saved info')

entry_point.add_command(playlist)

    

if __name__ == '__main__':
    entry_point()
    
#So this creates a chain of commands.
#You can do 
#python dittygetty.py playlist modify add "21st Century Schizoid Man" "King Crimson"
#and it works
