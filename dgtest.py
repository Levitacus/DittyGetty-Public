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

#returns list of ids for given songs
def findStoreId(songList):
	idList = list()
	for songs in songList:
		search = api.search(songs.toSearchString(), max_results=4)
		#catch exception if there are no song hits
		try:
			if acceptSong(songs.songName, findTrackElement(search, 'title')[0]):
				idList.append(findTrackElement(search, 'storeId')[0])
		except (IndexError):
			print 'PLACEHOLDER: UNSUCCESSFUL SONG ADDITION'
			continue
			
	return idList

#placeholder
def acceptSong(realSongName, comparedSongName):
	print realSongName
	print comparedSongName
	print '\n'
	return True
			

def initializePlaylist(playlistName, idList):
	playlistId = api.create_playlist(playlistName, description=None, public=False)

	return api.add_songs_to_playlist(playlistId, idList)

def uploadSongsGmusic(playlistName, songArtistList):
	storeIdList =  findStoreId(songArtistList)

	if initializePlaylist(playlistName, storeIdList):
		return True
	else:
		return False


def loginGmusic():
	global api
	api = Mobileclient()
		
	logged_in = api.login('patkmatts@gmail.com', 'ztqiefdvkyuenkxm', Mobileclient.FROM_MAC_ADDRESS)

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

			

