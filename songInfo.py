class SongInfo:
	songName = "name"
	songArtist = "artist"

	def __init__(self, name, artist):
		self.songName = name
		self.songArtist = artist

	def toString(self):
		return ("Name: %s Artist: %s" % (self.songName, self.songArtist))

	def toSearchString(self):
		return ("%s %s" % (self.songName, self.songArtist))

class scrapedSongInfo:
	songName = "name"
	songArtist = "artist"
	songTime = "00:00"

	def __init__(self, name, artist, time):
		self.songName = name
		self.songArtist = artist
		self.songTime = time


	def toString(self):
		return ("Time: %s Name: %s Artist: %s" % (self.songTime, self.songName, self.songArtist))
