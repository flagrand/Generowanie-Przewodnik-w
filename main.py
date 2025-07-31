import tkinter as tk
import customtkinter as ctk

historia_wpisow = []

def generuj():
    wpisany_tekst = pole_tekstowe.get()
    if wpisany_tekst.strip():
        historia_wpisow.append(wpisany_tekst)
        aktualizuj_historie()
        etykieta.configure(text=f"Wygenerowano dla: {wpisany_tekst}")
    else:
        etykieta.configure(text="Pole jest puste!")

def aktualizuj_historie():
    pole_historia.configure(state="normal")  # odblokuj edycję
    pole_historia.delete("1.0", "end")       # wyczyść zawartość
    for wpis in reversed(historia_wpisow):   # najnowsze na górze
        pole_historia.insert("end", f"• {wpis}\n")
    pole_historia.configure(state="disabled")  # zablokuj edycję

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

okno = ctk.CTk()
okno.title("Generowanie przewodników")
okno.geometry("800x600")
okno.iconbitmap("img/wiss_small_icon.ico")

# ----- Zakładki -----
zakladki = ctk.CTkTabview(okno, width=760, height=500)
zakladki.pack(pady=20)
zakladki.add("Generuj")
zakladki.add("Historia")

# ----- Zakładka "Generuj" -----
etykieta = ctk.CTkLabel(zakladki.tab("Generuj"), text="Podaj numer zlecenia lub dane wejściowe:")
etykieta.pack(pady=10)

pole_tekstowe = ctk.CTkEntry(zakladki.tab("Generuj"), width=300, placeholder_text="Wpisz tutaj...")
pole_tekstowe.pack(pady=10)

przycisk_generuj = ctk.CTkButton(zakladki.tab("Generuj"), text="Generuj", command=generuj)
przycisk_generuj.pack(pady=10)

# ----- Zakładka "Historia" jako lista -----
pole_historia = ctk.CTkTextbox(zakladki.tab("Historia"), width=700, height=400)
pole_historia.pack(pady=10)
pole_historia.insert("1.0", "(Brak wpisów)")
pole_historia.configure(state="disabled")  # zablokuj ręczną edycję

# ----- Stopka -----
stopka = ctk.CTkLabel(okno, text="© WISS All rights reserved", font=ctk.CTkFont(size=12))
stopka.pack(side="bottom", pady=5)

okno.mainloop()
