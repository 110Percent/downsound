import eyed3
from sc_utils import *

print('Please paste/enter the track URL:')
track_url = raw_input()
track = fetch_metadata(track_url))
download_track(track)