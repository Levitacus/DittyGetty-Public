import click
import os
from config import Config
from playlist import *
from songInfo import *
from gmusic import *
from jpr import *

APP_NAME = 'dittygetty'
CONFIG_NAME = 'config.json'

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@pass_config
def entry_point(config):
    '''entry point to the cli'''
    if not os.path.exists(click.get_app_dir(APP_NAME)):
	os.makedirs(click.get_app_dir(APP_NAME))
    if not config.load():
	config.save()
    pass #entry point to the cli

@entry_point.group()
@pass_config
def playlist(config):
    '''test'''
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
        temp_playlist.to_playlist((config['playlist_cli']))
        #print playlist
    except KeyError:
        pass
    
    temp_playlist.add(song_obj)

    playlist_dict = temp_playlist.to_dict()
    #print playlist_dict
    config['playlist_cli'] = playlist_dict
    config.save()

    click.echo('Song: %s. Artist: %s. \n' %(song, artist))

@playlist.command('display')
@pass_config
def playlist_display(config):
    '''
    Displays playlist, default is active playlist
    '''
    temp_playlist = Playlist()

    try:
        temp_playlist.to_playlist((config['playlist_cli']))
        #print playlist
    except KeyError:
        pass

    for songs in temp_playlist.get():
	print(songs.toString())

@playlist.command('clear')
@pass_config
def playlist_clear(config):
    '''Clears playlist, default is active playlist'''

    try:
        temp_playlist = Playlist()

        config['playlist_cli'] = temp_playlist.to_dict()
        config.save()

        click.echo('Active playlist clear successful')
    except:
        click.echo('ERROR: Active playlist clear unsuccessful') 

@entry_point.command('import')
@click.argument('date')
@click.option('--t', help='Starting time for parse')
@click.option('--et', help='Ending time for parse --t is required for this option')
@pass_config
def playlist_import(config, date, t, et):
    '''
    imports an NPR playlist
    requires date input "MM-DD-YYYY
    '''
    if not t:
        if et:
	    raise click.UsageError('--t option required for --et')

    #set default values
    if not t:
        t = "00:00"
    if not et:
        et = "23:59"

    temp_playlist = Playlist()
    try:
	tokens = date.split('-')
	print(tokens)
        month = int(tokens[0])
	day = int(tokens[1])
	year = int(tokens[2])
        #temp_playlist.to_playlist((config['playlist_cli']))
        #print playlist
    except:
        raise click.UsageError('Invalid arguments, requires DATE input "MM-DD-YYYY"')


    
    
    temp_playlist.set(getList(month, day, year, t, et))

    playlist_dict = temp_playlist.to_dict()
    #print playlist_dict
    config['playlist_cli'] = playlist_dict
    config.save()

@entry_point.command('export')
@click.argument('name')
@pass_config
def playlist_export(config, name):
    '''
    Exports the active playlist
    '''

    login = click.prompt('Enter Google Music username: ')
    password = click.prompt('Enter Google Music password: ')

    loginGmusic(login, password)

    temp_playlist = Playlist()
    
    try:
        temp_playlist.to_playlist((config['playlist_cli']))
        #print playlist
    except KeyError:
        pass

    uploadSongsGmusic(name, temp_playlist.get())    


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
