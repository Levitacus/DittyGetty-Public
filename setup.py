from setuptools import setup

setup(
    name="dittygetty",
    version="0.0.1",
    py_modules=["dittygetty", "config", "playlist", "songInfo", "helperFuncs", "jpr", "gmusic", "dg_gui"],
    install_requires=["Click", "gmusicapi", "beautifulsoup4", "lxml"],
    
    entry_points="""
        [console_scripts]
        dittygetty=dittygetty:entry_point
    """
)
