class songInfo:

	songName = "name"

	songArtist = "artist"



	def __init__(self, name, artist):

		self.songName = name

		self.songArtist = artist



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