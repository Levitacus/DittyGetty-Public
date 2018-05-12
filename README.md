# DittyGetty

DittyGetty is a tool to scrape playlists from JPR, modify those playlists, and export those playlists to Google Music.
DittyGetty utilizes a GUI made from Tkinter from view the playlist and allow the user to make modifications.

## Getting Started

You can either install the windows or mac releases and run DittyGetty from the main file located in DittyGetty/dist or you can download all files and run from the command prompt.

### Prerequisites

If you plan on executing DittyGetty from the command prompt you must have Python 2.7 installed https://www.python.org/download/releases/2.7/ 

The following libraries are required to run the program:

BeautifulSoup https://www.crummy.com/software/BeautifulSoup/bs4/doc/#  
gmusicapi https://unofficial-google-music-api.readthedocs.io/en/latest/
cryptography https://cryptography.io/en/latest/ for storing the password temporarily.

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
$ pip install cryptography

```

### Running

To run the gui from the command prompt, type the following command while in the DittyGetty directory:

```
python main.py
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

