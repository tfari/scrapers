from mutagen.mp3 import MP3
from mutagen.id3 import TPE2, TIT2, TCON, TRCK, TPE1, TALB, TYER, APIC


# v0.0.1


def mp3_tag_file(filename, track_artist, track_title, *, track_genre=None, track_count=None, album_artist=None,
                 album_title=None, album_release=None, album_cover=None, artist_cover=None, track_cover=None):
    """
    Tags an mp3 file
    """
    mp3 = MP3(filename)
    if mp3.tags is None:
        mp3.add_tags()

    # Essential Tags:
    mp3.tags.add(TPE1(encoding=3, text=track_artist))
    mp3.tags.add(TIT2(encoding=3, text=track_title))

    # Non-essential Tags:
    if track_genre:
        mp3.tags.add(TCON(encoding=3, text=track_genre))
    if track_count:
        mp3.tags.add(TRCK(encoding=3, text=str(track_count)))
    if album_artist:
        mp3.tags.add(TPE2(encoding=3, text=album_artist))
    if album_title:
        mp3.tags.add(TALB(encoding=3, text=album_title))
    if album_release:
        mp3.tags.add(TYER(encoding=3, text=str(album_release)))

    # Artwork tags:
    if album_cover:
        mp3.tags.add(APIC(encoding=3, mime='image/jpeg', type=12, desc='Cover', data=album_cover))
    if artist_cover:
        mp3.tags.add(APIC(encoding=3, mime='image/jpeg', type=13, desc='Cover', data=artist_cover))
    if track_cover:
        mp3.tags.add(APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=track_cover))

    mp3.save(v2_version=3)
