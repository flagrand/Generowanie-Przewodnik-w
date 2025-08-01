import os
import sys
import customtkinter as ctk
from tkinter import filedialog
from reportlab.pdfgen import canvas
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def resource_path(relative_path):
    """ Zwraca absolutną ścieżkę do zasobu (działa też po spakowaniu jako .exe) """
    try:
        base_path = sys._MEIPASS  # tymczasowy katalog przy uruchomieniu .exe
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

from dotenv import load_dotenv
load_dotenv(dotenv_path=resource_path(".env"))

def polacz_z_baza():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        return conn
    except Exception as e:
        print("Błąd połączenia z bazą:", e)
        return None

def generuj_i_zapisz_pdf():
    numer = pole_tekstowe.get().strip()
    if not numer:
        etykieta.configure(text="Pole jest puste!")
        return

    historia_wpisow.append(numer)
    aktualizuj_historie()
    etykieta.configure(text=f"Generuję przewodnik dla: {numer}")

    conn = polacz_z_baza()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT klient, opis, data FROM przewodniki WHERE numer_zlecenia = %s", (numer,))
            dane = cur.fetchone()
            cur.close()
            conn.close()
        except Exception as e:
            etykieta.configure(text="Błąd zapytania SQL.")
            print("SQL error:", e)
            return
    else:
        etykieta.configure(text="Brak połączenia z bazą.")
        return

    folder = filedialog.askdirectory(title="Wybierz folder do zapisania PDF")
    if not folder:
        return

    sciezka = os.path.join(folder, f"Przewodnik_{numer}.pdf")
    c = canvas.Canvas(sciezka)
    c.setFont("Helvetica", 14)
    c.drawString(100, 750, f"Przewodnik dla zlecenia: {numer}")
    
    if dane:
        klient, opis, data = dane
        c.drawString(100, 720, f"Klient: {klient}")
        c.drawString(100, 700, f"Opis: {opis}")
        c.drawString(100, 680, f"Data: {data}")
    else:
        c.drawString(100, 720, "Brak danych w bazie.")

    c.save()
    etykieta.configure(text=f"Zapisano PDF: {sciezka}")

# --- GUI CustomTkinter ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

okno = ctk.CTk()
okno.title("Generowanie przewodników")
okno.geometry("900x600")
okno.iconbitmap(resource_path("img/wiss_small_icon.ico"))

historia_wpisow = []

# --- Główna ramka ---
ramka_glowna = ctk.CTkFrame(okno)
ramka_glowna.pack(fill="both", expand=True, padx=20, pady=20)

# --- Lewa kolumna: pole + przycisk + status ---
ramka_lewa = ctk.CTkFrame(ramka_glowna)
ramka_lewa.pack(side="left", fill="both", expand=True, padx=(0, 10))

# Rząd: pole + przycisk
ramka_wyszukiwania = ctk.CTkFrame(ramka_lewa, fg_color="transparent")
ramka_wyszukiwania.place(relx=0.5, rely=0.33, anchor="center")  # 1/3 od góry, wyśrodkowane poziomo

pole_tekstowe = ctk.CTkEntry(ramka_wyszukiwania, placeholder_text="Wpisz numer zlecenia", width=300)
pole_tekstowe.pack(side="left", padx=(0, 10))

przycisk = ctk.CTkButton(ramka_wyszukiwania, text="Generuj i zapisz PDF", command=generuj_i_zapisz_pdf)
przycisk.pack(side="left")

etykieta = ctk.CTkLabel(ramka_lewa, text="", anchor="center", justify="center", wraplength=600)
etykieta.place(relx=0.5, rely=0.5, anchor="n")  # wyśrodkowana i z większym odstępem od wyszukiwania

# --- Prawa kolumna: historia ---
ramka_prawa = ctk.CTkFrame(ramka_glowna)
ramka_prawa.pack(side="right", fill="y")

historia_label = ctk.CTkLabel(ramka_prawa, text="Historia", anchor="w")
historia_label.pack(pady=(10, 0))

lista_historia = ctk.CTkTextbox(ramka_prawa, height=400, width=250)
lista_historia.pack(pady=10, padx=10)

def aktualizuj_historie():
    lista_historia.delete("0.0", "end")
    for wpis in reversed(historia_wpisow):
        lista_historia.insert("end", wpis + "\n")

# --- Copyright ---
copyright = ctk.CTkLabel(okno, text="© 2025 WISS", anchor="s", font=ctk.CTkFont(size=12))
copyright.pack(side="bottom", pady=10)

okno.mainloop()
