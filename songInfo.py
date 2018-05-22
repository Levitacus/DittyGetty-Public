class SongInfo:
	songName = "name"
	songArtist = "artist"
	songTime = "00:00"

	def __init__(self, name, artist, time=''):
		self.songName = name
		self.songArtist = artist
		self.songTime = time

	def toString(self):
		return ("Time: %s Name: %s Artist: %s" % (self.songTime, self.songName, self.songArtist))

	def toSearchString(self):
		return ("%s %s" % (self.songName, self.songArtist))
		
	def __eq__(self, other):
		return self.songName == other.songName and self.songArtist == other.songArtist

if __name__ == "__main__":
	song1 = SongInfo("Hello", "World")
	song2 = SongInfo("Hello", "World")
	if song1 == song2:
		print("Hello World")