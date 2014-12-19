# project file for py2app

from setuptools import setup

setup(
  name="OpenMEE",
  author="George Dietz",
  author_email="george_dietz@brown.edu",
  app=["mac_prelaunch.py"],
  options={"py2app":
    {"argv_emulation": True,
     "resources": ["/opt/local/Library/Frameworks/R.framework/Versions/3.1/Resources",],
     "iconfile": "images/mac_icon.icns",
     "no_strip": True,
     "includes":"rpy2",
     }
  },
  setup_requires=["py2app"])
