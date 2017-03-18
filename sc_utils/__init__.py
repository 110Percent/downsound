import requests
import platform
import string
import urllib
import eyed3
import unicodedata
client_id = 'bed20744714e9c5962c351efe15840ff'

def fetch_metadata(track_url):
    '''
    Fetches metadata for a track
    '''
    to_api = 'https://api.soundcloud.com/resolve?url=' + track_url
    get_data = requests.get(to_api, params={
        'client_id': client_id
    })
    return get_data.json()

def download_track(track_json):
    '''
    Downloads a track from its JSON data
    '''

    # Print track info
    print('\n')
    print(track_json['title'])
    print(track_json['user']['username'])
    if 'genre' in track_json:
        print('#' + track_json['genre'])
    print('\n')

    # Detect if track has a streamable URL
    if track_json['streamable']:
        dl_url = track_json['stream_url']
        print('Track is streamable! Starting download...')
    else:
        print('Track is not streamable.')
        return

    # Set regex for invalid filename characters based on OS type
    if platform.system() == 'Windows':
        inchar_regex = '<>:"/\|?*'
    else:
        inchar_regex = '/'
    
    # Set filename for downloaded track
    fname = track_json['title']
    for char in inchar_regex:
        fname = fname.replace(char,'')
    fname += '.mp3'

    # Download track
    with open(fname, 'wb') as handle:
        response = requests.get(dl_url, stream=True, params={
            'client_id': client_id
        })

        if not response.ok:
            print('ur shits fukt up fam')
            return

        for block in response.iter_content(1024):
            handle.write(block)
        
        print('Download finished; Writing ID3 tags...')

        # Apply ID3 tags
        audiofile = eyed3.load(fname)
        audiofile.initTag()
        audiofile.tag.artist = track_json['user']['username']
        audiofile.tag.title = track_json['title']
        if not track_json['artwork_url'] == None:
            art_url = track_json['artwork_url']
        else:
            art_url = track_json['user']['avatar_url']
        art = requests.get(art_url, stream=True).raw.read()
        audiofile.tag.images.set(3,art,"image/jpeg",u"you can put a description here")
        audiofile.tag.save()

        print('Tags applied!')