from __future__ import annotations

import sqlite3
from contextlib import contextmanager

DB_FILE = 'songs_database.db'

__all__ = ['DB_FILE', 'get_db_connection', 'init_db']


@contextmanager
def get_db_connection():
  conn = sqlite3.connect(DB_FILE)
  conn.row_factory = sqlite3.Row
  try:
    yield conn
  finally:
    conn.close()


def init_db():
  with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.executescript(CREATE_TABLE_SQL)
    conn.commit()


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS artists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    gender TEXT
);

CREATE TABLE IF NOT EXISTS lyrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lyrics TEXT,
    language TEXT
);

CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    artist_id INTEGER,
    lyrics_id INTEGER,
    FOREIGN KEY (artist_id) REFERENCES artists (id),
    FOREIGN KEY (lyrics_id) REFERENCES lyrics (id)
);

CREATE TABLE IF NOT EXISTS albums (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    genre TEXT,
    year TEXT,
    mood TEXT
);

CREATE TABLE IF NOT EXISTS album_songs (
    album_id INTEGER,
    song_id INTEGER,
    FOREIGN KEY (album_id) REFERENCES albums (id),
    FOREIGN KEY (song_id) REFERENCES songs (id),
    PRIMARY KEY (album_id, song_id)
);

CREATE TABLE IF NOT EXISTS descriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    song_id INTEGER,
    artist_id INTEGER,
    album_id INTEGER,
    region TEXT,
    FOREIGN KEY (song_id) REFERENCES songs (id),
    FOREIGN KEY (artist_id) REFERENCES artists (id),
    FOREIGN KEY (album_id) REFERENCES albums (id)
);

CREATE TABLE IF NOT EXISTS featured_artists (
    album_id INTEGER,
    artist_id INTEGER,
    FOREIGN KEY (album_id) REFERENCES albums (id),
    FOREIGN KEY (artist_id) REFERENCES artists (id),
    PRIMARY KEY (album_id, artist_id)
);

CREATE TABLE IF NOT EXISTS audio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    audio_file TEXT NOT NULL,
    song_id INTEGER,
    FOREIGN KEY (song_id) REFERENCES songs (id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_artists_name ON artists(name);
CREATE INDEX IF NOT EXISTS idx_songs_name ON songs(name);
CREATE INDEX IF NOT EXISTS idx_songs_artist_id ON songs(artist_id);
CREATE INDEX IF NOT EXISTS idx_albums_name ON albums(name);
CREATE INDEX IF NOT EXISTS idx_albums_genre ON albums(genre);
CREATE INDEX IF NOT EXISTS idx_album_songs_song_id ON album_songs(song_id);
CREATE INDEX IF NOT EXISTS idx_descriptions_song_id ON descriptions(song_id);
CREATE INDEX IF NOT EXISTS idx_featured_artists_album_id ON featured_artists(album_id);
CREATE INDEX IF NOT EXISTS idx_audio_song_id ON audio(song_id);
"""
