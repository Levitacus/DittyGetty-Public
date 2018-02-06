from Tkinter import *

class Application(Frame):
	
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
		print "Webscrape!"
		
	def createWidgets(self):
	
		#label for playlist viewer
		self.playlist_label = Label(text="Active Playlist")
		self.playlist_label.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

		#The playlist viewer
		self.playlist_viewer = Listbox(self)
		self.playlist_viewer.grid(row=1, rowspan=5, columnspan=4, padx=5, sticky="nesw")
		
	
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
		self.gMusic_button["command"] = self.clear_songs

		self.gMusic_button.grid(row=6, column=2, padx=5)
		
		#The webscrape button
		self.webscrape_button = Button(self, text="Import from Website")
		self.webscrape_button["command"] = self.clear_songs

		self.webscrape_button.grid(row=5, column=4, padx=5, pady=5)

	
	def on_exit(self):
		self.quit()
	
	def __init__(self, master=None):
		f = Frame.__init__(self, master, height=600, width=800)
		self.grid(row=0, column=0)
		master.protocol("WM_DELETE_WINDOW", self.on_exit)
		self.createWidgets()
		

# class Container(Frame):

	# #Dunno what I'm doing here.
	# def make_label(self, caption):
		# self.label = Label(caption)
		# self.label.grid(row=3, column=0)
		
	# def __init__(self, master=None):
		# Frame.__init__(self, master)
		# x = StringVar()
		# self.entry = Entry(textvariable=x)
		# self.label_test = Label(textvariable=x);
		# self.make_label(self.entry.get())
		# self.label_test.grid(row=1, column=0)
		# self.entry.grid(row=2, column=0)
	
	

root = Tk()
root.title("DittyGetty")

app = Application(master=root)
app.mainloop()

#Destroys after the mainloop is finished
root.destroy()