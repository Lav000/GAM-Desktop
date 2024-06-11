import subprocess
import threading
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext
import re
import configparser
import shutil

# Chargement des configurations
config = configparser.ConfigParser()
config.read('config.ini')
gam_path = shutil.which('gam')


if not gam_path:
    raise FileNotFoundError("GAM n'a pas été trouvé dans le PATH.")

# Fonction pour exécuter la commande gam et afficher les sorties dans une fenêtre de terminal
def run_gam_command(email_delegated, user):
    try:
        command = [gam_path, "user", user, "delegate", "to", email_delegated]
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True)

        # Efface le contenu précédent du terminal
        terminal_output.delete('1.0', tk.END)

        # Exécute la commande et récupère les sorties
        stdout, stderr = process.communicate(input='\n'.join(["\r"]))

        # Affiche les sorties de la commande dans le terminal
        terminal_output.insert(tk.END, stdout)
        terminal_output.insert(tk.END, stderr)
    except FileNotFoundError:
        messagebox.showerror("Error", "Zut ! Where is GAM ?")
    except Exception as e:
        messagebox.showerror("Error", f"Pas réussi ta commande: {e}")


# Fonction pour valider les emails
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


# Fonction pour déléguer l'email dans un thread séparé
def delegate_email():
    email_delegated = entry_email.get()
    user = entry_user.get()
    if not email_delegated or not user:
        messagebox.showwarning("Input Error", "Et le mail ??!!")
        return

    if not is_valid_email(email_delegated) or not is_valid_email(user):
        messagebox.showwarning("Input Error", "Format d'email invalide")
        return

    threading.Thread(target=run_gam_command, args=(email_delegated, user)).start()
    threading.Thread(target=tappingLetter, args=("Bien vu le broooother", label_message, 0.2)).start()


# Fonction pour afficher un message lettre par lettre
def tappingLetter(chaine, label, delai=0.1):
    label.config(text="")
    for lettre in chaine:
        label.config(text=label.cget("text") + lettre)
        label.update()
        time.sleep(delai)


# Création de la fenêtre principale
root = tk.Tk()
root.title("Email Delegation")

# Création des widgets
frame = tk.Frame(root)
frame.pack(pady=10, padx=10)

label_email = tk.Label(frame, text="Email à déléguer :")
label_email.grid(row=0, column=0, padx=5, pady=5)
entry_email = tk.Entry(frame)
entry_email.grid(row=0, column=1, padx=5, pady=5)

label_user = tk.Label(frame, text="User bénéficiaire :")
label_user.grid(row=1, column=0, padx=5, pady=5)
entry_user = tk.Entry(frame)
entry_user.grid(row=1, column=1, padx=5, pady=5)

button_delegate = tk.Button(frame, text="Déléguer", command=delegate_email)
button_delegate.grid(row=2, columnspan=2, pady=10)

label_message = tk.Label(root, text="")
label_message.pack(pady=5)

# Création de la fenêtre du terminal
terminal_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
terminal_output.pack(pady=10, padx=10)

# Lancement de la boucle principale
root.mainloop()
