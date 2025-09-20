import os
import shutil
import json
import threading
import zipfile
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

CONFIG_FILE = "backup_config.json"

class BackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Copias de Juegos")
        self.root.geometry("800x500")

        self.games = self.load_config()
        self.selected_game = None

        self.create_widgets()
        self.refresh_game_list()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_config(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.games, f, indent=4)

    def create_widgets(self):
        # Panel Izquierdo: lista de juegos
        frame_left = tk.Frame(self.root, padx=10, pady=10)
        frame_left.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(frame_left, text="Juegos").pack()
        self.game_list = tk.Listbox(frame_left, width=25, height=20)
        self.game_list.pack(fill=tk.Y)
        self.game_list.bind("<<ListboxSelect>>", self.on_game_select)

        tk.Button(frame_left, text="Añadir juego", command=self.add_game).pack(pady=5)
        tk.Button(frame_left, text="Eliminar juego", command=self.delete_game).pack(pady=5)
        tk.Button(frame_left, text="Salir", command=self.root.quit).pack(pady=20)

        # Panel Derecho: detalles del juego
        frame_right = tk.Frame(self.root, padx=10, pady=10)
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.label_game = tk.Label(frame_right, text="Selecciona un juego", font=("Arial", 14))
        self.label_game.pack()

        btn_frame = tk.Frame(frame_right)
        btn_frame.pack(pady=5)
        self.btn_open_game = tk.Button(btn_frame, text="Abrir carpeta del juego",
                                       command=self.open_game_folder, state=tk.DISABLED)
        self.btn_open_game.pack(side=tk.LEFT, padx=5)

        self.btn_open_backup = tk.Button(btn_frame, text="Abrir carpeta de copias",
                                         command=self.open_backup_folder, state=tk.DISABLED)
        self.btn_open_backup.pack(side=tk.LEFT, padx=5)

        self.btn_create_copy = tk.Button(btn_frame, text="Crear copia",
                                         command=self.create_backup, state=tk.DISABLED)
        self.btn_create_copy.pack(side=tk.LEFT, padx=5)

        # Lista de copias
        tk.Label(frame_right, text="Copias de seguridad").pack()
        self.backup_list = tk.Listbox(frame_right, width=50, height=15)
        self.backup_list.pack(fill=tk.BOTH, expand=True)

        # Botones de acciones sobre las copias
        action_frame = tk.Frame(frame_right)
        action_frame.pack(pady=5)
        tk.Button(action_frame, text="Restaurar copia", command=self.restore_backup).pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Eliminar copia", command=self.delete_backup).pack(side=tk.LEFT, padx=5)

        # Barra de progreso
        self.progress = ttk.Progressbar(frame_right, mode="determinate")
        self.progress.pack(fill=tk.X, pady=5)

    def center_window(self, win):
        win.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (win.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (win.winfo_height() // 2)
        win.geometry(f"+{x}+{y}")

    def refresh_game_list(self):
        self.game_list.delete(0, tk.END)
        for game in self.games:
            self.game_list.insert(tk.END, game)

    def refresh_backup_list(self):
        self.backup_list.delete(0, tk.END)
        if self.selected_game:
            game_data = self.games[self.selected_game]
            backup_dir = game_data["backup_dir"]
            if os.path.exists(backup_dir):
                for file in sorted(os.listdir(backup_dir), reverse=True):
                    self.backup_list.insert(tk.END, file)

    def on_game_select(self, event):
        if not self.game_list.curselection():
            return
        index = self.game_list.curselection()[0]
        self.selected_game = self.game_list.get(index)
        self.label_game.config(text=f"Juego: {self.selected_game}")
        self.btn_open_game.config(state=tk.NORMAL)
        self.btn_open_backup.config(state=tk.NORMAL)
        self.btn_create_copy.config(state=tk.NORMAL)
        self.refresh_backup_list()

    def add_game(self):
        name = simpledialog.askstring("Nombre del juego", "Introduce el nombre del juego:", parent=self.root)
        if not name:
            return
        game_folder = filedialog.askdirectory(title="Selecciona la carpeta del juego")
        if not game_folder:
            return
        backup_folder = filedialog.askdirectory(title="Selecciona la carpeta donde guardar las copias")
        if not backup_folder:
            return
        game_backup_dir = os.path.join(backup_folder, name)
        os.makedirs(game_backup_dir, exist_ok=True)
        self.games[name] = {"game_dir": game_folder, "backup_dir": game_backup_dir}
        self.save_config()
        self.refresh_game_list()

    def delete_game(self):
        if self.selected_game:
            if messagebox.askyesno("Confirmar", f"¿Eliminar el juego '{self.selected_game}' de la lista?"):
                self.games.pop(self.selected_game)
                self.save_config()
                self.selected_game = None
                self.label_game.config(text="Selecciona un juego")
                self.btn_open_game.config(state=tk.DISABLED)
                self.btn_open_backup.config(state=tk.DISABLED)
                self.btn_create_copy.config(state=tk.DISABLED)
                self.refresh_game_list()
                self.backup_list.delete(0, tk.END)

    def open_game_folder(self):
        if self.selected_game:
            os.startfile(self.games[self.selected_game]["game_dir"])

    def open_backup_folder(self):
        if self.selected_game:
            os.startfile(self.games[self.selected_game]["backup_dir"])

    def create_backup(self):
        if not self.selected_game:
            return
        backup_dir = self.games[self.selected_game]["backup_dir"]
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = os.path.join(backup_dir, f"{self.selected_game}_{timestamp}.zip")

        progress_win = tk.Toplevel(self.root)
        progress_win.title("Creando copia...")
        tk.Label(progress_win, text="Creando copia, por favor espera...").pack(padx=20, pady=20)
        self.center_window(progress_win)
        progress_bar = ttk.Progressbar(progress_win, mode="determinate", length=300)
        progress_bar.pack(padx=20, pady=10)

        def run_backup():
            game_dir = self.games[self.selected_game]["game_dir"]
            files = []
            for root_dir, _, filenames in os.walk(game_dir):
                for f in filenames:
                    files.append(os.path.join(root_dir, f))
            total = len(files)
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for i, file in enumerate(files, 1):
                    arcname = os.path.relpath(file, game_dir)
                    zipf.write(file, arcname)
                    progress_bar["value"] = (i / total) * 100
                    progress_bar.update()

            progress_win.destroy()
            messagebox.showinfo("Completado", f"Copia creada:\n{zip_name}", parent=self.root)
            self.refresh_backup_list()

        threading.Thread(target=run_backup).start()

    def restore_backup(self):
        if not self.selected_game or not self.backup_list.curselection():
            return
        selected_file = self.backup_list.get(self.backup_list.curselection())
        backup_path = os.path.join(self.games[self.selected_game]["backup_dir"], selected_file)
        if messagebox.askyesno("Restaurar", "¿Restaurar esta copia? Se sobrescribirán los archivos del juego."):
            game_dir = self.games[self.selected_game]["game_dir"]
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(game_dir)
            messagebox.showinfo("Restaurado", "Copia restaurada correctamente.", parent=self.root)

    def delete_backup(self):
        if not self.selected_game or not self.backup_list.curselection():
            return
        selected_file = self.backup_list.get(self.backup_list.curselection())
        backup_path = os.path.join(self.games[self.selected_game]["backup_dir"], selected_file)
        if messagebox.askyesno("Eliminar", f"¿Eliminar la copia '{selected_file}'?"):
            os.remove(backup_path)
            self.refresh_backup_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = BackupApp(root)
    root.mainloop()
