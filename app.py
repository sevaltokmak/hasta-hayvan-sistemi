from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "database.db"


# 🗄 VERİTABANI
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kayitlar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isim TEXT,
        telefon TEXT,
        email TEXT,
        kategori TEXT,
        tur TEXT,
        durum TEXT,
        aciklama TEXT,
        konum TEXT,
        foto TEXT,
        vaka_durum TEXT DEFAULT 'Alındı',
        tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

init_db()


# 🏠 ANA SAYFA
@app.route("/")
def index():
    return render_template("kullanici.html")


# 🔀 SEÇİM
@app.route("/secim", methods=["POST"])
def secim():
    isim = request.form["isim"]
    telefon = request.form["telefon"]
    email = request.form["email"]
    secim = request.form["secim"]

    if secim == "Hayvan":
        return render_template("hayvan.html", isim=isim, telefon=telefon, email=email)
    else:
        return render_template("sikayet.html", isim=isim, telefon=telefon, email=email)


# 📥 KAYIT
@app.route("/gonder", methods=["POST"])
def gonder():
    isim = request.form.get("isim")
    telefon = request.form.get("telefon")
    email = request.form.get("email")

    kategori = request.form.get("kategori", "")
    tur = request.form.get("tur", "")
    durum = request.form.get("durum", "")
    aciklama = request.form.get("aciklama", "")
    konum = request.form.get("konum", "")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO kayitlar 
    (isim, telefon, email, kategori, tur, durum, aciklama, konum)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (isim, telefon, email, kategori, tur, durum, aciklama, konum))

    conn.commit()
    conn.close()

    return render_template("basarili.html")


# 🧑‍🚒 PANEL
@app.route("/panel")
def panel():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM kayitlar ORDER BY id DESC")
    veriler = cursor.fetchall()

    conn.close()

    return render_template("panel.html", veriler=veriler)


# 🔄 DURUM GÜNCELLE
@app.route("/guncelle/<int:id>", methods=["POST"])
def guncelle(id):
    durum = request.form["durum"]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE kayitlar 
    SET vaka_durum=? 
    WHERE id=?
    """, (durum, id))

    conn.commit()
    conn.close()

    return "OK"


# 📱 SORGU (SON KAYIT)
@app.route("/sorgu", methods=["GET", "POST"])
def sorgu():
    if request.method == "POST":
        telefon = request.form["telefon"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM kayitlar 
        WHERE telefon=? 
        ORDER BY id DESC 
        LIMIT 1
        """, (telefon,))

        veriler = cursor.fetchall()

        conn.close()

        return render_template("sorgu.html", veriler=veriler)

    return render_template("sorgu.html")


# 🚀 RENDER UYUMLU BAŞLATMA
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)