### sc_track_get

Downloads Soundcloud tracks as .mp3. 

geckodriver.exe must be in PATH if we need to generate a client_id via Selenium.

To set the prefered output path for the files, edit the OUTPUT_PATH field in settings.json (./output by default.)

**Requirements:**
- requests
- mutagen

**Usage:**
```
    python sc_get.py URL | -v
```
The -v optional parameter is passed to activate verbose printing

**Example:**

```
    python sc_get.py soundcloud.com/MyUser
```
Downloads all non-existing playlists and orphan tracks (singles) into the OUTPUT_PATH specified in settings.json. 
<br>
It is what you want use to keep fully updated on the content as well. 

**Behaviour by URL type:** 
```
    https://soundcloud.com/MyUser => Downloads all playlists, then all orphan tracks into a Track folder
    https://soundcloud.com/MyUser/tracks => Downloads all tracks into a Track folder
    https://soundcloud.com/MyUser/sets => Downloads all sets
    https://soundcloud.com/MyUser/MyTrack => Downloads track MyTrack
    https://soundcloud.com/MyUser/sets/MySet => Downloads set MySet
```

**Warning:**
```
    http://soundcloud.com/MyUser/tracks
```
Should only be used to update orphan tracks(singles) after all sets have already been downloaded, unless
you want to download all tracks, indistinctly of if they belong to a playlist, into a same folder and tagged
as belonging to a single album.