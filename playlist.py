from songInfo import *

class Playlist:
	#can change this to inherit from list
	def __init__(self, playlist = list()):
		self.playlist = playlist
	
	def add(self, song):
		self.playlist.append(song)
		
	def remove(self, index):
		del self.playlist[index]
		
	def clear(self):
		self.playlist = list()
		
	def set(self, list):
		self.playlist = list
		
	def get(self):
		return self.playlist
		

	def to_dict(self):
		times = []
		songs = []
		artists = []
		playlist_dict = dict()
		
		for song in self.playlist:
			times.append(song.songTime)
			songs.append(song.songName)
			artists.append(song.songArtist)
		
		playlist_dict['times'] = times
		playlist_dict['songs'] = songs
		playlist_dict['artists'] = artists
		return playlist_dict
	
	def to_playlist(self, playlist_dict):
		times = playlist_dict['times']
		songs = playlist_dict['songs']
		artists = playlist_dict['artists']
		
		playlist = []
		try:
			for item in range(0, len(songs)):
				song = SongInfo(songs[item], artists[item], times[item])
				playlist.append(song)
		except Exception as e:
			print e
			
		self.playlist = playlist
		
	
	#def move(self)

