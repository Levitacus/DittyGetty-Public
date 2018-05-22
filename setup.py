from setuptools import setup

setup(
    name="dittygetty",
    version="0.0.1",
    py_modules=["dittygetty", "config", "playlist", "songInfo", "helperFuncs", "gmusic", "dg_gui", "daily_playlist", "npr", "scraper"],
    install_requires=["Click", "gmusicapi", "beautifulsoup4", "lxml", "cryptography"],
    
    entry_points="""
        [console_scripts]
        dittygetty=dittygetty:entry_point
    """
)
