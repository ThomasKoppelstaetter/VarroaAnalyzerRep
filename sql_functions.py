import mysql.connector
from datetime import datetime

# Verbindung zur Datenbank herstellen
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='varroa',
        password='meinPasswort',
        database='varroaanalyzer'
    )

# Neue Wabe erstellen (Datum automatisch)
def create_wabe():
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now()
    cursor.execute("INSERT INTO Wabe (Datum) VALUES (%s)", (now,))
    conn.commit()
    wID = cursor.lastrowid
    cursor.close()
    conn.close()
    return wID

# Neue Zelle erstellen (PosX, PosY, Stadium optional)
def create_zelle(wID, posX=None, posY=None, stadium=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Zelle (wID, PosX, PosY, Stadium) VALUES (%s, %s, %s, %s)",
        (wID, posX, posY, stadium)
    )
    conn.commit()
    zID = cursor.lastrowid
    cursor.close()
    conn.close()
    return zID

# Neues Bild erstellen (Name, Pfad, Varroaanzahl optional)
def create_bild(zID, namen=None, pfad=None, varroaanzahl=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Bilder (zID, Namen, Pfad, Varroaanzahl) VALUES (%s, %s, %s, %s)",
        (zID, namen, pfad, varroaanzahl)
    )
    conn.commit()
    bID = cursor.lastrowid
    cursor.close()
    conn.close()
    return bID

# Zelle-Update: Stadium ändern
def update_zelle_stadium(zID, stadium):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Zelle SET Stadium = %s WHERE zID = %s",
        (stadium, zID)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Zelle {zID} Stadium auf '{stadium}' aktualisiert")

# Bild-Update: Varroaanzahl ändern
def update_bild_varroaanzahl(bID, varroaanzahl):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Bilder SET Varroaanzahl = %s WHERE bID = %s",
        (varroaanzahl, bID)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Bild {bID} Varroaanzahl auf {varroaanzahl} aktualisiert")


# Für die Tabbelen ausgabe
def get_waben():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT wID, Datum FROM Wabe ORDER BY Datum DESC")
    data = cursor.fetchall()
    conn.close()
    return data

# Für die Tabbelen ausgabe
def get_zellen_by_wabe(wID):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            z.PosX,
            z.PosY,
            z.Stadium,
            -- erstes Bild oben
            (SELECT b.Varroaanzahl
             FROM Bilder b
             WHERE b.zID = z.zID
             ORDER BY b.bID ASC
             LIMIT 1) AS Varroaanzahl,
            (SELECT b.Pfad
             FROM Bilder b
             WHERE b.zID = z.zID AND b.Namen LIKE '%oben%'
             ORDER BY b.bID ASC
             LIMIT 1) AS BildOben,
            (SELECT b.Pfad
             FROM Bilder b
             WHERE b.zID = z.zID AND b.Namen LIKE '%unten%'
             ORDER BY b.bID ASC
             LIMIT 1) AS BildUnten
        FROM Zelle z
        WHERE z.wID = %s
        ORDER BY z.PosY, z.PosX
    """, (wID,))

    data = cursor.fetchall()
    conn.close()
    return data