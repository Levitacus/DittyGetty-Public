import click
import os
import sys
import dg_gui
from daily_playlist import DailyPlaylist
from datetime import datetime, timedelta
from config import Config
from playlist import *
from songInfo import *
from gmusic import *
from npr import NPR

APP_NAME = 'dittygetty'
CONFIG_NAME = 'config.json'

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@pass_config
def entry_point(config):
    '''
	DittyGetty is a tool used to scrape playlists from JPR, modify those playlists, and export those playlists to Google Music.
	'''
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

@entry_point.group()
@pass_config
def imports(config):
    '''Commands for importing a playlist'''
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
@click.option('--f', help = "Displays the playlist from a file without loading it into the active playlist")
@pass_config
def playlist_display(config, ff, f):
    '''
    Displays playlist, default is active playlist
    '''
    temp_playlist = Playlist()
	
    try:
		if f:
			temp_playlist = read_playlist(f)
		else:
			temp_playlist.to_playlist((config['playlist_cli']))
			#print playlist
    except KeyError:
        pass

    for song in temp_playlist.get():
		if ff:
			print("%s||%s||%s" % (song.songTime, song.songName, song.songArtist))
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

@entry_point.command('search')
@click.argument('search_str')
@click.option('--f', help='File: Option to save searched songs to a file rather than the active playlist.')
@click.option('--m', help='Set max number of results for the search')
@pass_config
def search(config, search_str, f):
	'''
	Searches a string on google music
	'''
	
	if not cli_login():
		raise click.ClickException('Invalid Google Music Account Login')

	searched_list = search_songs_text(search_str)
	
	if not searched_list:
		click.echo('No songs found with those search terms.')

	else:
		for songs in searched_list:
			print songs

		if f:
			prompt_string = ("Do you wish to save the searched songs to %s(y/n)?" % (f))
		else:
			prompt_string = "Do you wish to save the searched songs to your active playlist(y/n)?"

		choice = click.prompt(prompt_string)

		if choice.lower() != 'y':
			return

		temp_playlist = Playlist()
		temp_playlist.set(search_songs_obj(search_str))

	if f and len(temp_playlist.playlist) != 0:
		try:
			with open(f, 'w') as f:
				for song in temp_playlist.get():
					f.write("%s||%s||%s\n" % (song.songTime, song.songName, song.songArtist))
		except KeyError:
			pass
		except Exception as e:
			print e
	else:
		playlist_dict = temp_playlist.to_dict()
		
		config['playlist_cli'] = playlist_dict
		config.save()
			

	

@imports.command('jpr')
@click.argument('date')
@click.option('--t', help='Starting time for parse', default="00:00")
@click.option('--et', help='Ending time for parse', default="23:59")
@click.option('--f', help='File: Option to save imported songs to a file rather than the active playlist. Can use today and yesterday keywords.')
@pass_config
def playlist_import(config, date, t, et, f):
	'''
	Imports a playlist from JPR
    Requires a date in the format MM-DD-YYYY, 'today' or 'yesterday' keywords
	'''

	temp_playlist = Playlist()
	month, day, year = 0, 0, 0
	try:
		if date == "today":
			now = datetime.now()
			month = int(now.month)
			day = int(now.day)
			year = int(now.year)
			
			#limits the end time to now
			#et = str(now.hour) + ':' + str(now.minute)
			
		elif date == "yesterday":
			yesterday = datetime.now() - timedelta(days=1)
			month = int(yesterday.month)
			day = int(yesterday.day)
			year = int(yesterday.year)
			
		else:
			tokens = date.split('-')
			month = int(tokens[0])
			day = int(tokens[1])
			year = int(tokens[2])
		print t
		print et
		jpr = NPR("520a4969e1c85ef575dd2484")
		temp_playlist.set(jpr.scrape_run(month, day, year, t, et))
	except:
		raise click.UsageError('Invalid arguments, requires DATE input "MM-DD-YYYY"')

	if f and len(temp_playlist.playlist) != 0:
		if f == "today":
			f = datetime.today().strftime('%Y-%m-%d') +".txt"
		elif f == "yesterday":
			f = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d') +".txt"
		try:
			with open(f, 'w') as f:
				for song in temp_playlist.get():
					f.write("%s||%s||%s\n" % (song.songTime, song.songName, song.songArtist))
		except KeyError:
			pass
		except Exception as e:
			print e
		
	elif len(temp_playlist.playlist) != 0:
		playlist_dict = temp_playlist.to_dict()
		
		config['playlist_cli'] = playlist_dict
		config.save()
	else:
		print "No playlist found."

