
from collections import namedtuple

VersionInfo = namedtuple("VersionInfo", "major minor build")

version_info = VersionInfo(
   major=2,
   minor=0,
   build=56,
)

__version__ = f"{version_info.major}.{version_info.minor:02d}.{version_info.build:04d}"