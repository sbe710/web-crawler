import sqlite3
import os


def main():
    conn = sqlite3.connect("SaTRdatabase.db")
    cursor = conn.cursor()
    cursor.execute("""create table if not exists images
                      (name, path, sourse)""")
    cursor.execute("""create table if not exists videos
                      (path)""")
    cursor.execute("""create table if not exists audio
                      (path, sourse)""")
    cursor.execute("""create table if not exists textContent
                      (text, sourse)""")
    conn.commit()
    conn.close()


def video_to_db(path, cursor):
    cursor.execute("""create table if not exists videos
                   (name, path)""")
    video = [(str(os.path.basename(path)), str(os.path.abspath(path)))]
    cursor.executemany("INSERT INTO videos VALUES (?,?)", video)


def image_to_db(path, vsourse, cursor):
    if not str(vsourse) == 'no_video':
        sourse = str(os.path.abspath(vsourse))
    else:
        sourse = vsourse
    cursor.execute("""create table if not exists images
                   (name, path, sourse)""")
    for files in os.listdir(path):
        image = [(str(files), str(os.path.abspath(path)), str(sourse))]
        cursor.executemany("INSERT INTO images VALUES (?,?,?)", image)


def audio_to_db(path, vsourse, cursor):
    if not str(vsourse) == 'no_video':
        sourse = str(os.path.abspath(vsourse))
    else:
        sourse = vsourse
    cursor.execute("""create table if not exists audios
                   (path, sourse)""")
    audio = [(str(os.path.abspath(path)), str(sourse))]
    cursor.executemany("INSERT INTO audios VALUES (?,?)", audio)


def text_to_db(text, sourse, cursor):
    cursor.execute("""create table if not exists textContent
                   (text, sourse)""")
    txt = [(str(text), str(os.path.abspath(sourse)))]
    cursor.executemany("INSERT INTO textContent VALUES (?,?)", txt)


if __name__ == '__main__':
    main()
