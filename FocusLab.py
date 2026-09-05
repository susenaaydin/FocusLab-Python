import customtkinter as ctk
import threading
import time
import json
from datetime import date
import os

DATA_FILE = "data.json"

THEME_COLORS = {
    "Pink": {"bg":"#ffc0cb", "btn":"#ff69b4", "hover":"#ff85c1", "text":"#900c3f"},
    "Dark Pink": {"bg":"#d1477f", "btn":"#ff1493", "hover":"#ff69b4", "text":"white"},
    "Metal": {"bg":"#2b2b2b", "btn":"#5a5a5a", "hover":"#7a7a7a", "text":"white"},
    "Purple": {"bg":"#9b59b6", "btn":"#8e44ad", "hover":"#a64ca6", "text":"white"},
    "Blue": {"bg":"#87ceeb", "btn":"#1e90ff", "hover":"#6495ed", "text":"white"},
    "Midnight": {"bg":"#1c1c1c", "btn":"#2c2c2c", "hover":"#444", "text":"white"},
    "Lilac": {"bg":"#e6cfe6", "btn":"#d4a6d4", "hover":"#d8b2d8", "text":"#5a2a5a"},
    "Mint": {"bg":"#c1f0c1", "btn":"#2ecc71", "hover":"#58d68d", "text":"#145214"},
    "Sunset Orange": {"bg":"#ffd1a4", "btn":"#ff7f50", "hover":"#ffa07a", "text":"#8b3e2f"}
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            tasks = data.get("tasks", [])
            new_tasks = []
            for t in tasks:
                if isinstance(t, str):
                    new_tasks.append({"name": t, "done": False, "time": str(date.today()), "duration":0, "display": t})
                else:
                    new_tasks.append(t)
            data["tasks"] = new_tasks
            if "history" not in data:
                data["history"] = {}
            return data
    else:
        return {"theme":"Pink", "categories":[], "tasks":[], "history":{}}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

class FocusLab(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.data = load_data()
        self.current_theme = self.data.get("theme", "Pink")

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("FocusLab")
        self.geometry("950x600")

        self.daily_seconds = 0
        self.task_list_data = self.data.get("tasks", [])
        self.cat_list_data = self.data.get("categories", [])
        self.history_data = self.data.get("history", {})

        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        buttons = [
            ("Kronometre", self.show_chrono),
            ("Zamanlayıcı", self.show_timer),
            ("Günlük Planlayıcı", self.show_daily),
            ("Takvim", self.show_calendar),
            ("İstatistik", self.show_stats),
            ("Tema Seç", self.show_theme_selector),
        ]

        self.sidebar_buttons = []
        for text, cmd in buttons:
            btn = ctk.CTkButton(self.sidebar, text=text, command=cmd)
            btn.pack(pady=15, padx=20)
            self.sidebar_buttons.append(btn)

        self.main = ctk.CTkFrame(self, corner_radius=15)
        self.main.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        self.chrono_running = False
        self.chrono_seconds = 0
        self.timer_running = False

        self.apply_theme()
        self.show_chrono()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def apply_theme(self):
        colors = THEME_COLORS[self.current_theme]
        self.main.configure(fg_color=colors["bg"])
        self.sidebar.configure(fg_color=colors["bg"])
        for btn in self.sidebar_buttons:
            btn.configure(fg_color=colors["btn"], hover_color=colors["hover"], text_color=colors["text"])

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.data["theme"] = theme_name
        self.apply_theme()
        save_data(self.data)

    def clear_main(self):
        for w in self.main.winfo_children():
            w.destroy()

    # --- Kronometre ---
    def show_chrono(self):
        self.clear_main()
        colors = THEME_COLORS[self.current_theme]

        ctk.CTkLabel(self.main, text="Kronometre", font=("Arial", 30, "bold"), text_color=colors["text"]).pack(pady=20)
        self.chrono_label = ctk.CTkLabel(self.main, text="00:00:00", font=("Arial", 45, "bold"), text_color=colors["text"])
        self.chrono_label.pack(pady=20)

        frame = ctk.CTkFrame(self.main, fg_color=colors["bg"])
        frame.pack(pady=10)
        ctk.CTkButton(frame, text="Başlat", command=self.start_chrono, fg_color=colors["btn"], hover_color=colors["hover"]).pack(side="left", padx=10)
        ctk.CTkButton(frame, text="Durdur", command=self.stop_chrono, fg_color=colors["btn"], hover_color=colors["hover"]).pack(side="left", padx=10)
        ctk.CTkButton(frame, text="Sıfırla", command=self.reset_chrono, fg_color=colors["btn"], hover_color=colors["hover"]).pack(side="left", padx=10)

        if self.cat_list_data:
            self.chrono_cat_option = ctk.CTkOptionMenu(self.main, values=self.cat_list_data)
            self.chrono_cat_option.pack(pady=10)

    def start_chrono(self):
        if not self.chrono_running:
            self.chrono_running = True
            threading.Thread(target=self.run_chrono, daemon=True).start()

    def run_chrono(self):
        while self.chrono_running:
            time.sleep(1)
            self.chrono_seconds += 1
            self.daily_seconds += 1
            today_str = str(date.today())
            if today_str not in self.history_data:
                self.history_data[today_str] = 0
            self.history_data[today_str] += 1
            h = self.chrono_seconds // 3600
            m = (self.chrono_seconds % 3600) // 60
            s = self.chrono_seconds % 60
            self.chrono_label.configure(text=f"{h:02d}:{m:02d}:{s:02d}")
        # Kronometre durduğunda süreyi görev listesine ekle
        self.add_time_to_task(self.chrono_seconds)
        self.chrono_seconds = 0

    def stop_chrono(self):
        self.chrono_running = False

    def reset_chrono(self):
        self.chrono_running = False
        self.chrono_seconds = 0
        self.chrono_label.configure(text="00:00:00")

    # --- Zamanlayıcı ---
    def show_timer(self):
        self.clear_main()
        colors = THEME_COLORS[self.current_theme]

        ctk.CTkLabel(self.main, text="Zamanlayıcı", font=("Arial", 30, "bold"), text_color=colors["text"]).pack(pady=20)
        self.timer_label = ctk.CTkLabel(self.main, text="00:00", font=("Arial", 40, "bold"), text_color=colors["text"])
        self.timer_label.pack(pady=20)

        btn_frame = ctk.CTkFrame(self.main, fg_color=colors["bg"])
        btn_frame.pack(pady=5)
        for m in [10, 25, 45]:
            ctk.CTkButton(btn_frame, text=f"{m} dk", command=lambda x=m: self.start_countdown(x*60), fg_color=colors["btn"], hover_color=colors["hover"]).pack(side="left", padx=10)

        ctk.CTkLabel(self.main, text="Özel süre (dakika):", text_color=colors["text"]).pack()
        self.custom_timer = ctk.CTkEntry(self.main)
        self.custom_timer.pack(pady=5)
        ctk.CTkButton(self.main, text="Başlat", command=self.start_custom_timer, fg_color=colors["btn"], hover_color=colors["hover"]).pack(pady=5)

        if self.cat_list_data:
            self.timer_cat_option = ctk.CTkOptionMenu(self.main, values=self.cat_list_data)
            self.timer_cat_option.pack(pady=10)

    def start_custom_timer(self):
        try:
            minutes = int(self.custom_timer.get())
            self.start_countdown(minutes*60)
        except:
            pass

    def start_countdown(self, total_seconds):
        if self.timer_running:
            return
        self.timer_running = True
        threading.Thread(target=self.run_countdown, args=(total_seconds,), daemon=True).start()

    def run_countdown(self, sec):
        while sec >= 0 and self.timer_running:
            m = sec // 60
            s = sec % 60
            self.timer_label.configure(text=f"{m:02d}:{s:02d}")
            time.sleep(1)
            sec -= 1
        self.timer_running = False
        self.add_time_to_task(sec)  # kalan saniye değil, toplam zamanı ekle

    # --- Görev ve kategori yönetimi ---
    def show_daily(self):
        self.clear_main()
        colors = THEME_COLORS[self.current_theme]

        ctk.CTkLabel(self.main, text="Günlük Planlayıcı", font=("Arial", 30, "bold"), text_color=colors["text"]).pack(pady=10)

        # Kategoriler
        ctk.CTkLabel(self.main, text="Kategoriler:", font=("Arial", 16, "bold"), text_color=colors["text"]).pack()
        self.cat_entry = ctk.CTkEntry(self.main, placeholder_text="Yeni kategori ekle…")
        self.cat_entry.pack(pady=5)
        ctk.CTkButton(self.main, text="Kategori Ekle", command=self.add_category, fg_color=colors["btn"], hover_color=colors["hover"]).pack(pady=5)
        self.cat_listbox = ctk.CTkFrame(self.main)
        self.cat_listbox.pack(pady=10)
        self.refresh_categories()

        # Görevler
        ctk.CTkLabel(self.main, text="Görevler:", font=("Arial", 16, "bold"), text_color=colors["text"]).pack()
        self.task_entry = ctk.CTkEntry(self.main, placeholder_text="Görev ekle…")
        self.task_entry.pack(pady=5)
        ctk.CTkButton(self.main, text="Görev Ekle", command=self.add_task, fg_color=colors["btn"], hover_color=colors["hover"]).pack(pady=5)
        self.task_listbox = ctk.CTkFrame(self.main)
        self.task_listbox.pack(pady=10)
        self.refresh_tasks()

    def refresh_categories(self):
        for widget in self.cat_listbox.winfo_children():
            widget.destroy()
        for idx, cat in enumerate(self.cat_list_data):
            frame = ctk.CTkFrame(self.cat_listbox, fg_color="transparent")
            frame.pack(fill="x", pady=2)
            ctk.CTkLabel(frame, text=cat, width=200, anchor="w").pack(side="left", padx=5)
            ctk.CTkButton(frame, text="Sil", width=50, command=lambda i=idx: self.delete_category(i)).pack(side="right", padx=5)

    def refresh_tasks(self):
        for widget in self.task_listbox.winfo_children():
            widget.destroy()
        for idx, task in enumerate(self.task_list_data):
            frame = ctk.CTkFrame(self.task_listbox, fg_color="transparent")
            frame.pack(fill="x", pady=2)
            mark = "✔" if task.get("done") else "✖"
            text_to_show = task.get("display", task["name"])
            ctk.CTkLabel(frame, text=f"{mark} {text_to_show}", width=200, anchor="w").pack(side="left", padx=5)
            ctk.CTkButton(frame, text="Sil", width=50, command=lambda i=idx: self.delete_task(i)).pack(side="right", padx=5)

    def add_category(self):
        t = self.cat_entry.get().strip()
        if t:
            self.cat_list_data.append(t)
            self.data["categories"] = self.cat_list_data
            self.cat_entry.delete(0, "end")
            self.refresh_categories()
            save_data(self.data)

    def add_task(self):
        t = self.task_entry.get().strip()
        if t:
            task_dict = {"name": t, "done": False, "time": str(date.today()), "duration":0, "display":t}
            self.task_list_data.append(task_dict)
            self.task_entry.delete(0, "end")
            self.refresh_tasks()
            save_data(self.data)

    def delete_category(self, idx):
        cat = self.cat_list_data.pop(idx)
        self.data["categories"] = self.cat_list_data
        if hasattr(self, 'chrono_cat_option') and cat in self.chrono_cat_option._values:
            self.chrono_cat_option._values.remove(cat)
        if hasattr(self, 'timer_cat_option') and cat in self.timer_cat_option._values:
            self.timer_cat_option._values.remove(cat)
        self.refresh_categories()
        save_data(self.data)

    def delete_task(self, idx):
        self.task_list_data.pop(idx)
        self.refresh_tasks()
        save_data(self.data)

    def add_time_to_task(self, seconds):
        if seconds <= 0: return
        cat_name = ""
        if hasattr(self,'chrono_cat_option'):
            cat_name = self.chrono_cat_option.get()
        if hasattr(self,'timer_cat_option'):
            cat_name = self.timer_cat_option.get()
        task_name = cat_name if cat_name else "Genel"
        duration_min = seconds // 60
        task_dict = {
            "name": task_name,
            "done": True,
            "duration": duration_min,
            "time": str(date.today()),
            "display": f"{task_name} - {duration_min} dk"
        }
        self.task_list_data.append(task_dict)
        save_data(self.data)
        self.refresh_tasks()

    # --- Takvim ve İstatistik ---
    def show_calendar(self):
        self.clear_main()
        colors = THEME_COLORS[self.current_theme]
        ctk.CTkLabel(self.main, text="Takvim", font=("Arial", 30, "bold"), text_color=colors["text"]).pack(pady=20)
        today = date.today()
        ctk.CTkLabel(self.main, text=f"Bugün: {today}", font=("Arial", 18), text_color=colors["text"]).pack(pady=10)
        for day, seconds in self.history_data.items():
            h = seconds // 3600
            m = (seconds % 3600) // 60
            ctk.CTkLabel(self.main, text=f"{day}: {h} saat {m} dakika", font=("Arial", 14), text_color=colors["text"]).pack()

    def show_stats(self):
        self.clear_main()
        colors = THEME_COLORS[self.current_theme]
        ctk.CTkLabel(self.main, text="İstatistik", font=("Arial", 30, "bold"), text_color=colors["text"]).pack(pady=20)
        h = self.daily_seconds // 3600
        m = (self.daily_seconds % 3600) // 60
        ctk.CTkLabel(self.main, text=f"Bugün toplam çalışma: {h} saat {m} dakika", font=("Arial", 20), text_color=colors["text"]).pack(pady=20)

    # --- Tema ---
    def show_theme_selector(self):
        self.clear_main()
        ctk.CTkLabel(self.main, text="Tema Seçimi", font=("Arial", 30, "bold")).pack(pady=20)
        for name in THEME_COLORS.keys():
            ctk.CTkButton(self.main, text=name, command=lambda n=name: self.change_theme(n)).pack(pady=8)

    def on_close(self):
        self.data["tasks"] = self.task_list_data
        self.data["categories"] = self.cat_list_data
        self.data["theme"] = self.current_theme
        self.data["history"] = self.history_data
        save_data(self.data)
        self.destroy()

if __name__ == "__main__":
    FocusLab().mainloop()