@imports.command('gmusic')
@click.argument('playlist_name')
@click.option('--f', help='File: Option to save imported songs to a file rather than the active playlist. Can use today and yesterday keywords.')
@pass_config
def playlist_import(config, playlist_name, f):
	'''
	Imports a playlist from gmusic, requires a playlist name
	'''
	if not cli_login():
			raise click.ClickException('Invalid Google Music Account Login')

	try:
		temp_playlist = Playlist()
		playlist_dict = {}
	
		for playlists in gmusic_get_playlists_content():
			if playlists['name'] == playlist_name:
				playlist_dict = playlists
				break

	
		if playlist_dict:
			track_list = playlist_dict['tracks']
			

			gmusic_songs = []

			for track in track_list:
				gmusic_songs.append(SongInfo(track['track']['title'].encode('ascii', 'ignore'), track['track']['artist'].encode('ascii', 'ignore')))
			temp_playlist.set(gmusic_songs)
		else:
			raise IndexError()

	except:
		raise click.UsageError('Playlist name must be a valid playlist in your gmusic account.')

	if f and len(temp_playlist.playlist) != 0:
		try:
			with open(f, 'w') as f:
				for song in temp_playlist.get():
					f.write("%s||%s||%s\n" % (song.songTime, song.songName, song.songArtist))
		except KeyError:
			pass
		except Exception as e:
			print e
		
	elif len(temp_playlist.playlist) != 0:
		playlist_dict = temp_playlist.to_dict()
		
		config['playlist_cli'] = playlist_dict
		config.save()
	else:
		print "No playlist found."

@imports.command('daily_playlist')
#@click.option('--jpr', '-j', help='Imports a playlist from jpr requires date input "MM-DD-YYYY"')
@click.argument('name')
@click.option('--f', help='File: Option to save imported songs to a file rather than the active playlist. Can use today and yesterday keywords.')
@pass_config
def playlist_import(config, name, f):
	'''
	Imports a playlist from dailyplaylist.com name argument is the url name given to a playlist
	i.e. dailyplaylist.com/chill-daily/ chill-daily is the playlist name
	'''

	temp_playlist = Playlist()

	try:
		dp = DailyPlaylist(name)
		temp_playlist.set(dp.scrape_run())
	except:
		raise click.UsageError('Invalid arguments, name must have no spaces')

	if f and len(temp_playlist.playlist) != 0:
		if f == "today":
			f = datetime.today().strftime('%Y-%m-%d') +".txt"
		elif f == "yesterday":
			f = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d') +".txt"
		try:
			with open(f, 'w') as f:
				for song in temp_playlist.get():
					f.write("%s||%s||%s\n" % (song.songTime, song.songName, song.songArtist))
		except KeyError:
			pass
		except Exception as e:
			print e
		
	elif len(temp_playlist.playlist) != 0:
		playlist_dict = temp_playlist.to_dict()
		
		config['playlist_cli'] = playlist_dict
		config.save()
	else:
		print "No playlist found."

@entry_point.command('gui')
@pass_config
def open_gui(config):
	'''
	Opens the graphical user interface to allow for playlst manipulation there.
	**Warning: Will halt this window.
	'''

	dg_gui.main()

@entry_point.command('read')
@click.argument('file')
@pass_config
def playlist_read(config, file):
	'''
	Reads a playlist from textfile
	Each line in the file must be in the format 
		time||song||artist
	'''

	temp_playlist = read_playlist(file)
    
	if len(temp_playlist.playlist) != 0:
		playlist_dict = temp_playlist.to_dict()
		
		config['playlist_cli'] = playlist_dict
		config.save()
	else:
		print "No playlist found."
		
@entry_point.command('write')
@click.argument('file')
@click.option('--m', is_flag=True, default=False, help="Merge: If file already exists, append active playlist with duplicate removal")
@pass_config
def playlist_write(config, file, m):
	'''
    Writes the active playlist to the file with the designated name
	Will overwrite any previous data in that file
    '''
	temp_playlist = Playlist()
		
	try:
		temp_playlist.to_playlist((config['playlist_cli']))
		
		#This won't get rid of duplicates 
		if m:
			temp_playlist2 = read_playlist(file)
			merged_playlist = Playlist()
			for song in temp_playlist2.get():
				if song not in temp_playlist.get():
					temp_playlist.add(song)
				
		
		with open(file, 'w') as f:
			for song in temp_playlist.get():
				f.write("%s||%s||%s\n" % (song.songTime, song.songName, song.songArtist))
	except KeyError:
		pass
	except Exception as e:
		print e
		
