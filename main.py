from Tkinter import *
from jpr import *
from songInfo import *
from gmusic import *
import tkFileDialog
import tkMessageBox
import ttk

#The current playlist that is viewed, needs to be global.

playlist = list()

class Application(Frame):
	
	#These aren't working atm
	# def limitSongSize(self):
		# value = self.songVar.get()
		# if len(value) > 20: songVar.set(value[:20])
	
	# def limitArtistSize(self):
		# value = self.artistVar.get()
		# if len(value) > 20: artistVar.set(value[:20])

	#Various callback functions for the homepage buttons
	def add_song(self):
		self.add_window = Toplevel(root)
		self.add_window.wm_title("Enter Date and Time")
		
		# self.addSong = ""
		# self.addArtist = ""
		self.add_error = ""
		
		self.add_error = StringVar()
		
		# self.songVar = StringVar()
		# self.songVar.trace('w', self.limitSongSize)
		# self.artistVar = StringVar()
		# self.artistVar.trace('w', self.limitArtistSize)
		
		#Entry field for song name
		self.song_entry = Entry(self.add_window)
		song_label = Label(self.add_window, text="Song Name")
		
		#Entry field for artist name
		self.artist_entry = Entry(self.add_window)
		artist_label = Label(self.add_window, text="Artist Name")
		
		self.add_window.submit_button = Button(self.add_window, text="Submit", command=self.add_confirm)
		
		#Error label
		self.add_error_label = Label(self.add_window, textvariable=self.add_error)

		#place all of the widgets
		song_label.grid(row=1, column=0)
		self.song_entry.grid(row=2, column=0)
		
		artist_label.grid(row=1, column=1)
		self.artist_entry.grid(row=2, column=1)
		
		self.add_window.submit_button.grid(row=2, column=2)
		self.add_error_label.grid(row=3, column=0, columnspan=3)
		
	
	def add_confirm(self):
		global playlist

		# error check for size of artist and song names
		if(len(self.song_entry.get()) > 75 or len(self.song_entry.get()) < 1):
			self.add_error.set("The song needs to be between 1 and 75 characters.")
		elif(len(self.artist_entry.get()) > 75 or len(self.artist_entry.get()) < 1):
			self.add_error.set("The artist needs to be between 1 and 75 characters.")
		else:
			self.add_error.set("")
			#"" is for the time, which if you're manually adding it, then it doesn't matter.
			song = SongInfo('', self.song_entry.get(), self.artist_entry.get())
			playlist.append(song)
			self.playlist_view.insert("", 'end', text=0, values=(song.songName, song.songArtist, song.songTime))
			self.add_window.destroy()
	
	def helpbox(self):
		global playlist
		
		self.help_window = Toplevel(root)
		self.help_window.wm_title("Help")
		options = ["Selection", "Add Song", "Remove Song", "Clear Songs", "Import from Website", "Import as Textfile", "Export as Textfile", "Export to Google Music", ]
		descriptions = ["Click an entry in the active playlist to select. Hold ctrl to select multiple. Hold shift to select consecutive.", "Adds a song to the active playlist.", "Removes all songs that are currently selected from the active playlist.", "Clears all songs from the active playlist.", "Imports a playlist from JPR given a date and range of time.", "Imports a textfile using the format: time || songname || songartist.", "Exports the current playlist as a textfile that uses the format: time || songname || songartist.", "Exports the current playlist to Google Music, will ask for login credentials."]
		
		for i in range(0, len(options)):
			label1 = Label(self.help_window, text=options[i], anchor=W, justify=LEFT)
			label2 = Label(self.help_window, text=descriptions[i], anchor=W, justify=LEFT)
			
			label1.grid(row=i, column=0, sticky=W)
			label2.grid(row=i, column=1, sticky=W)
		#help_label.grid(row=0, column=0, columnspan=2, rowspan=len(options))

		# for song in playlist:
			# print song.toString()
		
		
	def remove_song(self):
		global playlist
		items = self.playlist_view.selection()
		count = 0
		for item in items:
			#del playlist[item - count]
			#print self.playlist_view.index(item)
			del playlist[self.playlist_view.index(item) - count]
			self.playlist_view.delete(item)
			#print(self.playlist_view.get(item - count))
			#count += 1
			
		
	def clear_songs(self):
		global playlist
		playlist = list()
		self.playlist_view.delete(*self.playlist_view.get_children())
		print "Clear!"
		
	def import_text(self):
		global playlist
		filename = tkFileDialog.askopenfilename()
		file = open(filename, 'r')

		if file is None:
			return

		#clear playlist
		playlist = list()
		self.playlist_view.delete(*self.playlist_view.get_children())

		for line in file:
			trimmedLine = line.replace('\n', "")
			nameArtist = trimmedLine.split("||")
			song = SongInfo(nameArtist[1], nameArtist[2], nameArtist[0])
			playlist.append(song)

		self.updatePlaylist()

		
	def export_text(self):
		global playlist
		
		#If the playlist is empty
		if len(playlist) is 0:
			export_error_window = Toplevel(root)
			export_error_window.wm_title("Error")
			label = Label(export_error_window, text="Can't export an empty playlist.")
			button = Button(export_error_window, text="Okay", command=export_error_window.destroy)
			label.grid(row=0, column=0, padx=10, pady=10)
			button.grid(row=1, column=0, padx=10)
			
		
		#If not empty, write to file
		else:
			f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")
			if f is None:
				return

			for song in playlist:
				f.write("%s||%s||%s\n" % (song.songTime, song.songName, song.songArtist))

			f.close()

	def login_gmusic(self):

		#login to gmusic
		self.t2 = Toplevel(root)
		self.t2.wm_title("Login")

		self.username = ""
		self.playlist_username_entry = Entry(self.t2)
		playlist_username_label = Label(self.t2, text="Email")

		self.password = ""
		self.playlist_password_entry = Entry(self.t2, show="*")
		playlist_password_label = Label(self.t2, text="Password")

		self.t2.submit_button2 = Button(self.t2, text="Submit", command=self.export_gmusic)	

		playlist_username_label.grid(row=1, column=0)
		self.playlist_username_entry.grid(row=2, column=0)

		playlist_password_label.grid(row=1, column=2)
		self.playlist_password_entry.grid(row=2, column=2)	

		self.t2.submit_button2.grid(row=4, column=1, pady=15, sticky="s")
		
	def export_gmusic(self):
		
		self.playlist_username = self.playlist_username_entry.get()
		self.playlist_password = self.playlist_password_entry.get()

		if not loginGmusic(self.playlist_username, self.playlist_password):
			tkMessageBox.showinfo('Login Failed', 'Login Failure, please check your internet connection and try again')
		else:
			#get playlist name

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
		
		hyphen_label = Label(self.t, text="---")
		
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


		failed_song_list = uploadSongsGmusic(self.playlistName, playlist)

		if failed_song_list:
			str_failed_songs = ""
			count = 0
			for songs in failed_song_list:
				str_failed_songs += (str(count) + ": " + songs.toString() + "\n\n")
				count += 1


			tkMessageBox.showinfo('Playlist Creation', 'Creation of playlist: %s successful!\n\n Failed Songs:\n%s' % (self.playlistName, str_failed_songs))
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
	
	#Updates the playlist in the viewer to match the playlist variable
	def updatePlaylist(self):
		global playlist
		
		# for song in playlist:
			# print song
		self.playlist_view.delete(*self.playlist_view.get_children())
		for song in playlist:
			self.playlist_view.insert("", 'end', text=1, values=(song.songTime, song.songName, song.songArtist))
		print 'update playlist was called'
	
		
		
	def createWidgets(self):
		#self.playlist = list()
	
		#help button
		self.help_button = Button(self, text="Help")
		self.help_button["command"] = self.helpbox
		
		self.help_button.grid(row=1, column=5, padx=5)
	
		#The eventual add button
		self.add_button = Button(self, text="Add Song")
		self.add_button["command"] = self.add_song

		self.add_button.grid(row=3, column=5, padx=5)
		
		#The remove button
		self.remove_button = Button(self, text="Remove Song")
		self.remove_button["command"] = self.remove_song

		self.remove_button.grid(row=4, column=5, padx=5)
		
		#The clear button
		self.clear_button = Button(self, text="Clear Songs")
		self.clear_button["command"] = self.clear_songs

		self.clear_button.grid(row=5, column=5, padx=5)
		
		#The import text button
		self.import_text_button = Button(self, text="Import as Textfile")
		self.import_text_button["command"] = self.import_text

		self.import_text_button.grid(row=10, column=1, pady=5)

		#The export text button
		self.export_text_button = Button(self, text="Export as Textfile")
		self.export_text_button["command"] = self.export_text

		self.export_text_button.grid(row=10, column=2, pady=5)

		#The gmusic button
		self.gMusic_button = Button(self, text="Export to Google Music")
		self.gMusic_button["command"] = self.login_gmusic

		self.gMusic_button.grid(row=10, column=3, padx=5,)

		#The webscrape button
		self.webscrape_button = Button(self, text="Import from Website")
		self.webscrape_button["command"] = self.scrape

		self.webscrape_button.grid(row=8, column=5, padx=5, pady=5)

	
	def on_exit(self):
		self.quit()
	
	def __init__(self, master=None):
		f = Frame.__init__(self, master, height=1280, width=1920)
		self.grid()
		master.protocol("WM_DELETE_WINDOW", self.on_exit)
		
		#label for playlist viewer
		
		
		
		#The playlist viewer
		scrollbar = Scrollbar(self, orient=VERTICAL)
		#self.playlist_viewer_name = Listbox(self, exportselection=0, selectmode=MULTIPLE, height=30, width=25, yscrollcommand=scrollbar.set)
		#self.playlist_viewer_artist = Listbox(self, exportselection=0, selectmode=MULTIPLE, height=30, width=25, yscrollcommand=scrollbar.set)
		
		#self.updatePlaylist()
		

		#self.playlist_viewer_name.grid(row=2, column=1, rowspan=8, sticky="nesw")
		#self.playlist_viewer_artist.grid(row=2, column=2, rowspan=8, sticky="nesw")


		
		self.playlist_view = ttk.Treeview(self, height=30, yscrollcommand=scrollbar.set)
		self.playlist_view["columns"]=("zero", "one", "two")
		self.playlist_view.column("zero", width=150)
		self.playlist_view.column("one", width=250)
		self.playlist_view.column("two", width=250)
		self.playlist_view.heading("zero", text="Time")
		self.playlist_view.heading("one", text="Name")
		self.playlist_view.heading("two", text="Artist")

		#to get rid of first empty column
		self.playlist_view['show'] = 'headings'

		scrollbar.config(command=self.playlist_view.yview)

		self.playlist_view.grid(row=2, column=1, rowspan=8, columnspan=3, padx=5, sticky="nesw")
		scrollbar.grid(row=2, column=4, rowspan=8, sticky="nsw")

		#listbox callback for selecting multiple columns
		
		
		self.createWidgets()

		self.playlist_label_name = Label(self, text="Playlist Viewer")
		self.playlist_label_name.grid(row=1, column=2)
		
	
	

root = Tk()
root.title("DittyGetty")

app = Application(master=root)
app.mainloop()

#Destroys after the mainloop is finished
root.destroy()
