from setuptools import setup

setup(
    name="dittygetty",
    version="1.0.0",
    py_modules=["dittygetty", "config", "playlist", "songInfo", "helperFuncs", "gmusic", "dg_gui", "daily_playlist", "npr", "scraper"],
    install_requires=["Click", "gmusicapi", "bs4", "lxml"],
    
    entry_points="""
        [console_scripts]
        dittygetty=dittygetty:entry_point
    """
)
