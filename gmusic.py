from gmusicapi import Mobileclient
from songInfo import SongInfo
import pprint


#given a search list from gmusicapi this function returns
#a list of the given element for each song in the search list
def findTrackElement(searchDict, element):
	finalList = list()
	searchDict = searchDict.get('song_hits')
	
	for songs in searchDict:
		song = songs.get('track')
		finalList.append(song.get(element))

	return finalList

def search_songs_text(search_str, max):
	search = api.search(search_str, max_results=max)
	song_list = list()

	i = 0

	for songs in search['song_hits']:
		i += 1
		song_list.append("%d: Title: %s Artist: %s Album: %s" % (i, songs['track']['title'], songs['track']['artist'], songs['track']['album']))

	return song_list

def search_songs_obj(search_str, max):
	search = api.search(search_str, max_results=max)
	song_list = list()

	i = 0

	for songs in search['song_hits']:
		i += 1
		song_list.append(SongInfo(songs['track']['title'], songs['track']['artist']))

	return song_list

#returns list of ids for given songs
def find_store_ids(songList):
	idList = list()
	for songs in songList:
		search = api.search(songs.toSearchString(), max_results=4)
		#catch exception if there are no song hits
		try:
			if acceptSong(songs.songName, findTrackElement(search, 'title')[0]):
				idList.append(findTrackElement(search, 'storeId')[0])
		except (IndexError):
			print 'PLACEHOLDER: UNSUCCESSFUL SONG ADDITION'
			failedSongs.append(songs)
			continue
			
	return idList

def find_store_id(song):
	search = api.search(song.toSearchString(), max_results=4)

	try:
		if acceptSong(song.songName, findTrackElement(search, 'title')[0]):
			song_id = findTrackElement(search, 'storeId')[0]
	except (IndexError):
		return None
			
	return song_id

#placeholder
def acceptSong(realSongName, comparedSongName):
	
	#print realSongName
	#print comparedSongName
	#print '\n'
	return True
			

def add_songs_existing(playlistID, idList):
	return api.add_songs_to_playlist(playlistID, idList)

#def upload_songs_existing_gmusic(playlistID, songArtistList, existing=False, merge=False):
	#storeIdList =  findStoreId(songArtistList)

	#if add_songs_existing(playlistID, storeIdList):
		#return failedSongs
	#else:
		#return False

def initializePlaylist(playlistName, idList):
	playlistId = api.create_playlist(playlistName, description=None, public=False)

	return api.add_songs_to_playlist(playlistId, idList)

def upload_ids_gmusic(playlist_name_id, store_id_list, existing=False, merge=False):

	if existing:
		if merge:
			playlists = api.get_all_user_playlist_contents()
			for playlist_dict in playlists:
				if playlist_dict['id'] == playlist_name_id:
					playlist = playlist_dict
					break
			
			current_trackIds = [track['trackId'] for track in playlist['tracks']]

			for current_trackId in current_trackIds:
				if current_trackId in store_id_list:
					store_id_list.remove(current_trackId)

		return add_songs_existing(playlist_name_id, store_id_list)

	else:
		return initializePlaylist(playlist_name_id, store_id_list)

def uploadSongsGmusic(playlist_name_id, songArtistList, existing=False, merge=False):
	storeIdList = find_store_ids(songArtistList)

	if existing:
		if merge:
			playlists = api.get_all_user_playlist_contents()
			for playlist_dict in playlists:
				if playlist_dict['id'] == playlist_name_id:
					playlist = playlist_dict
					break
			
			current_trackIds = [track['trackId'] for track in playlist['tracks']]

			for current_trackId in current_trackIds:
				if current_trackId in storeIdList:
					storeIdList.remove(current_trackId)

		if add_songs_existing(playlist_name_id, storeIdList):

			#if failedSongs is empty
			if not failedSongs:
				return True

			return failedSongs
		else:
			return False
	else:
		if initializePlaylist(playlist_name_id, storeIdList):
			#if failedSongs is empty
			if not failedSongs:
				return True
			return failedSongs
		else:
			return False

def gmusic_get_playlists():
	return api.get_all_playlists()

def gmusic_delete_playlist(playlist_id):
	return api.delete_playlist(playlist_id)

def gmusic_get_playlists_content():
	return api.get_all_user_playlist_contents()

def loginGmusic(username, pword):
	global api
	global failedSongs
	failedSongs = list()
	api = Mobileclient()
		
	#logged_in = api.login('patkmatts@gmail.com', 'ztqiefdvkyuenkxm', Mobileclient.FROM_MAC_ADDRESS)

	logged_in = api.login(username, pword, Mobileclient.FROM_MAC_ADDRESS)

	if logged_in:
		return True
	else:
		return False


#my_list = ['Ana Ng','The Moment Tame Impala','sandstorm darude','fly me to the moon frank sinatra','zebra beach house',  'robot rock daft punk']

#my_songs = list()


#my_songs.append(SongInfo('Ana Ng', 'They Might Be Giants'))
#my_songs.append(SongInfo('Sandstorm', 'Darude'))
#my_songs.append(SongInfo('The Moment', 'Tame Impala'))
#my_songs.append(SongInfo('Aerodynamic', 'Daft Punk'))



#uploadSongsGmusic('Test 3', my_songs)

			

