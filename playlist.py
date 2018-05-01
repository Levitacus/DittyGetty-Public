class Playlist:
	
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
		
	
	#def move(self)

