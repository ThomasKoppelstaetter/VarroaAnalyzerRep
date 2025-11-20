import mysql.connector
from datetime import datetime

# Verbindung zur Datenbank herstellen
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
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