@entry_point.command('exports')
@click.argument('playlist_name')
@click.option('--f',  help="File: Export a file to Gmusic rather than the active playlist")
@click.option('--e', is_flag=True, default=False, help="Add Existing: Add songs to an existing playlist.")
@click.option('--m', is_flag=True, default=False, help="Merge: If adding to an existing playlist, duplicate songs will not be added")
#@click.option('--gmusic', '-g', help="Export active playlist to google music")
@pass_config
def playlist_export(config, f, e, m, playlist_name):
	'''
    Exports the active playlist to google music with the name [PLAYLIST_NAME]
    '''
	temp_playlist = Playlist()
	success = False
		
	try:
		if f:
			temp_playlist = read_playlist(f)
		else:
			temp_playlist.to_playlist((config['playlist_cli']))
		
		if not cli_login():
			raise click.ClickException('Invalid Google Music Account Login')
		
		if(e):
			playlists_dict = gmusic_get_playlists()

			playlist_id = 0
			for dicts in playlists_dict:
				if(dicts['name'] == playlist_name):
					playlist_id = dicts['id']
			
			if(playlist_id):
				success = upload_gmusic_loading(playlist_id, temp_playlist.get(), e, m)
			else:
				click.echo('Could not find existing playlist:  %s, creating new playlist' % playlist_name)
				success = upload_gmusic_loading(playlist_name, temp_playlist.get())

		else:
			click.echo('Creating new playlist: %s' % playlist_name)
			success = upload_gmusic_loading(playlist_name, temp_playlist.get())

		if(success):
			click.echo('Export successful, songs added to: %s' % playlist_name)
		else:
			raise click.ClickException('Export failed')

	except KeyError:
		pass
	#except Exception as e:
		#raise click.ClickException('Export failed')
		
@entry_point.command('reset')
@pass_config
def reset(config):
	'''
		Resets the user's username and password
	'''
	try:
		config['password'] = ''
		config['username'] = ''
		config.save()
		click.echo('Your username and password have been reset')
	except:
		pass
		
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


def read_playlist(file):
	'''
	Tries to read a playlist from a given file
	prints error if it fails
	returns playlist object
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
	except IOError:
		raise click.UsageError("%s not found." %(file))
		return Playlist()
	except:
		raise click.UsageError("No playlist found in %s." %(file))
		return Playlist()

	return temp_playlist

@pass_config
def cli_login(config):
	'''
	Prompts user for login information and returns
	results of login
	'''
	
	if config['username'] and config['password']:
		login = config['username']
		password = config['password']

	else:
		login = click.prompt('Enter Google Music username: ')
		password = click.prompt('Enter Google Music password: ', hide_input=True)
			
	
	valid_login = loginGmusic(login, password)
	
	if valid_login:
		config['username'] = login
		config['password'] = password
		config.save()
		
	return valid_login

def upload_gmusic_loading(playlist_name_id, songs_list, existing=False, merge=False):
	ids_list = []
	failed_songs = []

	for i, song in enumerate(songs_list):
		song_id = find_store_id(song)

		if(song_id):
			ids_list.append(song_id)
		else:
			failed_songs.append(song)
			
		if os.name == 'nt':
			print_loading_bar(i, len(songs_list) - 1, fill='X')
		else:
			print_loading_bar(i, len(songs_list) - 1)

	return upload_ids_gmusic(playlist_name_id, ids_list, existing, merge)


def print_loading_bar (iteration, total, length = 20, fill = '█'):
	"""
	Call in a loop to create terminal progress bar
	@params:
	iteration   - Required  : current iteration (Int)
	total       - Required  : total iterations (Int)
	length      - Optional  : character length of bar (Int)
	fill        - Optional  : bar fill character (Str)
	"""
	percent = ("{0:." + str(2) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	sys.stdout.write('\rExporting Songs: |%s| %s%% Complete' % (bar, percent))
	sys.stdout.flush()
	# Print New Line on Complete
	if iteration >= total: 
		print()

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
