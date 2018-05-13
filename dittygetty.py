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
    '''Commands for modifying the playlist'''
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
@click.option('--ff', is_flag=True, default=False, help="Displays the playlist in the file format(HH:MM||SongName||ArtistName). Can be output into a file for import later.")
#@click.option('--file', help = "Displays the playlist in a file.")
@pass_config
def playlist_display(config, ff):
    '''
    Displays playlist, default is active playlist
    '''
    temp_playlist = Playlist()
	
    try:
        temp_playlist.to_playlist((config['playlist_cli']))
        #print playlist
    except KeyError:
        pass

    for song in temp_playlist.get():
		if ff:
			print("%s||%s||%s\n" % (song.songTime, song.songName, song.songArtist))
		else:
			print("" + song.toString())

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
#@click.option('--jpr', '-j', help='Imports a playlist from jpr requires date input "MM-DD-YYYY"')
#@click.option('--file', '-f', help='Imports a textfile, give path of textfile')
@click.argument('date')
@click.option('--t', help='Starting time for parse', default="00:00")
@click.option('--et', help='Ending time for parse', default="23:59")
@pass_config
def playlist_import(config, date, t, et):
	'''
	Imports a playlist from NPR or textfile
    Requires a date in the formate MM-DD-YYYY
	'''

	temp_playlist = Playlist()
	try:
		tokens = date.split('-')
		print(tokens)
		month = int(tokens[0])
		day = int(tokens[1])
		year = int(tokens[2])
		temp_playlist.set(getList(month, day, year, t, et))
		
	except:
		raise click.UsageError('Invalid arguments, requires DATE input "MM-DD-YYYY"')
			
	if len(temp_playlist.playlist) != 0:
		playlist_dict = temp_playlist.to_dict()
		
		config['playlist_cli'] = playlist_dict
		config.save()
	else:
		print "No playlist found."

@entry_point.command('read')
@click.argument('file')
@pass_config
def playlist_read(config, file):
	'''
	Reads a playlist from textfile
	Each line in the file must be in the format 
		time||song||artist
	'''

	temp_playlist = Playlist()
	try:
		with open(file, 'r') as f:
			for line in f:
				line.encode('ascii', 'ignore')
				trimmed_line = line.replace('\n', "")
				name_artist = trimmed_line.split("||")
				song = SongInfo(name_artist[1], name_artist[2], name_artist[0])
				temp_playlist.add(song)
				
	except FileNotFoundException:
		print "%s not found." %(file)
    
	if len(temp_playlist.playlist) != 0:
		playlist_dict = temp_playlist.to_dict()
		
		config['playlist_cli'] = playlist_dict
		config.save()
	else:
		print "No playlist found."
		
@entry_point.command('write')
@click.argument('file')
@pass_config
def playlist_write(config, file):
	'''
    Writes the active playlist to the file with the designated name
	Will overwrite any previous data in that file
    '''
	temp_playlist = Playlist()
		
	try:
		temp_playlist.to_playlist((config['playlist_cli']))
		
		with open(file, 'w') as f:
			for song in temp_playlist.get():
				f.write("%s||%s||%s\n" % (song.songTime, song.songName, song.songArtist))
	except KeyError:
		pass
	except Exception as e:
		print e
		
@entry_point.command('export')
@click.argument('playlist_name')
#@click.option('--gmusic', '-g', help="Export active playlist to google music")
@pass_config
def playlist_export(config, playlist_name):
	'''
    Exports the active playlist to google music
    '''
	temp_playlist = Playlist()
		
	try:
		temp_playlist.to_playlist((config['playlist_cli']))
		
		login = click.prompt('Enter Google Music username: ')
		password = click.prompt('Enter Google Music password: ', hide_input=True)

		loginGmusic(login, password)

		uploadSongsGmusic(playlist_name, temp_playlist.get())
	except KeyError:
		pass
	except Exception as e:
		print e
		raise click.UsageError('Invalid login.')

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

#f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")
# if f is None:
	# return

# for song in playlist.get():
	# f.write("%s||%s||%s\n" % (song.songTime, song.songName, song.songArtist))