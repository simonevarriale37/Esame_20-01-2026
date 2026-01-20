from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
                   FROM artist a"""
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def prendi_artisti_con_album_maggiore(numero_album):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT a.id, a.name, COUNT(*) AS num_album
                   FROM artist a, album b
                   WHERE a.id = b.artist_id 
                   GROUP BY a.id, a.name
                   HAVING COUNT(*) >= %s"""
        cursor.execute(query, (numero_album,))
        lista_artisti_per_album = []
        for row in cursor:
            lista_artisti_per_album.append((row['id'], row['name']))
        cursor.close()
        conn.close()
        return lista_artisti_per_album

    @staticmethod
    def prendi_artisti_con_canzone_stesso_genere():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT a1.id AS artist1, a2.id AS artist2, COUNT(*) AS num_generi
                    FROM artist a1, artist a2, track t1, track t2, album ab1, album ab2
                    WHERE a1.id = ab1.artist_id AND a2.id = ab2.artist_id 
                        AND t1.album_id = ab1.id AND t2.album_id = ab2.id AND a1.id <> a2.id
                        AND t1.id <> t2.id AND t1.genre_id = t2.genre_id
                    GROUP BY a1.id, a2.id"""
        cursor.execute(query)
        lista_artisti_per_genere = []
        for row in cursor:
            lista_artisti_per_genere.append((row['artist1'], row['artist2'], row['num_generi']))
        cursor.close()
        conn.close()
        return lista_artisti_per_genere

    @staticmethod
    def prendi_artisti_con_canzone_in_minuti(durata_minima):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT a1.id AS artist, COUNT(*) AS tot_canzoni
                    FROM artist a1, track t1, album ab1
                    WHERE a1.id = ab1.artist_id  AND t1.album_id = ab1.id
                          AND (t1.milliseconds/60000) >= %s
                    GROUP BY a1.id"""
        cursor.execute(query,(durata_minima,))
        lista_artisti_per_minuti = []
        for row in cursor:
            lista_artisti_per_minuti.append((row['artist'], row['tot_canzoni']))
        cursor.close()
        conn.close()
        return lista_artisti_per_minuti


