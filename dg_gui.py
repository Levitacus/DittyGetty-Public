from Tkinter import *
from songInfo import *
from gmusic import *
from threading import *
from playlist import *
from config import Config
from npr import NPR
from helperFuncs import *
from daily_playlist import DailyPlaylist
import tkFileDialog
import tkMessageBox
import ttk
import re
import urllib2
import string



#The current playlist that is viewed, needs to be global.
playlist = Playlist()

class Application(Frame):
	'''
        GUI application
    '''
	#deletes child windows of root
	def delete_child_windows(self):
		count = True
		children_list = root.winfo_children()
		for children in children_list:
			
			if(count) or isinstance(children, Menu):
				count = False
			else:
				children.destroy()
		

	#Various callback functions for the homepage buttons
	def add_song_option(self):
		'''
			Callback function for add song button
			Gets artist and song name
		'''
		self.delete_child_windows()
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
		
		self.add_window.submit_button = Button(self.add_window, text="Submit", command=self.add_song)
		#bind enter to submit button
		self.add_window.bind("<Return>", lambda e: self.add_song())

		#Error label
		self.add_error_label = Label(self.add_window, textvariable=self.add_error)

		#place all of the widgets
		song_label.grid(row=1, column=0)
		self.song_entry.grid(row=2, column=0)
		
		artist_label.grid(row=1, column=1)
		self.artist_entry.grid(row=2, column=1)
		
		self.add_window.submit_button.grid(row=2, column=2)
		self.add_error_label.grid(row=3, column=0, columnspan=3)

		self.center_window(self.add_window)
		
	
	def add_song(self):
		'''
			Callback function for add_song_option submit button
			Adds the song artist pair to the playlist
		'''
		global playlist

		# error check for size of artist and song names
		if(len(self.song_entry.get()) > 75 or len(self.song_entry.get()) < 1):
			self.add_error.set("The song needs to be between 1 and 75 characters.")
		elif(len(self.artist_entry.get()) > 75 or len(self.artist_entry.get()) < 1):
			self.add_error.set("The artist needs to be between 1 and 75 characters.")
		else:
			self.add_error.set("")
			#'' in SongInfo is for the time, which if you're manually adding it, then it doesn't matter.
			song = SongInfo(self.song_entry.get(), self.artist_entry.get(), '')
			#playlist.append(song)
			playlist.add(song)
			self.playlist_view.insert("", 'end', text=0, values=(song.songTime, song.songName, song.songArtist))
			self.add_window.destroy()
	
	def helpbox(self):
		'''
			Callback function for the help button
			Gives the user instructions to operate the gui
		'''
		
		self.help_window = Toplevel(root, width="500")
		self.help_window.wm_title("Help")
		options = ["Selection", "Add Song", "Remove Song", "Clear Songs", "Import from Website", "Import as Textfile", "Export as Textfile", "Export to Google Music", ]
		descriptions = ["Click an entry in the active playlist to select. Hold ctrl to select multiple. Hold shift to select consecutive.", "Adds a song to the active playlist.", "Removes all songs that are currently selected from the active playlist.", "Clears all songs from the active playlist.", "Imports a playlist from JPR given a date and range of time. Format: dd mm yyyy. hh:mm or hh:mm AM/PM", "Imports a textfile using the format: time || songname || songartist.", "Exports the current playlist as a textfile that uses the format: time || songname || songartist.", "Exports the current playlist to Google Music, will ask for login credentials."]
		
		for i in range(0, len(options)):
			label1 = Label(self.help_window, text=options[i], anchor=W, justify=LEFT)
			label2 = Label(self.help_window, text=descriptions[i], anchor=W, justify=LEFT)
			
			label1.grid(row=i, column=0, sticky=W)
			label2.grid(row=i, column=1, sticky=W)
		self.center_window(self.help_window)
		#help_label.grid(row=0, column=0, columnspan=2, rowspan=len(options))
		
	def remove_song(self):
		'''
			Callback function for the remove button
			Removes the selected songs from the playlist
		'''
		global playlist
		items = self.playlist_view.selection()
		#count = 0
		for item in items:
			#del playlist[self.playlist_view.index(item) - count]
			playlist.remove(self.playlist_view.index(item))
			self.playlist_view.delete(item)
			
		
	def clear_songs(self):
		'''
			Callback function for the clear button
			Clears the active playlist
		'''
		global playlist
		#playlist = list()
		playlist.clear()
		self.playlist_view.delete(*self.playlist_view.get_children())
		
	def import_text(self):
		'''
			Callback function for the import_text_button
			Imports from a text file
		'''
		global playlist
		self.delete_child_windows()
		filename = tkFileDialog.askopenfilename()
		try:
			file = open(filename, 'r')
		except:
			file = None
			
		if file is None:
			tkMessageBox.showinfo('Import Text', 'Error: File Not Found')
			
		else:	
			playlist.clear()
			self.playlist_view.delete(*self.playlist_view.get_children())
			
			try:
				for line in file:
					line.encode('ascii', 'ignore')
					trimmedLine = line.replace('\n', "")
					nameArtist = trimmedLine.split("||")
					song = SongInfo(nameArtist[1], nameArtist[2], nameArtist[0])
					#playlist.append(song)
					playlist.add(song)

				self.updatePlaylist()
				self.update_logical_playlist()
			except:
				tkMessageBox.showinfo('Import Text', 'Incorrect file format\nentries should be listed as:\n(TIME)||(SONG TITLE)||(SONG ARTIST)\nTime section can be left blank')

		
	def export_text(self):
		'''
			Callback function for the export_text_button
			Exports to a textfile
		'''
		self.delete_child_windows()
		global playlist
		
		#If the playlist is empty
		if len(playlist.get()) is 0:
			tkMessageBox.showinfo('Export Text', "Can't export an empty playlist.")
			
		
		#If not empty, write to file
		else:
			f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")
			if f is None:
				return

			for song in playlist.get():
				f.write("%s||%s||%s\n" % (song.songTime, song.songName, song.songArtist))

			f.close()
	
	def import_gmusic(self, event=None):
		'''
			Callback function for the gMusic_button
			Has the user login and checks their credentials
		'''
		if self.submit_button2['state'] == 'disabled':
			return

		playlist_username = self.playlist_username_entry.get()
		playlist_password = self.playlist_password_entry.get()

		if not loginGmusic(playlist_username, playlist_password):
			tkMessageBox.showinfo('Login Failed', 'Login Failure, please check your internet connection and try again')
		else:
		
			self.json_config['username'] = playlist_username
			self.json_config['password'] = playlist_password
			
			playlists_dict = gmusic_get_playlists_content()

			#close window asking for pass and email
			self.gmusic_window.destroy()

			#get playlist name
			self.gmusic_window3 = Toplevel(root)
			self.gmusic_window3.wm_title("Export")

			playlist_name_label = Label(self.gmusic_window3, text="Choose playlist to import")
			
			#list of playlists with scrollbar
			scrollbar = Scrollbar(self.gmusic_window3, orient=VERTICAL)
			self.playlists_listbox = Listbox(self.gmusic_window3, selectmode=SINGLE, width=50, yscrollcommand=scrollbar.set)
			scrollbar.config(command=self.playlists_listbox.yview)

			for dicts in playlists_dict:
				#print(dicts['name'])
				self.playlists_listbox.insert(END, dicts['name'])

			self.gmusic_window3.submit_button2 = Button(self.gmusic_window3, text="Submit", command= lambda: self.import_gmusic_run(playlists_dict))	

			#place the components
			playlist_name_label.grid(row=0, column=0, sticky='ew')
			self.playlists_listbox.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
			scrollbar.grid(row=1, column=1, sticky='wns')
			self.gmusic_window3.submit_button2.grid(row=2, column=0)

			self.center_window(self.gmusic_window3)

	def import_gmusic_run(self, playlists_dict):
		'''
			Callback function for the submit_button2
			Imports selected playlist from gmusic
		'''
		global playlist
			
		select_tuple = self.playlists_listbox.curselection()
		#if a playlist is selected
		if(select_tuple):
			playlist_select_index = int(select_tuple[0])
			track_list = playlists_dict[playlist_select_index]['tracks']
			
			gmusic_songs = []

			for track in track_list:
				gmusic_songs.append(SongInfo(track['track']['title'].encode('ascii', 'ignore'), track['track']['artist'].encode('ascii', 'ignore')))

			try:
				playlist.set(gmusic_songs)
				self.updatePlaylist()
				#self.scrape_window.destroy()
			except urllib2.URLError:
				self.scrape_error.set("No songs found in playlist")

		else:
			self.gmusic_window3.destroy()
	
	#enable login button function
	def button_enable(self, *args):
		'''
			Enables the login button if there is a user and pass in the fields
		'''
		username = self.default_name.get()
		password = self.default_pass.get()

		if username and password:
			self.submit_button2.config(state='normal')
		else:
			self.submit_button2.config(state='disabled')

	#def button_bind_check(self, dependent_button, command_arg):
		#if button['state'] == 'normal':
			#command_arg

	def login_gmusic(self, command_arg):
		'''
			Brings up a login window for google music
		'''
		#login to gmusic
		self.delete_child_windows()
		self.gmusic_window = Toplevel(root)
		self.gmusic_window.wm_title("Login")


		try:
			#get the username
			username = self.json_config['username']
		except:
			username = ''
		try:
			password = self.json_config['password']
		except Exception as e:
			password = ''
			
		self.default_name = StringVar(root)
		self.default_pass = StringVar(root)
		self.default_name.trace('w', self.button_enable)
		self.default_pass.trace('w', self.button_enable)

		self.playlist_username_entry = Entry(self.gmusic_window, textvariable=self.default_name)
		playlist_username_label = Label(self.gmusic_window, text="Email")

		self.playlist_password_entry = Entry(self.gmusic_window, show="*", textvariable=self.default_pass)
		playlist_password_label = Label(self.gmusic_window, text="Password")

		self.submit_button2 = Button(self.gmusic_window, text="Submit", command=command_arg, state='disabled')
		
		#set the stringargs
		self.default_name.set(username)
		self.default_pass.set(password)

		self.gmusic_window.bind("<Return>", command_arg)

		playlist_username_label.grid(row=1, column=0)
		self.playlist_username_entry.grid(row=2, column=0)

		playlist_password_label.grid(row=1, column=2)
		self.playlist_password_entry.grid(row=2, column=2)	

		self.submit_button2.grid(row=4, column=1, pady=15, sticky="s")
		self.center_window(self.gmusic_window)
		
	def export_gmusic(self, event=None):
		'''
			Callback function for export gmusic button
			Logs in and brings up a list of playlists
		'''
		if self.submit_button2['state'] == 'disabled':
			return

		playlist_username = self.playlist_username_entry.get()
		playlist_password = self.playlist_password_entry.get()

		if not loginGmusic(playlist_username, playlist_password):
			tkMessageBox.showinfo('Login Failed', 'Login Failure, please check your internet connection and try again')
		else:
		
			self.json_config['username'] = playlist_username
			self.json_config['password'] = playlist_password
			
			playlists_dict = gmusic_get_playlists()

			#close window asking for pass and email
			self.gmusic_window.destroy()

			#get playlist name
			self.gmusic_window2 = Toplevel(root)
			self.gmusic_window2.wm_title("Export")

			self.playlistName = ""
			default_name = StringVar(root, value='New playlist name')
			self.playlist_name_entry = Entry(self.gmusic_window2, width=50, textvariable=default_name)
			playlist_name_label = Label(self.gmusic_window2, text="Choose pre-existing playlist to add to or enter a new playlist name.")
			
			#List of playlists with scrollbar
			scrollbar = Scrollbar(self.gmusic_window2, orient=VERTICAL)
			self.playlists_listbox = Listbox(self.gmusic_window2, selectmode=SINGLE, width=50, yscrollcommand=scrollbar.set)
			scrollbar.config(command=self.playlists_listbox.yview)

			for dicts in playlists_dict:
				#print(dicts['name'])
				self.playlists_listbox.insert(END, dicts['name'])

			
			self.merge_bool = IntVar()
			self.merge_check = Checkbutton(self.gmusic_window2, text="Merge(remove duplicates)", var=self.merge_bool)

			#use lambda expression to pass arguments to export_gmusic_run function
			self.gmusic_window2.submit_button2 = Button(self.gmusic_window2, text="Submit", command= lambda: self.export_gmusic_run(playlists_dict))

			#place the components
			self.playlists_listbox.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
			playlist_name_label.grid(row=0, column=0, sticky='ew')
			self.merge_check.grid(row=2, column=0)
			scrollbar.grid(row=1, column=1, sticky="nsw")
			self.playlist_name_entry.grid(row=3, column=0)	
			self.gmusic_window2.submit_button2.grid(row=4, column=0)

			self.center_window(self.gmusic_window2)
		
	def scrape_options(self):
		self.delete_child_windows()
		scrape_option_window = Toplevel(root, height=500, width=500)
		scrape_option_window.wm_title("Scrape Option")
		site_choice = StringVar()
		
		#options
		combobox_values = ['Jefferson Public Radio', 'Jefferson Public Radio - Classics', 'KLCC', 'Daily Playlist']
		
		label = Label(scrape_option_window, text="Choose a website to scrape.")
		site_combobox = ttk.Combobox(scrape_option_window, textvariable=site_choice, values=combobox_values)
		submit = Button(scrape_option_window, text="Choose", command= lambda: self.determine_site(site_combobox.get()))
		
		scrape_option_window.bind("<Return>", lambda e: self.determine_site(site_combobox.get()))
		
		label.grid(row=1, column=3, rowspan=2, columnspan=5, padx=50)
		site_combobox.grid(row=3, column=3, rowspan=2, columnspan=5, padx=50, pady=(10,20))
		submit.grid(row=5, column=3, columnspan=5, padx=50, pady=(0, 50))
		
		self.center_window(scrape_option_window)

	def determine_site(self, site):
		if site is None:
			pass
		elif site == 'Jefferson Public Radio' or site == 'JPR' or site == 'jpr':
			self.npr_scrape('520a4969e1c85ef575dd2484')
		
		elif site == 'JPR - Classics':
			self.npr_scrape('520a42b0e1c8eb30d9d7f0b7')

		elif site == 'KLCC':
			self.npr_scrape('520a4984e1c8e13a9ec5e282')
		
		elif site == 'Daily Playlist':
			self.dp_scrape()
		else:
			#maybe a URL the user enters
			pass
			
	def dp_scrape(self):
		'''
			Asks for name of daily playlist
			Stores the previous daily playlist playlists in the json file
		'''
		self.delete_child_windows()
		self.dp_scrape_window = Toplevel(root, height=500, width=500)
		self.dp_scrape_window.wm_title("Scrape Option")
		site_choice = StringVar()
		combobox_values = ['hip-hop-daily', 'house-daily', 'rock-daily']
		try:
			combobox_values = self.json_config['daily_playlist']
		except KeyError:
			self.json_config['daily_playlist'] = combobox_values
		
		label = Label(self.dp_scrape_window, text="Choose a daily playlist to scrape.")
		dp_combobox = ttk.Combobox(self.dp_scrape_window, textvariable=site_choice, values=combobox_values)
		submit = Button(self.dp_scrape_window, text="Choose", command= lambda: self.dp_playlist(dp_combobox.get()))
		
		self.dp_scrape_window.bind("<Return>", lambda e: self.dp_playlist(dp_combobox.get()))
		
		label.grid(row=1, column=3, rowspan=2, columnspan=5, padx=50)
		dp_combobox.grid(row=3, column=3, rowspan=2, columnspan=5, padx=50, pady=(10,20))
		submit.grid(row=5, column=3, columnspan=5, padx=50, pady=(0, 50))
		self.center_window(self.dp_scrape_window)
		pass
		
	def dp_playlist(self, daily_playlist):
		'''
			Scrapes from dailyplaylists.com
			with the given list name
		'''
		global playlist
		dp = DailyPlaylist(daily_playlist)
		try:
			playlist.set(dp.scrape_run())
			self.updatePlaylist()
			if daily_playlist not in self.json_config['daily_playlist']:
				self.json_config['daily_playlist'].append(daily_playlist)
			self.dp_scrape_window.destroy()
		except:
			tkMessageBox.showinfo('DailyPlaylist Import', 'That playlist doesn\'t exist')
	
	def npr_scrape(self, station):
		'''
			Asks for date and time to scrape JPR
		'''
		self.delete_child_windows()
		self.scrape_window = Toplevel(root)
		self.scrape_window.wm_title("Enter Date and Time")
		
		#error variable
		self.scrape_error = ""
		self.scrape_error = StringVar()
		
		#t.month_entry = Entry(t, textvariable=self.month)
		self.month_entry = EntryAdvanced(self.scrape_window, 'MM')
		month_label = Label(self.scrape_window, text="Enter Month here")
		
		#t.day_entry = Entry(t, textvariable=self.day)
		self.day_entry = EntryAdvanced(self.scrape_window, 'DD')
		day_label = Label(self.scrape_window, text="Enter Day here")
		
		#t.year_entry = Entry(t, textvariable=self.year)
		self.year_entry = EntryAdvanced(self.scrape_window, 'YYYY')
		year_label = Label(self.scrape_window, text="Enter Year here")
		
		self.startTime_entry = EntryAdvanced(self.scrape_window, '00:00AM')
		startTime_label = Label(self.scrape_window, text="Start Time")
		
		self.endTime_entry = EntryAdvanced(self.scrape_window, '00:00AM')
		endTime_label = Label(self.scrape_window, text="End Time")
		
		hyphen_label = Label(self.scrape_window, text="---")

		
		#important that the callback function here just references the command, not passing it
		self.scrape_window.submit_button = Button(self.scrape_window, text="Submit")
		self.scrape_window.submit_button["command"] = lambda: self.jpr_playlist(station)
		#bind enter key to submit button
		self.scrape_window.bind("<Return>", lambda e: self.jpr_playlist(station))

		#error label
		self.scrape_error_label = Label(self.scrape_window, textvariable=self.scrape_error)
		

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
		
		self.scrape_window.submit_button.grid(row=5, column=1)
		self.scrape_error_label.grid(row=6, column=0, columnspan=3)

		self.center_window(self.scrape_window)
	
	def jpr_playlist(self, station_code):
		'''
			Callback function for the jpr_scrape() submit_button
			Actually scrapes the website
		'''
		global playlist
		
		month = self.month_entry.get()
		day = self.day_entry.get()
		year = self.year_entry.get()
		startTime = self.startTime_entry.get()
		endTime = self.endTime_entry.get()
		
		#The regex checks
		month_check = re.match('0*([1-9]|0[1-9]|[1][0-2])$', month)
		day_check = re.match('0*([1-9]|0[1-9]|[1-2][0-9]|[3][0-1])$', day)
		year_check = re.match('(20[2-9][0-9]|201[4-9])$', year)
		start_check = re.match('([1-9]|[0-1][0-9]|[2][0-4]):[0-5][0-9]|([1-9]|[0-1][0-2]):[0-5][0-9](AM|PM|am|pm)$', startTime)
		end_check = re.match('([1-9]|[0-1][0-9]|[2][0-4]):[0-5][0-9]|([1-9]|[0-1][0-2]):[0-5][0-9](AM|PM|am|pm)$', endTime)
		
		if month_check is None:
			self.scrape_error.set("Please enter a month between 1-12 in mm format.")
		elif day_check is None:
			self.scrape_error.set("Please enter a day between 1-31 in dd format.")
		elif year_check is None:
			self.scrape_error.set("Please enter a year after 2013 in yyyy format.")
		elif start_check is None:
			self.scrape_error.set("Please enter a valid start time in hh:mm format or hh:mm AM/PM format.")
		elif end_check is None:
			self.scrape_error.set("Please enter a valid end time in hh:mm format or hh:mm AM/PM format.")
		else:
			month_int, day_int, year_int = int(month), int(day), int(year)
			#call getList function from jpr.py
			try:
				jpr = NPR(station_code)
				playlist.set(jpr.scrape_run(month_int, day_int, year_int, startTime, endTime))
				self.updatePlaylist()
				self.scrape_window.destroy()
			except urllib2.URLError:
				self.scrape_error.set("No data available for selected time")
				
	
	def export_gmusic_run(self, playlists_dict):
		'''
			Callback function for the submit_button 
			Runs the export to gmusic
		'''
		global playlist
		
		self.failed_song_list = []
		
		ids_list = []
		existing = False
		
		length = len(playlist.get())

		
		select_tuple = self.playlists_listbox.curselection()
		#if a playlist is selected
		if(select_tuple):
			playlist_select_index = int(select_tuple[0])
			self.playlistName = playlists_dict[playlist_select_index]['name']
			self.playlistID = playlists_dict[playlist_select_index]['id']
			#self.failed_song_list = uploadSongsGmusic(playlists_dict[playlist_select_index]['id'], playlist.get(), existing=True, merge=self.merge_bool.get())
			existing = True
			
		else:
			#no selection
			playlist_select_index = 0
			self.playlistName = self.playlist_name_entry.get()
			self.playlistID = self.playlistName
			#self.failed_song_list = uploadSongsGmusic(self.playlistName, playlist.get())

		self.loading_window_run("Loading", len(playlist.get()))
			
		i = 0

		for song in playlist.get():
				song_id = find_store_id(song)

				if(song_id):
					ids_list.append(song_id)
				else:
					self.failed_song_list.append(song)
				i += 1
				self.step(i)
			
		test = upload_ids_gmusic(self.playlistID, ids_list, existing, merge=self.merge_bool.get())

		#print(playlist_select_index)

		#if failed songs is a list and has entries
		if len(self.failed_song_list) > 0 and isinstance(self.failed_song_list, list):
			str_failed_songs = ""
			count = 1
			for songs in self.failed_song_list:
				str_failed_songs += (str(count) + ": " + songs.toString() + "\n\n")
				count += 1
			
			missed_string = ('Creation of playlist: %s successful!\n\n Failed Songs:\n%s' % (self.playlistName, str_failed_songs))

			#create a new window that has the option to save to a textfile
			self.missed_songs_window = Toplevel(root)
			self.missed_songs_window.wm_title("Missed Songs")

			# create a Frame for the Text and Scrollbar
			txt_frm = Frame(self.missed_songs_window, width=600, height=600)
			txt_frm.pack(fill="both", expand=True)
			# ensure a consistent GUI size
			txt_frm.grid_propagate(False)
			# implement stretchability
			txt_frm.grid_rowconfigure(0, weight=1)
			txt_frm.grid_columnconfigure(0, weight=1)

		    	# create a Text widget
			self.txt = Text(txt_frm, borderwidth=3, relief="sunken")
			self.txt.insert(END, missed_string)
			self.txt.config(font=("consolas", 12), undo=True, wrap='word')
			self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

		    	# create a Scrollbar and associate it with txt
			scrollb = Scrollbar(txt_frm, command=self.txt.yview)
			scrollb.grid(row=0, column=1, sticky='nsew')
			self.txt['yscrollcommand'] = scrollb.set
			
			missed_songs_label = Label(self.missed_songs_window, text=missed_string, bg="white", anchor='w')
			ok_button = Button(self.missed_songs_window, text="Okay", command=self.missed_songs_window.destroy)
			self.export_missed_songs_button = Button(self.missed_songs_window, text="Export to Textfile", command=self.export_missed_songs)
			
			#Place the label and the buttons.
			#missed_songs_label.grid(row=0, column=1, columnspan=3)
			
			#ok_button.grid(row=1, column=1)
			ok_button.pack()
			self.export_missed_songs_button.pack()
			#self.export_missed_songs_button.grid(row=1, column=2)
		#if failed songs exists but has no entries
		elif test:
			tkMessageBox.showinfo('Playlist Creation', 'Creation of playlist: %s Successful!' % (self.playlistName))
		else:
			tkMessageBox.showinfo('Playlist Creation Error', 'Creation of playlist: %s unsuccessful!' % (self.playlistName))
		
		self.gmusic_window2.destroy()
	
	def export_missed_songs(self):
		'''
			Callback function for export_missed_songs_button
			Export missed songs to a textfile
		'''
		if len(self.failed_song_list) is 0:
			tkMessageBox.showinfo('Export Text', "Can't export an empty playlist.")
		
		#If not empty, write to file
		else:
			f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")
			if f is None:
				return

			for song in self.failed_song_list:
				f.write("%s||%s||%s\n" % (song.songTime, song.songName, song.songArtist))

			f.close()
		self.missed_songs_window.destroy()
		
	def loading_window_run(self, title="Loading Bar", progress_increments=100):
		self.loading_window = Toplevel(self, width=200, height=100)
		self.loading_window.title(title)
		self.loading_label = Label(self.loading_window, text='Exporting playlist...', anchor='w')
		self.loading_bar = ttk.Progressbar(self.loading_window, orient="horizontal", maximum=100, mode="determinate")
		self.loading_bar["maximum"] = progress_increments
		
		self.loading_label.grid(row=0, column=0, padx=40, pady=20)
		self.loading_bar.grid(row=2, column=0, padx=10, pady=10)
		self.center_window(self.loading_window)
		#self.loading_bar.pack()

		
		
	
	def step(self, num_items):
		global root
		self.loading_bar["value"] = num_items
		self.loading_window.update()
		if self.loading_bar["maximum"] <= num_items:
			self.loading_window.destroy()




	def center_window(self, window):
		window.update_idletasks()

		w = window.winfo_width()
		h = window.winfo_height()

		#find screen width and height
		screen_width = window.winfo_screenwidth()
		screen_height = window.winfo_screenheight()

		size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
		x = screen_width/2 - size[0]/2
		y = screen_height/2 - size[1]/2

		window.geometry("%dx%d+%d+%d" % (w, h, x, y))

	
	
	#Updates the playlist in the viewer to match the playlist variable
	def updatePlaylist(self):
		global playlist
	
		self.playlist_view.delete(*self.playlist_view.get_children())
		for song in playlist.get():
			self.playlist_view.insert("", 'end', text=1, values=(song.songTime, song.songName, song.songArtist))
		#print 'update playlist was called'
	
	def create_toolbar(self):
		#creating toolbar
		menubar = Menu(self.master)
		self.master.config(menu=menubar)

		#File
		file_menu = Menu(menubar)
		menubar.add_cascade(label="File", menu=file_menu)
		file_menu.add_command(label="Save Playlist", command=self.export_text)
		file_menu.add_command(label="Load Playlist", command=self.import_text)
		file_menu.add_command(label="Exit", command=self.on_exit)
		#Edit
		edit_menu = Menu(menubar)
		menubar.add_cascade(label="Edit", menu=edit_menu)
		edit_menu.add_command(label="Add Song", command=self.add_song_option)
		edit_menu.add_command(label="Remove Song", command=self.remove_song)
		edit_menu.add_command(label="Clear Songs", command=self.clear_songs)
		#Import
		import_menu = Menu(menubar)
		menubar.add_cascade(label="Import", menu=import_menu)
		import_menu.add_command(label="Playlist From Website", command=self.scrape_options)
		import_menu.add_command(label="Google Music", command=lambda: self.login_gmusic(self.import_gmusic))
		
		#Export
		export_menu = Menu(menubar)
		menubar.add_cascade(label="Export", menu=export_menu)
		export_menu.add_command(label="Google Music", command=lambda: self.login_gmusic(self.export_gmusic))
		#Help
		
	def create_widgets(self):
		
		#help button
		self.help_button = Button(self, text="Help", command=self.helpbox)
		
		self.help_button.grid(row=1, column=6, padx=5)
	
		#The add button
		self.add_button = Button(self, text="Add Song", command=self.add_song_option)

		self.add_button.grid(row=3, column=6, padx=5)
		
		#The remove button
		self.remove_button = Button(self, text="Remove Song", command=self.remove_song)

		self.remove_button.grid(row=4, column=6, padx=5)
		
		#The clear button
		self.clear_button = Button(self, text="Clear Songs", command=self.clear_songs)
		self.clear_button.grid(row=5, column=6, padx=5)
		
		#The import text button
		self.import_text_button = Button(self, text="Import as Textfile", command=self.import_text)

		self.import_text_button.grid(row=10, column=1, pady=5)


		#The export text button
		self.export_text_button = Button(self, text="Export as Textfile", command=self.export_text)

		self.export_text_button.grid(row=10, column=2, pady=5)

		#The gmusic button
		self.gMusic_button = Button(self, text="Export to Google Music")
		self.gMusic_button["command"] = lambda: self.login_gmusic(self.export_gmusic)

		self.gMusic_button.grid(row=10, column=4, padx=5,)

		#The import gmusic button
		self.import_text_button = Button(self, text="Import From Google Music")
		self.import_text_button["command"] = lambda: self.login_gmusic(self.import_gmusic)

		self.import_text_button.grid(row=10, column=3, pady=5)

		#The webscrape button
		self.webscrape_button = Button(self, text="Import from Website", command=self.scrape_options)
		
		self.webscrape_button.grid(row=8, column=6, padx=5, pady=5)

	def b_press(self, event):
		tv = event.widget
		if tv.identify_row(event.y) not in tv.selection():
			tv.selection_set(tv.identify_row(event.y))    
		
	def shift_b_press(self, event):
		tv = event.widget
		select = [tv.index(s) for s in tv.selection()]
		select.append(tv.index(tv.identify_row(event.y)))
		select.sort()
		for i in range(select[0],select[-1]+1,1):
			 tv.selection_add(tv.get_children()[i])   

	def b_release(self, event):
		tv = event.widget
		if tv.identify_row(event.y) in tv.selection():
			tv.selection_set(tv.identify_row(event.y))
		self.update_logical_playlist()
			

	def b_move(self, event):
		tv = event.widget
		moveto = tv.index(tv.identify_row(event.y))    
		for s in tv.selection():
			tv.move(s, '', moveto)
			
			
	# def shift_b_release(self, event):
		# pass
		
	def update_logical_playlist(self):
		global playlist
		
		treeview_playlist = [self.playlist_view.item(child, "values") for child in self.playlist_view.get_children()]
		
		playlist_new = []

		for song in treeview_playlist:
			playlist_new.append(SongInfo(song[1], song[2], song[0]))

		playlist.set(playlist_new)

	def sort_playlist_artist(self):
		try:
			playlist.get().sort(key=lambda song: song.songArtist)
		except:
			pass
		self.updatePlaylist()

	def sort_playlist_name(self):
		try:
			playlist.get().sort(key=lambda song: song.songName)
		except:
			pass
		self.updatePlaylist()

	def sort_playlist_time(self):
		try:
			playlist.get().sort(key=lambda song: timeObject(song.songTime).totalMinutes())
		except:
			pass
		self.updatePlaylist()
	

	def on_exit(self):
		global playlist
		playlist_dict = playlist.to_dict()
		#print playlist_dict
		self.json_config['playlist'] = playlist_dict
		#print(self.json_config)
		self.json_config.save()
		self.quit()
		
	def pass_func(self, event):
		pass
	
	def __init__(self, master=None):
		global playlist
		self.master = master



		f = Frame.__init__(self, master, height=1280, width=1920)
		self.grid()
		master.protocol("WM_DELETE_WINDOW", self.on_exit)
		
        	#json file object
		self.json_config = Config()
        
        	#load json as a dict
		self.json_config.load()
		#print self.json_config
		try:
			playlist.to_playlist((self.json_config['playlist']))
			#print playlist
		except KeyError:
			pass
		
		#The playlist viewer
		scrollbar = Scrollbar(self, orient=VERTICAL)
		self.playlist_view = ttk.Treeview(self, height=30, yscrollcommand=scrollbar.set)
		self.playlist_view["columns"]=("zero", "one", "two")
		self.playlist_view.column("zero", width=150)
		self.playlist_view.column("one", width=250)
		self.playlist_view.column("two", width=250)
		self.playlist_view.heading("zero", text="Time", command=self.sort_playlist_time)
		self.playlist_view.heading("one", text="Name", command=self.sort_playlist_name)
		self.playlist_view.heading("two", text="Artist", command=self.sort_playlist_artist)

		#to get rid of first empty column
		self.playlist_view['show'] = 'headings'

		scrollbar.config(command=self.playlist_view.yview)
		
		self.playlist_view.grid(row=2, column=1, rowspan=8, columnspan=4, padx=5, sticky="nesw")
		scrollbar.grid(row=2, column=5, rowspan=8, sticky="nsw")

		#listbox callback for selecting multiple columns
		self.create_widgets()

		#create toolbar
		self.create_toolbar()

		self.playlist_label_name = Label(self, text="DittyGetty Playlist Viewer", font='helvetica 16')
		self.playlist_label_name.grid(row=1, column=0, columnspan=6)
		
		#playlist view movement
		self.playlist_view.bind('<1>', self.b_press)
		self.playlist_view.bind('<B1-Motion>', self.b_move)
		self.playlist_view.bind('<ButtonRelease-1>', self.b_release)
		self.playlist_view.bind('<Shift-1>', self.pass_func)
		self.playlist_view.bind('<Shift-ButtonRelease-1>', self.pass_func)
		self.playlist_view.bind('<Control-1>', self.pass_func)
		self.playlist_view.bind('<Control-ButtonRelease-1>', self.pass_func)
		

		#update playlist
		self.updatePlaylist()
		

#for advanced entry fields, can have placeholder values and enable/disable buttons
class EntryAdvanced(Entry):
	def __init__(self, master=None, placeholder="DEFAULT TEXT", button_connect=None):
		Entry.__init__(self, master)

		self.placeholder = placeholder
		self.fg_color = 'grey'
		self.default_fg_color = self['fg']
		self.connected_button = button_connect

		self.bind("<FocusIn>", self.focus)
		self.bind("<FocusOut>", self.unfocus)

		self.put_placeholder()

	def put_placeholder(self):
		self.insert(0, self.placeholder)
		self['fg'] = self.fg_color

	def remove_placeholder(self):
		self.delete('0', 'end')
		self['fg'] = self.default_fg_color

	def focus(self, *args):
		if self['fg'] == self.fg_color:
			self.remove_placeholder()
			if self.connected_button:
				self.connected_button.config(state='normal')

	def unfocus(self, *args):
		if not self.get():
			self.put_placeholder()
			if self.connected_button:
				self.connected_button.config(state='disabled')
		
	
def main():
	global root
	root = Tk()
	root.title("DittyGetty")
	app = Application(master=root)
	app.mainloop()


	#Destroys after the mainloop is finished
	root.destroy()

if __name__ == "__main__":
	main()

