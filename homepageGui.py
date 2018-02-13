from Tkinter import *
from jpr import *

#The current playlist that is viewed, needs to be global.
playlist = list()

class Application(Frame):
	
	#Various callback functions for the homepage buttons
	def add_song(self):
		print "Add!"
	
	def remove_song(self):
		print "Remove!"
		
	def clear_songs(self):
		print "Clear!"
		
	def import_text(self):
		print "Import text!"
		
	def export_text(self):
		print "Export text!"
		
	def export_gmusic(self):
		print "Export playlist!"
		
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
		
		
	#callback function for the submit_button
	def getPlaylist(self):
		self.month, self.day, self.year = int(self.month_entry.get()), int(self.day_entry.get()), int(self.year_entry.get())
		self.startTime = self.startTime_entry.get()
		self.endTime = self.endTime_entry.get()
		
		playlist = getList(self.month, self.day, self.year, self.startTime, self.endTime)
		self.updatePlaylist()
		self.t.destroy();
	
	#Was supposed to update the playlist in the viewer to match the playlist variable
	#but alas, it is borked
	def updatePlaylist(self):
		for song in playlist:
			self.playlist_viewer = self.playlist_viewer.insert(END, song)
			self.playlist_viewer.update_idletasks()
	
		
		
	def createWidgets(self):
		#self.playlist = list()
	
		#label for playlist viewer
		self.playlist_label = Label(text="Active Playlist")
		self.playlist_label.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

		#The playlist viewer
		self.playlist_viewer = Listbox(self, selectmode=MULTIPLE, height=10, width=5)
		self.playlist_viewer.grid(row=1, rowspan=5, columnspan=4, padx=5, sticky="nesw")
		self.updatePlaylist()
	
		#The eventual add button
		self.add_button = Button(self, text="Add Song")
		self.add_button["command"] = self.add_song

		self.add_button.grid(row=0, column=4, padx=5)
		
		#The remove button
		self.remove_button = Button(self, text="Remove Song")
		self.remove_button["command"] = self.remove_song

		self.remove_button.grid(row=1, column=4, padx=5)
		
		#The clear button
		self.clear_button = Button(self, text="Clear Songs")
		self.clear_button["command"] = self.clear_songs

		self.clear_button.grid(row=2, column=4, padx=5)
		
		#The import text button
		self.import_text_button = Button(self, text="Import as Textfile")
		self.import_text_button["command"] = self.clear_songs

		self.import_text_button.grid(row=6, column=0, pady=5)
		
		#The export text button
		self.export_text_button = Button(self, text="Export as Textfile")
		self.export_text_button["command"] = self.clear_songs

		self.export_text_button.grid(row=6, column=1, pady=5)
		
		#The gmusic button
		self.gMusic_button = Button(self, text="Export to Google Music")
		self.gMusic_button["command"] = self.export_gmusic

		self.gMusic_button.grid(row=6, column=2, padx=5)
		
		#The webscrape button
		self.webscrape_button = Button(self, text="Import from Website")
		self.webscrape_button["command"] = self.scrape

		self.webscrape_button.grid(row=5, column=4, padx=5, pady=5)

	
	def on_exit(self):
		self.quit()
	
	def __init__(self, master=None):
		f = Frame.__init__(self, master, height=600, width=800)
		self.grid(row=0, column=0)
		master.protocol("WM_DELETE_WINDOW", self.on_exit)
		self.createWidgets()
		self.updatePlaylist()
	
	

root = Tk()
root.title("DittyGetty")

app = Application(master=root)
app.mainloop()

#Destroys after the mainloop is finished
root.destroy()