# DittyGetty

DittyGetty is a tool used to scrape playlists from JPR, modify those playlists, and export those playlists to Google Music.
DittyGetty utilizes a GUI made from Tkinter to display the playlist and allow the user to make modifications.
DittyGetty can be run from the command prompt and uses Click to make the CLI.

# Getting Started

## Prerequisites

If you plan on executing DittyGetty from the command prompt you must have Python 2.7 installed https://www.python.org/download/releases/2.7/ 

The following libraries are required to run the program:

BeautifulSoup https://www.crummy.com/software/BeautifulSoup/bs4/doc/#  
gmusicapi https://unofficial-google-music-api.readthedocs.io/en/latest/  
Click http://click.pocoo.org/5/

Download libraries with pip: 
To check if you have pip installed:
```
$ pip --version
```
If you don't have pip installed, install it from https://bootstrap.pypa.io/get-pip.py
then navigate to your downloads directory and run get-pip.py with admin priveleges.
Mac OS and Linux:
```
$ sudo python get-pip.py
```
Windows:
```
$ python get-pip.py
```

If you have pip all ready to go:
```
$ pip install beautifulsoup4  
$ pip install gmusicapi
$ pip install click
```

## Command Line Interface

To install the CLI, you need to install setup.py like so:

```
python setup.py install
```

### Commands

exports
```
Usage: dittygetty exports [OPTIONS] PLAYLIST_NAME

  Exports the active playlist to google music with the name [PLAYLIST_NAME]

Options:
  --f TEXT  File: Export a file to Gmusic rather than the active playlist
  --e       Add Existing: Add songs to an existing playlist.
  --m       Merge: If adding to an existing playlist, duplicate songs will
            not be added
  --help    Show this message and exit.
```

gui
```
Usage: dittygetty gui [OPTIONS]

  Opens the graphical user interface to allow for playlst manipulation
  there. **Warning: Will halt this window.

Options:
  --help  Show this message and exit.
```
imports
```
Usage: dittygetty imports [OPTIONS] COMMAND [ARGS]...

  Commands for importing a playlist

Options:
  --help  Show this message and exit.

Commands:
  daily_playlist  Imports a playlist from dailyplaylist.com...
  gmusic          Imports a playlist from gmusic, requires a...
  jpr             Imports a playlist from JPR Requires a date...
```

imports commands

    jpr
```
Usage: dittygetty imports jpr [OPTIONS] DATE

      Imports a playlist from JPR Requires a date in the format MM-DD-YYYY,
      'today' or 'yesterday' keywords

Options:
  --t TEXT   Starting time for parse
  --et TEXT  Ending time for parse
  --f TEXT   File: Option to save imported songs to a file rather than the
             active playlist. Can use today and yesterday keywords.
  --help     Show this message and exit.
```
    gmusic
```
Usage: dittygetty imports gmusic [OPTIONS] PLAYLIST_NAME

  Imports a playlist from gmusic, requires a playlist name

Options:
  --f TEXT  File: Option to save imported songs to a file rather than the
            active playlist. Can use today and yesterday keywords.
  --help    Show this message and exit.
```
    daily_playlist
```
Usage: dittygetty imports daily_playlist [OPTIONS] NAME

  Imports a playlist from dailyplaylist.com name argument is the url name
  given to a playlist i.e. dailyplaylist.com/chill-daily/ chill-daily is
  the playlist name

Options:
  --f TEXT  File: Option to save imported songs to a file rather than the
            active playlist. Can use today and yesterday keywords.
  --help    Show this message and exit.
```
  
read
```
Usage: dittygetty read [OPTIONS] FILE

  Reads a playlist from textfile Each line in the file must be in the
  format          time||song||artist

Options:
  --help  Show this message and exit.
```

write
```
Usage: dittygetty write [OPTIONS] FILE

  Writes the active playlist to the file with the designated name     Will
  overwrite any previous data in that file

Options:
  --m     Merge: If file already exists, append active playlist with
          duplicate removal
  --help  Show this message and exit.
```
playlist
```
Usage: dittygetty playlist [OPTIONS] COMMAND [ARGS]...

  Commands for modifying the playlist

Options:
  --help  Show this message and exit.
```

Playlist Commands:
  
    add ---        Adds a song to the current playlist
```
      Usage: dittygetty playlist add [OPTIONS] SONG ARTIST

        Adds a song to the current playlist

      Options:
        --help  Show this message and exit.
```
    clear ---      Clears playlist, default is active playlist
```
      Usage: dittygetty playlist clear [OPTIONS]

        Clears playlist, default is active playlist

      Options:
        --help  Show this message and exit.
```
    display ---    Displays playlist, default is active playlist
```
      Usage: dittygetty playlist display [OPTIONS]

        Displays playlist, default is active playlist

      Options:
        --ff      Displays the playlist in the file
                  format(HH:MM||SongName||ArtistName). Can be output into a file
                  for import later.
        --f TEXT  Displays the playlist from a file without loading it into the
                  active playlist
        --help    Show this message and exit.
```
    get_dir ---    Gets current app directory
```
      Usage: dittygetty playlist get_dir [OPTIONS]

        Gets current app directory

      Options:
        --help  Show this message and exit.
```

### Scheduling with cron

Dittygetty can easily be scheduled to run with crontab on Unix-like computer operating systems.

Here's an example of a cronjob that runs at 2:00 AM every day and imports 4-14-2018 from JPR into the text file "test.txt"
```
crontab 0 2 * * * dittygetty imports jpr --f "test.txt" 4-14-2018
```

Using today keyword, runs at 11:59 PM every day and imports that day to a file named that date EX: 2018-05-22.txt 
```
crontab 59 23 * * * dittygetty imports jpr --f today today
```

## Logging in with Google Music

Because of the unofficial api gmusicapi, you cannot login to Google Music using the actual password to your Google music account.
To login to Google Music through DittyGetty, you must set up an app password.

To do this first go to My Account from whatever Google email you use to access Google Music from.

![Add Account button](https://i.imgur.com/a0Huqhz.png)


From there: go to sign in and security

![Sign in and Security](https://i.imgur.com/icmMhL0.png)


Then turn on 2 step verification if it's not already on and add your phone.

![2 Step Verification](https://i.imgur.com/8ZGQ4kn.png)


Once 2 Step Verification is on, Click App Password just below it.

![App Password](https://i.imgur.com/oz8MuAu.png)


Click Select App then Other and make a custom app called DittyGetty:

![Custom App](https://i.imgur.com/lLzCXCj.png)


Click Generate and from there you'll be given a 16 character password you can use to log in through DittyGetty.

![App Password](https://i.imgur.com/oGM38qe.png)

Write this password down as you'll need it whenever you need to login.
After you have this App Password, you may disable 2-step verification and the password will remain usable.

