from gmusicapi import Mobileclient
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
		search = api.search(songs, max_results=4)
		idList.append(findTrackElement(search, 'storeId')[0])
	return idList
			

def initializePlaylist(playlistName, idList):
	playlistId = api.create_playlist(playlistName, description=None, public=False)

	return api.add_songs_to_playlist(playlistId, idList)

def uploadSongsGmusic(playlistName, songArtistList):
	storeIdList =  findStoreId(my_list)

	if initializePlaylist(playlistName, storeIdList):
		print 'Success'
	else:
		print 'Failure to create playlist'

	

api = Mobileclient()
logged_in = api.login('patkmatts@gmail.com', 'ztqiefdvkyuenkxm', Mobileclient.FROM_MAC_ADDRESS)

if logged_in:
	print("SUCCESS\n")
else:
	print("NOT SUCCESSFUL\n")


my_list = ['Ana Ng','The Moment Tame Impala','sandstorm darude','fly me to the moon frank sinatra','zebra beach house', 
'robot rock daft punk']

uploadSongsGmusic('Test 2', my_list)
