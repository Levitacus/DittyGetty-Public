from Tkinter import *
from jpr import *
from songInfo import *
from dgtest import *
import tkFileDialog
import tkMessageBox

#The current playlist that is viewed, needs to be global.

playlist = list()
#playlist = getList(2, 8, 2017, "2:00", "14:00")

class Application(Frame):
	
	#Various callback functions for the homepage buttons
	def add_song(self):
		self.add_window = Toplevel(root)
		self.add_window.wm_title("Enter Date and Time")
		
		self.addSong = ""
		self.addArtist = ""
		
		#Entry field for song name
		self.song_entry = Entry(self.add_window)
		song_label = Label(self.add_window, text="Song Name")
		
		#Entry field for artist name
		self.artist_entry = Entry(self.add_window)
		artist_label = Label(self.add_window, text="Artist Name")
		
		self.add_window.submit_button = Button(self.add_window, text="Submit", command=self.add_confirm)
		
		#place all of the widgets
		song_label.grid(row=1, column=0)
		self.song_entry.grid(row=2, column=0)
		
		artist_label.grid(row=1, column=1)
		self.artist_entry.grid(row=2, column=1)
		
		self.add_window.submit_button.grid(row=2, column=2)
		
	
	def add_confirm(self):
		global playlist
		song = SongInfo(self.song_entry.get(), self.artist_entry.get())
		playlist.append(song)
		self.playlist_viewer.insert(END, song.toString())
		self.add_window.destroy()
	
	def helpbox(self):
		global playlist
		
		for song in playlist:
			print song
		
	def remove_song(self):
		global playlist
		items = self.playlist_viewer.curselection()
		count = 0
		for item in items:
			del playlist[item - count]
			print(self.playlist_viewer.get(item - count))
			self.playlist_viewer.delete(item - count)
			count += 1
			
		# Old way, doesn't work as well because it updated the whole playlist
		# Every time you removed song(s)
		
		# songs = list()
		# for item in items:
			# songs.append(self.playlist_viewer.get(item))
		
		# for song in songs:
			# print song
			# for element in playlist:
				# if song == element:
					# playlist.remove(element)
		# self.updatePlaylist()
		
	def clear_songs(self):
		global playlist
		playlist = list()
		self.playlist_viewer.delete(0, END)
		print "Clear!"
		
	def import_text(self):
		global playlist
		filename = tkFileDialog.askopenfilename()
		file = open(filename, 'r')

		if file is None:
			return

		playlist = list()
		self.playlist_viewer.delete(0, END)

		for line in file:
			trimmedLine = line.replace('\n', "")
			nameArtist = trimmedLine.split("-")
			song = SongInfo(nameArtist[0], nameArtist[1])
			playlist.append(song)

		self.updatePlaylist()

		
	def export_text(self):
		f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")
		if f is None:
			return

		for songs in playlist:
			f.write("%s-%s\n" % (songs.songName, songs.songArtist))

		f.close()
		
	def export_gmusic(self):
		self.t = Toplevel(root)
		self.t.wm_title("Export")

		self.playlistName = ""
		self.playlist_name_entry = Entry(self.t)
		playlist_name_label = Label(self.t, text="Enter Playlist Name Here")

		self.t.submit_button2 = Button(self.t, text="Submit", command=self.exportGmusic)	

		playlist_name_label.grid(row=1, column=0)
		self.playlist_name_entry.grid(row=2, column=0)	

		self.t.submit_button2.grid(row=3, column=0)
		
		
	def scrape(self):
		#
		self.t = Toplevel(root)
		self.t.wm_title("Enter Date and Time")
		
		self.month = 0
		self.day = 0 
		self.year = 0
		self.startTime = ""
		self.endTime = ""
		#t.month_entry = Entry(t, textvariable=self.month)
		self.month_entry = Entry(self.t)
		month_label = Label(self.t, text="Enter Month here")
		
		#t.day_entry = Entry(t, textvariable=self.day)
		self.day_entry = Entry(self.t)
		day_label = Label(self.t, text="Enter Day here")
		
		#t.year_entry = Entry(t, textvariable=self.year)
		self.year_entry = Entry(self.t)
		year_label = Label(self.t, text="Enter Year here")
		
		self.startTime_entry = Entry(self.t)
		startTime_label = Label(self.t, text="Start Time")
		
		self.endTime_entry = Entry(self.t)
		endTime_label = Label(self.t, text="End Time")
		
		hyphen_label = Label(self.t, text="-")
		
		#important that the callback function here just references the command, not passing it
		self.t.submit_button = Button(self.t, text="Submit", command=self.getPlaylist)
		
		#place all of the widgets
		month_label.grid(row=1, column=0)
		self.month_entry.grid(row=2, column=0)
		
		day_label.grid(row=1, column=1)
		self.day_entry.grid(row=2, column=1)
		
		year_label.grid(row=1, column=2)
		self.year_entry.grid(row=2, column=2)
		
		startTime_label.grid(row=3, column=0)
		self.startTime_entry.grid(row=4, column=0)
		
		hyphen_label.grid(row=4, column=1)
		
		endTime_label.grid(row=3, column=2)
		self.endTime_entry.grid(row=4, column=2)
		
		self.t.submit_button.grid(row=5, column=1)
		
	#callback function for the submit_button for exporting to gmusic
	def exportGmusic(self):
		global playlist
		
		self.playlistName = self.playlist_name_entry.get()

		loginGmusic()

		if uploadSongsGmusic(self.playlistName, playlist):
			tkMessageBox.showinfo('Playlist Creation', 'Creation of playlist: %s successful!' % (self.playlistName))
		else:
			tkMessageBox.showinfo('Playlist Creation Error', 'Creation of playlist: %s unsuccessful!' % (self.playlistName))
		
		self.t.destroy()
		
	#callback function for the submit_button
	def getPlaylist(self):
		global playlist
		
		self.month, self.day, self.year = int(self.month_entry.get()), int(self.day_entry.get()), int(self.year_entry.get())
		self.startTime = self.startTime_entry.get()
		self.endTime = self.endTime_entry.get()
		#call getList function from jpr.py
		playlist = getList(self.month, self.day, self.year, self.startTime, self.endTime)
		self.updatePlaylist()
		self.t.destroy()
	
	#Was supposed to update the playlist in the viewer to match the playlist variable
	#but alas, it is borked
	def updatePlaylist(self):
		global playlist
		
		# for song in playlist:
			# print song
		self.playlist_viewer.delete(0, END)
		for song in playlist:
			self.playlist_viewer.insert(END, song.toString())
		print 'update playlist was called'
	
		
		
	def createWidgets(self):
		#self.playlist = list()
	
		#help button
		self.help_button = Button(self, text="Help")
		self.help_button["command"] = self.helpbox
		
		self.help_button.grid(row=1, column=10, padx=5)
	
		#The eventual add button
		self.add_button = Button(self, text="Add Song")
		self.add_button["command"] = self.add_song

		self.add_button.grid(row=3, column=10, padx=5)
		
		#The remove button
		self.remove_button = Button(self, text="Remove Song")
		self.remove_button["command"] = self.remove_song

		self.remove_button.grid(row=4, column=10, padx=5)
		
		#The clear button
		self.clear_button = Button(self, text="Clear Songs")
		self.clear_button["command"] = self.clear_songs

		self.clear_button.grid(row=5, column=10, padx=5)
		
		#The import text button
		self.import_text_button = Button(self, text="Import as Textfile")
		self.import_text_button["command"] = self.import_text

		self.import_text_button.grid(row=10, column=0, pady=5)

		#The export text button
		self.export_text_button = Button(self, text="Export as Textfile")
		self.export_text_button["command"] = self.export_text

		self.export_text_button.grid(row=10, column=1, pady=5)

		#The gmusic button
		self.gMusic_button = Button(self, text="Export to Google Music")
		self.gMusic_button["command"] = self.export_gmusic

		self.gMusic_button.grid(row=10, column=2, padx=5,)

		#The webscrape button
		self.webscrape_button = Button(self, text="Import from Website")
		self.webscrape_button["command"] = self.scrape

		self.webscrape_button.grid(row=8, column=10, padx=5, pady=5)

	
	def on_exit(self):
		self.quit()
	
	def __init__(self, master=None):
		f = Frame.__init__(self, master, height=1280, width=1920)
		self.grid()
		master.protocol("WM_DELETE_WINDOW", self.on_exit)
		
		#label for playlist viewer
		self.playlist_label = Label(text="Active Playlist")
		self.playlist_label.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
		
		
		
		#The playlist viewer
		scrollbar = Scrollbar(self, orient=VERTICAL)
		self.playlist_viewer = Listbox(self, selectmode=MULTIPLE, height=30, width=100, yscrollcommand=scrollbar.set)
		
		#self.updatePlaylist()
		
		scrollbar.config(command=self.playlist_viewer.yview)
		self.playlist_viewer.grid(row=2, rowspan=8, columnspan=7, padx=5, sticky="nesw")
		scrollbar.grid(row=2, column=8, rowspan=8, sticky="sn")
		
		self.createWidgets()
		
	
	

root = Tk()
root.title("DittyGetty")

app = Application(master=root)
app.mainloop()

#Destroys after the mainloop is finished
root.destroy()
