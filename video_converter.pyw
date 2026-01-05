import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
from moviepy import VideoFileClip
from PIL import Image

# --- KONFIGURATION DES DESIGNS (DARK MODE) ---
COLOR_BG = "#2b2b2b"        # Dunkelgrau (Hintergrund)
COLOR_FG = "#ffffff"        # Weiß (Text)
COLOR_ACCENT = "#007acc"    # Blau (Buttons)
COLOR_ACCENT_HOVER = "#005f9e"
COLOR_ENTRY = "#3a3a3a"     # Eingabefelder
COLOR_LOG = "#1e1e1e"       # Log-Hintergrund
FONT_MAIN = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")

class ModernConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Konverter Pro (+Metadaten)")
        self.root.geometry("600x450")
        self.root.configure(bg=COLOR_BG)

        # Variablen
        self.folder_path = tk.StringVar()
        self.source_format = tk.StringVar(value="* (Alle)")
        self.target_format = tk.StringVar(value=".mp4")
        self.move_originals = tk.BooleanVar(value=True)

        # --- STYLE SETTINGS FÜR TTK WIDGETS ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=COLOR_ENTRY, background=COLOR_BG, foreground=COLOR_FG, arrowcolor="white")
        style.configure("Horizontal.TProgressbar", background=COLOR_ACCENT, troughcolor=COLOR_ENTRY, bordercolor=COLOR_BG)

        # --- LAYOUT AUFBAU ---
        
        # 1. Header / Ordnerwahl
        frame_top = tk.Frame(root, bg=COLOR_BG)
        frame_top.pack(fill="x", padx=20, pady=(20, 10))

        tk.Label(frame_top, text="Quell-Ordner:", font=FONT_BOLD, bg=COLOR_BG, fg=COLOR_FG).pack(anchor="w")
        
        frame_input = tk.Frame(frame_top, bg=COLOR_BG)
        frame_input.pack(fill="x", pady=5)

        self.entry = tk.Entry(frame_input, textvariable=self.folder_path, bg=COLOR_ENTRY, fg=COLOR_FG, insertbackground="white", relief="flat", font=FONT_MAIN)
        self.entry.pack(side=tk.LEFT, fill="x", expand=True, ipady=4, padx=(0, 10))

        btn_browse = tk.Button(frame_input, text="📂 Suchen", command=self.select_folder, 
                               bg=COLOR_ENTRY, fg=COLOR_FG, activebackground=COLOR_ACCENT, 
                               relief="flat", font=FONT_MAIN, padx=10)
        btn_browse.pack(side=tk.RIGHT)

        # 2. Formatauswahl
        frame_formats = tk.Frame(root, bg=COLOR_BG)
        frame_formats.pack(fill="x", padx=20, pady=10)

        # Quellformat
        frame_src = tk.Frame(frame_formats, bg=COLOR_BG)
        frame_src.pack(side=tk.LEFT, expand=True, fill="x", padx=(0, 5))
        tk.Label(frame_src, text="Nur Dateien vom Typ:", font=FONT_MAIN, bg=COLOR_BG, fg="#aaaaaa").pack(anchor="w")
        
        src_opts = ["* (Alle)", ".mov", ".mp4", ".webm", ".avi", ".mkv", ".jpg", ".jpeg", ".png", ".gif"]
        self.combo_src = ttk.Combobox(frame_src, values=src_opts, textvariable=self.source_format, state="readonly")
        self.combo_src.pack(fill="x", pady=2)

        tk.Label(frame_formats, text="➜", font=("Arial", 16), bg=COLOR_BG, fg=COLOR_ACCENT).pack(side=tk.LEFT, padx=10, pady=(15,0))

        # Zielformat
        frame_dest = tk.Frame(frame_formats, bg=COLOR_BG)
        frame_dest.pack(side=tk.LEFT, expand=True, fill="x", padx=(5, 0))
        tk.Label(frame_dest, text="Konvertieren in:", font=FONT_MAIN, bg=COLOR_BG, fg="#aaaaaa").pack(anchor="w")
        
        dest_opts = [".mp4", ".mov", ".webm", ".gif", ".jpg", ".png"]
        self.combo_dest = ttk.Combobox(frame_dest, values=dest_opts, textvariable=self.target_format, state="readonly")
        self.combo_dest.pack(fill="x", pady=2)

        # 3. Optionen
        frame_opt = tk.Frame(root, bg=COLOR_BG)
        frame_opt.pack(fill="x", padx=20, pady=10)
        
        chk = tk.Checkbutton(frame_opt, text="Originale nach Erfolg in '_ERLEDIGT' verschieben", 
                             var=self.move_originals, bg=COLOR_BG, fg="#dddddd", 
                             selectcolor=COLOR_BG, activebackground=COLOR_BG, activeforeground=COLOR_FG,
                             font=FONT_MAIN)
        chk.pack(anchor="w")

        # 4. Buttons
        self.btn_start = tk.Button(root, text="KONVERTIERUNG STARTEN", command=self.start_conversion,
                                   bg=COLOR_ACCENT, fg="white", activebackground=COLOR_ACCENT_HOVER, activeforeground="white",
                                   relief="flat", font=("Segoe UI", 11, "bold"), cursor="hand2")
        self.btn_start.pack(fill="x", padx=20, pady=(10, 5), ipady=5)

        self.progress = ttk.Progressbar(root, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", padx=20, pady=5)

        # 5. Log
        self.log_area = scrolledtext.ScrolledText(root, height=6, bg=COLOR_LOG, fg="#cccccc", 
                                                  font=("Consolas", 9), relief="flat", state='disabled')
        self.log_area.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, "> " + message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')
        self.root.update()

    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path.set(path)

    def start_conversion(self):
        folder = self.folder_path.get()
        src_filter = self.source_format.get()
        target_ext = self.target_format.get()
        should_move = self.move_originals.get()

        if not folder:
            self.log("FEHLER: Bitte erst einen Ordner auswählen!")
            return

        video_exts = ['.mov', '.mp4', '.webm', '.gif', '.avi', '.mkv', '.m4v']
        image_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.webp', '.heic']
        all_exts = video_exts + image_exts

        self.log(f"Starte... Metadaten werden bestmöglich erhalten.")

        done_folder = os.path.join(folder, "_ERLEDIGT")
        if should_move and not os.path.exists(done_folder):
            try: os.makedirs(done_folder)
            except: pass

        files = os.listdir(folder)
        files_to_process = []

        for f in files:
            if os.path.isdir(os.path.join(folder, f)): continue
            ext = os.path.splitext(f)[1].lower()
            
            if src_filter != "* (Alle)":
                if ext != src_filter: continue 
            else:
                if ext not in all_exts: continue 

            files_to_process.append(f)

        if not files_to_process:
            self.log("Keine passenden Dateien gefunden.")
            return

        self.progress["maximum"] = len(files_to_process)
        self.progress["value"] = 0
        success_count = 0

        for i, filename in enumerate(files_to_process):
            input_path = os.path.join(folder, filename)
            new_filename = os.path.splitext(filename)[0] + target_ext
            output_path = os.path.join(folder, new_filename)
            input_ext = os.path.splitext(filename)[1].lower()

            is_video_in = input_ext in video_exts
            is_image_in = input_ext in image_exts
            is_video_out = target_ext in video_exts
            is_image_out = target_ext in image_exts

            success = False

            if input_path == output_path:
                self.log(f"Ignoriere {filename} (Input = Output)")
            elif is_video_in and is_video_out:
                success = self.convert_video(input_path, output_path, target_ext)
            elif is_image_in and is_image_out:
                success = self.convert_image(input_path, output_path, target_ext)
            else:
                self.log(f"Überspringe {filename}: Typ-Konflikt")

            if success:
                # WICHTIG: Dateidatum (Modified Date) vom Original auf die neue Datei kopieren
                try:
                    shutil.copystat(input_path, output_path)
                except Exception as e:
                    self.log(f"Warnung: Zeitstempel konnte nicht kopiert werden: {e}")

                success_count += 1
                if should_move:
                    try:
                        shutil.move(input_path, os.path.join(done_folder, filename))
                    except Exception as e:
                        self.log(f"Verschieben fehlgeschlagen: {e}")

            self.progress["value"] = i + 1
            self.root.update()

        self.log(f"Fertig! {success_count} Dateien verarbeitet.")

    def convert_video(self, in_path, out_path, ext):
        try:
            self.log(f"Video: {os.path.basename(in_path)}...")
            with VideoFileClip(in_path) as clip:
                if ext == ".gif":
                    clip.write_gif(out_path, program='ffmpeg', logger=None)
                else:
                    v_codec = 'libvpx' if ext == ".webm" else 'libx264'
                    clip.write_videofile(out_path, codec=v_codec, audio_codec='aac', 
                                         temp_audiofile='temp-audio.m4a', remove_temp=True, logger=None)
            return True
        except Exception as e:
            self.log(f"Fehler: {e}")
            return False

    def convert_image(self, in_path, out_path, ext):
        try:
            self.log(f"Bild: {os.path.basename(in_path)}...")
            with Image.open(in_path) as img:
                # 1. EXIF-Daten auslesen (falls vorhanden)
                exif_data = img.info.get('exif')

                # 2. Transparenz behandeln
                if ext in ['.jpg', '.jpeg'] and img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert("RGBA")
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                
                rgb_img = img.convert('RGB') if ext in ['.jpg', '.jpeg'] else img
                
                # 3. Speichern MIT EXIF-Daten, wenn Zielformat JPG ist
                if ext in ['.jpg', '.jpeg'] and exif_data:
                    try:
                        rgb_img.save(out_path, quality=95, exif=exif_data)
                    except:
                        # Falls EXIF kaputt ist, ohne speichern
                        rgb_img.save(out_path, quality=95)
                else:
                    # Für PNG oder wenn keine EXIF da waren
                    rgb_img.save(out_path, quality=95)
                    
            return True
        except Exception as e:
            self.log(f"Fehler: {e}")
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernConverter(root)
    root.mainloop()
