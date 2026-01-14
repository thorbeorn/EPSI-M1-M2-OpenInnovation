import subprocess
import os
import pathlib

command = ["wg", "--help"]
current_python_folder = pathlib.Path(__file__).parent.resolve()

config_folder = current_python_folder / "config"
key_folder = current_python_folder / "keys"

if not os.path.exists(config_folder):
  os.makedirs(config_folder)

try:
  subprocess.check_call(command)
except subprocess.CalledProcessError:
  raise ValueError(f"Error executing command: {command}")


import tkinter as tk
from tkinter import messagebox

# Palette de couleurs
colors = {
    "rose_fonce": "#CE6A6B",
    "rose_clair": "#EBACA2",
    "vert_clair": "#BED3C3",
    "bleu_canard": "#4A919E",
    "bleu_fonce": "#212E53"
}

# Fonction de connexion
def login():
    username = entry_user.get()
    password = entry_pass.get()
    # Exemple simple : utilisateur = admin, mot de passe = 1234
    if username == "admin" and password == "1234":
        messagebox.showinfo("Connexion réussie", f"Bienvenue {username} !")
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Page de connexion")
root.geometry("400x300")
root.configure(bg=colors["bleu_fonce"])

# Titre
title = tk.Label(root, text="Connexion", font=("Arial", 24, "bold"), bg=colors["bleu_fonce"], fg=colors["rose_fonce"])
title.pack(pady=20)

# Frame pour les champs
frame = tk.Frame(root, bg=colors["bleu_fonce"])
frame.pack(pady=10)

# Nom d'utilisateur
label_user = tk.Label(frame, text="Nom d'utilisateur", font=("Arial", 12), bg=colors["bleu_fonce"], fg=colors["vert_clair"])
label_user.grid(row=0, column=0, sticky="w", pady=5)
entry_user = tk.Entry(frame, font=("Arial", 12), bg=colors["rose_clair"], fg=colors["bleu_fonce"], relief="flat")
entry_user.grid(row=1, column=0, pady=5, ipadx=50, ipady=5)

# Mot de passe
label_pass = tk.Label(frame, text="Mot de passe", font=("Arial", 12), bg=colors["bleu_fonce"], fg=colors["vert_clair"])
label_pass.grid(row=2, column=0, sticky="w", pady=5)
entry_pass = tk.Entry(frame, font=("Arial", 12), bg=colors["rose_clair"], fg=colors["bleu_fonce"], relief="flat", show="*")
entry_pass.grid(row=3, column=0, pady=5, ipadx=50, ipady=5)

# Bouton de connexion
btn_login = tk.Button(root, text="Se connecter", font=("Arial", 12, "bold"), bg=colors["bleu_canard"], fg=colors["rose_clair"], activebackground=colors["rose_fonce"], activeforeground=colors["bleu_fonce"], command=login)
btn_login.pack(pady=20, ipadx=10, ipady=5)

root.mainloop()
