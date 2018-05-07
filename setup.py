from setuptools import setup

setup(
    name="dittygetty",
    version="0.0.1",
    py_modules=["dittygetty"],
    install_requires=["Click"],
    
    entry_points="""
        [console_scripts]
        dittygetty=dittygetty:entry_point
    """
)
