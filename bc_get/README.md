### bc_get

Downloads Bandcamp tracks as .mp3. 

To set the preferred output path for the files, edit the OUTPUT_PATH field in settings.json (./output by default.)

(Settings file gets created first time the script runs.)

**Requirements:**
- requests
- bs4
- mutagen

**Usage:**
```
    python bc_get.py URL | -n
```
The -n optional parameter is passed to notify when the download is finished.

**Example:**

```
    python bc_get.py MyUser.bandcamp.com
```
Downloads all non-existing albums and orphan tracks (singles) into the OUTPUT_PATH specified in settings.json. 
(It is what you want use to keep fully updated on the content as well, as it doesn't download files that already exist in
the output directory.)

**Behaviour by URL type:** 
```
    MyUser.bandcamp.com => Downloads all albums, then all orphan tracks into a Track folder
    MyUser.bandcamp.com/music => Downloads all albums, then all orphan tracks into a Track folder
    MyUser.bandcamp.com/album/MyAlbum => Downloads album MyAlbum
    MyUser.bandcamp.com/track/MyTrack => Downloads track MyTrack into Track folder. If MyTrack belongs to an album, it asks the user if he would rather download the full album. 
```
