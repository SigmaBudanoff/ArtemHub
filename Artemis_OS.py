import os
import sys
import time
import tkinter as tk
from tkinter import ttk, messagebox
from time import strftime
import winsound
import qrcode # type: ignore
import requests # type: ignore
import platform
import psutil # type: ignore
import socket
import subprocess
from googletrans import Translator, LANGUAGES # type: ignore
from io import BytesIO
from PIL import Image, ImageTk # type: ignore
from datetime import datetime

def center_window(window, width, height):
    # Отримуємо ширину та висоту екрана користувача
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Розраховуємо координати X та Y для центру
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Встановлюємо розмір та позицію: "ШиринаxВисота+X+Y"
    window.geometry(f'{width}x{height}+{x}+{y}')

def quit_system():
    # Можна додати запит "Ви впевнені?", але для швидкості зробимо прямий вихід
    root.destroy() # Закриваємо вікно
    sys.exit()     # Повністю зупиняємо процес Python

def update_info_panel():
    current_time = time.strftime('%H:%M:%S')
    current_date = time.strftime('%d.%m.%Y')
    time_label.config(text=current_time)
    date_label.config(text=current_date)
    root.after(1000, update_info_panel)

def update_info_panel():
    # Отримуємо час і дату через strftime
    string_time = strftime('%H:%M:%S')
    string_date = strftime('%d.%m.%Y')

    # Оновлюємо текст у віджетах
    time_label.config(text=string_time)
    date_label.config(text=string_date)

    # Повторюємо через 1 секунду
    root.after(1000, update_info_panel)

# 1. НАЛАШТУВАННЯ ШЛЯХІВ (Правильно для EXE)
if hasattr(sys, '_MEIPASS'):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. НАЛАШТУВАННЯ ШЛЯХІВ
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "lib", "site-packages"))

try:
    from PIL import Image, ImageTk # type: ignore
    PILLOW_INSTALLED = True
except ImportError:
    PILLOW_INSTALLED = False

# === ФУНКЦІЯ ОНОВЛЕННЯ (UPDATE SYSTEM) ===

def run_update_process():
    import os, sys, subprocess, threading, time
    from tkinter import messagebox

    # 1. Визначаємо робочу папку
    if getattr(sys, 'frozen', False):
        exe_path = os.path.abspath(sys.executable)
        exe_dir = os.path.dirname(exe_path)
    else:
        exe_dir = os.path.dirname(os.path.abspath(__file__))

    # Якщо програма всередині dist, виходимо на рівень вище
    if os.path.basename(exe_dir).lower() == "dist":
        exe_dir = os.path.dirname(exe_dir)

    os.chdir(exe_dir)
    build_script = "Консоль.bat"
    full_path = os.path.join(exe_dir, build_script)

    if not os.path.exists(full_path):
        messagebox.showerror("Шлях до батника", f"Файл не знайдено:\n{full_path}")
        return

    root.title("Artemis Hub [ ОНОВЛЕННЯ... ]")
    root.update()
    messagebox.showinfo("Artemis OS", "Зараз відкриється вікно збірки. НЕ ЗАКРИВАЙ ЙОГО!")

    def wait_and_finish():
        try:
            # Запускаємо термінал збірки
            os.startfile(full_path)
            
            # Шукаємо новий файл
            new_exe = os.path.join(exe_dir, "dist", "Artemis_NEW.exe")
            current_exe_name = os.path.basename(sys.executable)
            
            found = False
            for _ in range(180): # Чекаємо до 3 хвилин
                time.sleep(1)
                if os.path.exists(new_exe):
                    time.sleep(3) # Даємо час дозаписати файл на диск
                    found = True
                    break
            
            if found:
                bat_path = os.path.join(exe_dir, "update_fix.bat")
                
                # Створюємо посилений батник для заміни файлів
                with open(bat_path, "w", encoding="utf-8") as f:
                    f.write(f"""@echo off
chcp 65001 > nul
echo [ Artemis OS Update System ]
echo Очікування повного закриття програми...

:retry_kill
taskkill /f /im "{current_exe_name}" > nul 2>&1
timeout /t 2 /nobreak > nul

:retry_del
del /f "{os.path.join(exe_dir, current_exe_name)}" > nul 2>&1

if exist "{os.path.join(exe_dir, current_exe_name)}" (
    echo Файл ще зайнятий системою... Пробую знову...
    goto retry_kill
)

echo Встановлення нової версії...
move /y "{new_exe}" "{os.path.join(exe_dir, current_exe_name)}"

echo Очищення сміття...
rd /s /q "{os.path.join(exe_dir, 'dist')}" 2>nul
rd /s /q "{os.path.join(exe_dir, 'build')}" 2>nul
del /q *.spec 2>nul

echo Перезапуск...
start "" "{os.path.join(exe_dir, current_exe_name)}"
del "%~f0"
""")
                # Запускаємо батник і миттєво вбиваємо поточну програму
                subprocess.Popen(["cmd", "/c", bat_path], shell=True)
                os._exit(0)
            else:
                root.title("Artemis Hub")
                messagebox.showerror("Error", "Збірка не вдалася або тривала занадто довго.")
        
        except Exception as e:
            messagebox.showerror("Критична помилка", f"{e}")

    threading.Thread(target=wait_and_finish, daemon=True).start()

# === ФУНКЦІЇ МОДУЛІВ ===

def open_clock():
    clock_window = tk.Toplevel(root)
    clock_window.title("Модуль: Годинник")
    center_window(clock_window, 450, 400)
    clock_window.config(bg="#2c3e50")
    
    label_clock = tk.Label(clock_window, font=("Consolas", 60, "bold"), bg="#2c3e50", fg="white")
    label_clock.pack(pady=10)
    
    # Дата: тепер теж на синьому фоні та з білим текстом
    label_date = tk.Label(clock_window, font=("Arial", 12), 
                          bg="#2c3e50", fg="white")
    label_date.pack()

    # Пояснювальний напис для будильника
    tk.Label(clock_window, text="ВСТАНОВИТИ БУДИЛЬНИК (HH:MM:SS):", 
             font=("Arial", 8, "bold"), bg="#2c3e50", fg="#bdc3c7").pack(pady=(20, 0))

    # Поле вводу: зробимо його трохи світлішим синім, щоб виділялося
    entry_alarm = tk.Entry(clock_window, font=("Consolas", 20), justify='center', 
                           width=10, bg="#34495e", fg="#00FF00", bd=0)
    entry_alarm.insert(0, "00:00:00")
    entry_alarm.pack(pady=10)

    def update_clock():
        curr = strftime('%H:%M:%S')
        label_clock.config(text=curr)
        label_date.config(text=strftime('%A, %d %B %Y'))
        if curr == entry_alarm.get():
            alarm_path = os.path.join(BASE_DIR, "alarm.wav")
            if os.path.exists(alarm_path):
                winsound.PlaySound(alarm_path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
        label_clock.after(1000, update_clock)

    tk.Button(clock_window, text="ВИМКНУТИ ЗВУК", command=lambda: winsound.PlaySound(None, winsound.SND_PURGE), bg="#cc0000", fg="white").pack(pady=10)
    update_clock()

def open_translator():
    trans_window = tk.Toplevel(root)
    trans_window.title("Модуль: Перекладач")
    center_window(trans_window, 600, 400)
    trans_window.config(bg="#2c3e50")

    tk.Label(trans_window, text="Введіть текст:", bg="#2c3e50", fg="white", font=("Arial", 10, "bold")).pack(pady=(20, 5))
    in_text = tk.Text(trans_window, height=5, width=40, bg="#34495e", fg="white", bd=0, padx=10, pady=10)
    in_text.pack(padx=20)
    
    lang_names = list(LANGUAGES.values())
    combo_dest = ttk.Combobox(trans_window, values=lang_names, state="readonly")
    combo_dest.set("ukrainian")
    combo_dest.pack(pady=10)
    
    out_text = tk.Text(trans_window, height=5, width=40, bg="#34495e", fg="#bdc3c7", bd=0, padx=10, pady=10, state=tk.DISABLED)

    def translate():
        text = in_text.get("1.0", tk.END).strip()
        if text:
            try:
                dest_code = [code for code, name in LANGUAGES.items() if name == combo_dest.get()][0]
                res = Translator().translate(text, dest=dest_code)
                out_text.config(state=tk.NORMAL)
                out_text.delete("1.0", tk.END)
                out_text.insert(tk.END, res.text)
                out_text.config(state=tk.DISABLED)
            except Exception as e: messagebox.showerror("Помилка", str(e))

    tk.Button(trans_window, text="Перекласти", command=translate, bg="#27ae60", fg="white", 
              font=("Arial", 10, "bold"), relief="flat", padx=20, pady=5).pack(pady=10)
    out_text.pack(padx=20)

def open_qr():
    qr_window = tk.Toplevel(root)
    qr_window.title("QR Генератор")
    center_window(qr_window, 350, 450)
    qr_window.config(bg="#2c3e50")
    
    entry_url = tk.Entry(qr_window, width=25, font=("Arial", 12))
    entry_url.pack(pady=20)
    label_img = tk.Label(qr_window, bg="#2c3e50")
    label_img.pack()

    def generate():
        if entry_url.get():
            img = qrcode.make(entry_url.get()).resize((200, 200))
            img_tk = ImageTk.PhotoImage(img)
            label_img.config(image=img_tk); label_img.image = img_tk
    
    tk.Button(qr_window, text="Згенерувати", command=generate, bg="#8e44ad", fg="white").pack(pady=10)

def open_weather():
    weather_win = tk.Toplevel(root)
    weather_win.title("Прогноз на 7 днів")
    center_window(weather_win, 600, 400)
    weather_win.config(bg="#34495e")

    ctrl_frame = tk.Frame(weather_win, bg="#34495e")
    ctrl_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

    tk.Label(ctrl_frame, text="Місто:", bg="#34495e", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)
    city_entry = tk.Entry(ctrl_frame, font=("Arial", 12), width=15)
    city_entry.insert(0, "Rivne")
    city_entry.pack(side=tk.LEFT, padx=5)

    res_text = tk.Text(weather_win, font=("Consolas", 11), bg="#2c3e50", fg="#ecf0f1", bd=0, padx=15, pady=15)
    res_text.pack(side=tk.BOTTOM, pady=10, padx=20, expand=True, fill="both")

    def get_weather():
        city = city_entry.get().strip() # Прибираємо випадкові пробіли
        if not city:
            messagebox.showwarning("Увага", "Будь ласка, введіть назву міста.")
            return

        try:
            # Додаємо timeout=5, щоб програма не "висла", якщо сайт не відповідає
            response = requests.get(f"https://wttr.in/{city}?format=j1", timeout=5)
        
            # Перевірка на успішність запиту
            if response.status_code != 200:
                # Виводимо у вікно конкретний код помилки від сервера (напр. 404 або 429)
                messagebox.showerror("Помилка сервера", f"Сервер повернув код: {response.status_code}\nМожливо, місто введено неправильно або ліміт запитів вичерпано.")
                return

            data = response.json()
            output = f"ПРОГНОЗ ДЛЯ: {city.upper()}\n"
            output += "=" * 45 + "\n"
        
            for day in data['weather'][:7]:
                date = day['date']
                max_t = day['maxtempC']
                min_t = day['mintempC']
                hourly_info = day['hourly'][4]
                desc = hourly_info['weatherDesc'][0]['value']
                output += f"{date:<12} | {min_t:>3}°C...{max_t:>3}°C | {desc}\n"
        
            res_text.config(state=tk.NORMAL)
            res_text.delete("1.0", tk.END)
            res_text.insert(tk.END, output)
            res_text.config(state=tk.DISABLED)

        # Ловимо помилки мережі (без вискакуючих вікон, просто в консоль)
        except requests.exceptions.ConnectionError:
            print("[WEATHER ERROR] Відсутнє підключення до інтернету.")
            messagebox.showerror("Помилка", "Перевірте з'єднання з інтернетом.")
    
        except requests.exceptions.Timeout:
            print("[WEATHER ERROR] Сайт wttr.in не відповів вчасно.")
            messagebox.showerror("Помилка", "Час очікування відповіді вийшов. Спробуйте пізніше.")

        # Ловимо все інше (наприклад, помилки в структурі JSON)
        except Exception as e:
            print(f"[WEATHER CRITICAL] {e}")
            messagebox.showerror("Помилка", f"Сталася непередбачена помилка: {e}")

    tk.Button(ctrl_frame, text="ПОКАЗАТИ", command=get_weather, bg="#f1c40f", fg="black").pack(side=tk.LEFT, padx=10)
    get_weather()

def open_calculator():
    calc_win = tk.Toplevel(root)
    calc_win.title("Калькулятор")
    center_window(calc_win, 400, 500)
    calc_win.config(bg="#1a1a1a")

    entry = tk.Entry(calc_win, font=("Consolas", 25), justify='right', bg="#1a1a1a", fg="white", bd=0)
    entry.grid(row=0, column=0, columnspan=4, padx=20, pady=20, sticky="we")

    def click(char): entry.insert(tk.END, char)
    def clear(): entry.delete(0, tk.END)
    def calculate():
        try:
            res = eval(entry.get().replace('×', '*').replace('÷', '/'))
            entry.delete(0, tk.END); entry.insert(tk.END, str(res))
        except: messagebox.showerror("Error", "Невірний вираз")
    
    btns = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('÷', 1, 3, "#e67e22"),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('×', 2, 3, "#e67e22"),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3, "#e67e22"),
        ('C', 4, 0, "#e74c3c"), ('0', 4, 1), ('=', 4, 2, "#27ae60"), ('+', 4, 3, "#e67e22")
    ]
    for b in btns:
        text, r, c = b[0], b[1], b[2]
        bg = b[3] if len(b) > 3 else "#333"
        cmd = calculate if text == '=' else clear if text == 'C' else lambda x=text: click(x)
        tk.Button(calc_win, text=text, width=5, height=2, font=("Arial", 12, "bold"),
                  bg=bg, fg="white", relief="flat", command=cmd).grid(row=r, column=c, padx=5, pady=5)

def open_system_report():
    report_win = tk.Toplevel(root)
    report_win.title("System Monitor") # Версію ти додаси сам, як домовлялися
    center_window(report_win, 480, 650)
    report_win.configure(bg="#2c3e50")

    # --- 1. ОТРИМАННЯ КРАСИВОЇ НАЗВИ ПРОЦЕСОРА ---
    try:
        # Опитуємо Windows Management Instrumentation для отримання повної назви
        cpu_raw = os.popen("wmic cpu get name").read()
        clean_cpu = cpu_raw.replace("Name", "").strip()
        if not clean_cpu: # Якщо WMIC раптом не спрацював
            clean_cpu = platform.processor()
    except:
        clean_cpu = platform.processor()

    # --- 2. СТАТИЧНА ІНФОРМАЦІЯ ---
    header = tk.Label(report_win, text="ІНФОРМАЦІЯ ПРО СИСТЕМУ", font=("Arial", 12, "bold"), 
                      bg="#2c3e50", fg="#1abc9c")
    header.pack(pady=(20, 10))

    static_info = [
        f"DEVICE NAME  : {socket.gethostname()}",
        f"OS VERSION   : {platform.system()} {platform.release()}",
        f"PROCESSOR    : {clean_cpu}",
        f"TOTAL RAM    : {round(psutil.virtual_memory().total / (1024**3), 2)} GB",
        f"LOCAL IP     : {socket.gethostbyname(socket.gethostname())}",
        f"CURRENT USER : {os.getlogin()}",
        f"CPU CORES    : {psutil.cpu_count(logical=True)} Threads"
    ]

    for line in static_info:
        tk.Label(report_win, text=line, font=("Consolas", 9), bg="#2c3e50", fg="#bdc3c7", anchor="w", justify="left").pack(fill="x", padx=40)

    tk.Label(report_win, text="-" * 45, bg="#2c3e50", fg="#34495e").pack()

    # --- ДИНАМІЧНА ІНФОРМАЦІЯ (оновлюється кожні 2 сек) ---
    tk.Label(report_win, text="МЕТРИКИ РЕАЛЬНОГО ЧАСУ", font=("Arial", 10, "bold"), bg="#2c3e50", fg="#f1c40f").pack(pady=5)

    cpu_label = tk.Label(report_win, text="Завантаження CPU: ...", font=("Arial", 11), bg="#2c3e50", fg="white")
    cpu_label.pack(pady=5)

    ram_label = tk.Label(report_win, text="Використання RAM: ...", font=("Arial", 11), bg="#2c3e50", fg="white")
    ram_label.pack(pady=5)
    
    storage_label = tk.Label(report_win, text="Диск C:: ...", font=("Arial", 11), bg="#2c3e50", fg="white")
    storage_label.pack(pady=5)

    def update_stats():
        if not report_win.winfo_exists():
            return

        cpu_usage = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        cpu_label.config(text=f"Завантаження CPU: {cpu_usage}%")
        ram_label.config(text=f"Використання RAM: {ram.percent}% ({ram.used // (1024**2)} MB)")
        storage_label.config(text=f"Диск C: {disk.percent}% вільно")

        # Індикація перевантаження
        cpu_label.config(fg="#e74c3c" if cpu_usage > 80 else "white")
        ram_label.config(fg="#e74c3c" if ram.percent > 90 else "white")

        report_win.after(2000, update_stats)

    update_stats()

    # Кнопки внизу
    btn_frame = tk.Frame(report_win, bg="#2c3e50")
    btn_frame.pack(pady=20)

    # Твоя кнопка Save Log
    # 1. ФУНКЦІЯ ЗАПИСУ (Має бути з відступом всередині open_system_report)
    def save_log(cpu_name):
        try:
            from datetime import datetime
            cpu_usage = psutil.cpu_percent()
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
                
            log_content = [
                f"=== ARTEMIS SYSTEM LOG [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ===",
                f"DEVICE NAME  : {socket.gethostname()}",
                f"OS VERSION   : {platform.system()} {platform.release()}",
                f"PROCESSOR    : {cpu_name}",
                f"TOTAL RAM    : {round(ram.total / (1024**3), 2)} GB",
                f"LOCAL IP     : {socket.gethostbyname(socket.gethostname())}",
                f"CURRENT USER : {os.getlogin()}",
                "-" * 45,
                f"CPU USAGE    : {cpu_usage}%",
                f"RAM USAGE    : {ram.percent}% ({ram.used // (1024**2)} MB)",
                f"DISK C:      : {disk.percent}% free",
                "==========================================\n"
            ]

            log_path = os.path.join(os.path.dirname(sys.executable), "system_log.txt")

            with open(log_path, "a", encoding="utf-8") as f:
                f.write("\n".join(log_content))

            messagebox.showinfo("Успіх", "Звіт збережено у файл system_log.txt")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося зберегти файл: {e}")

   # 1. Створюємо ОДИН фрейм
    btn_frame = tk.Frame(report_win, bg="#2c3e50")
    btn_frame.pack(pady=20)

    # 2. ОДНА кнопка закриття (зліва)
    tk.Button(btn_frame, text="ЗАКРИТИ", command=report_win.destroy, 
              bg="#e74c3c", fg="white", width=15).pack(side=tk.LEFT, padx=5)
    
    # 3. ОДНА кнопка збереження (справа)
    save_btn = tk.Button(btn_frame, text="SAVE LOG FILE", 
                         command=lambda: save_log(clean_cpu), 
                         bg="#34495e", fg="white", width=15)
    save_btn.pack(side=tk.LEFT, padx=5)

def show_space_weather():
    space_win = tk.Toplevel(root)
    space_win.title("Artemis OS [ Space Weather Station ]")
    center_window(space_win, 500, 750) # Трохи збільшив висоту для нових кнопок
    space_win.configure(bg="#0a0a1a")

    # Центрування вікна
    space_win.update_idletasks()
    x = (space_win.winfo_screenwidth() // 2) - (500 // 2)
    y = (space_win.winfo_screenheight() // 2) - (750 // 2)
    space_win.geometry(f"+{x}+{y}")

    tk.Label(space_win, text="КОСМІЧНА ПОГОДА", font=("Arial", 16, "bold"), bg="#0a0a1a", fg="#00f2ff").pack(pady=10)

    # 1. МАГНІТНІ БУРІ
    kp_frame = tk.Frame(space_win, bg="#0a0a1a")
    kp_frame.pack(fill="x", padx=20)

    def fetch_kp():
        for widget in kp_frame.winfo_children():
            widget.destroy()
        try:
            # Використовуємо основне джерело NOAA
            res = requests.get("https://services.swpc.noaa.gov/products/noaa-scales.json", timeout=5).json()
            kp_val = res['0']['g']['value'] if '0' in res else "0"
            status = "СПОКІЙНО" if int(kp_val) < 2 else "АКТИВНІСТЬ"
            color = "#00ff00" if int(kp_val) < 2 else "#ffcc00"
            tk.Label(kp_frame, text=f"Геомагнітний стан: {status}", font=("Arial", 12), bg="#0a0a1a", fg=color).pack()
            tk.Label(kp_frame, text=f"Поточний G-індекс: {kp_val}/5", font=("Arial", 10), bg="#0a0a1a", fg="white").pack()
        except:
            tk.Label(kp_frame, text="⚠ Супутники офлайн", bg="#0a0a1a", fg="red").pack()

    tk.Button(space_win, text="🔄 ОНОВИТИ СТАН", command=fetch_kp, bg="#1a1a2e", fg="#00f2ff", font=("Arial", 8)).pack(pady=5)

    # 2. ФОТО ДНЯ NASA
    tk.Label(space_win, text="--- Фото дня від NASA ---", bg="#0a0a1a", fg="#555").pack(pady=10)
    img_container = tk.Label(space_win, bg="#0a0a1a")
    img_container.pack(pady=5)
    title_label = tk.Label(space_win, text="Завантаження...", wraplength=400, justify="center", bg="#0a0a1a", fg="#00f2ff")
    title_label.pack()

    # Змінні для збереження (об'явимо їх порожніми спочатку)
    current_img_data = {"url": "", "title": ""}

    def load_nasa():
        try:
            # Використовуємо DEMO_KEY (краще потім замінити на свій)
            nasa_res = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY", timeout=7).json()
            url = nasa_res.get("url")
            title = nasa_res.get("title", "Space_Photo")
            
            # Зберігаємо дані в словник для доступу кнопці збереження
            current_img_data["url"] = url
            current_img_data["title"] = title

            response = requests.get(url, timeout=10)
            img = Image.open(BytesIO(response.content))
            img.thumbnail((440, 300))
            photo = ImageTk.PhotoImage(img)

            img_container.config(image=photo)
            img_container.image = photo 
            title_label.config(text=title)
        except Exception as e:
            title_label.config(text=f"Помилка завантаження фото: {e}", fg="gray")

    # 3. ФУНКЦІЯ ЗБЕРЕЖЕННЯ НА ДИСК
    def save_nasa_photo():
        url = current_img_data["url"]
        title = current_img_data["title"]
        if not url:
            messagebox.showwarning("Увага", "Спочатку завантажте фото!")
            return
            
        try:
            from datetime import datetime
            img_res = requests.get(url, timeout=15)
            # Очищуємо назву для файлу
            clean_title = "".join(x for x in title if x.isalnum() or x in "._- ").strip()
            filename = f"NASA_{datetime.now().strftime('%Y-%m-%d')}_{clean_title[:15]}.jpg"
            
            save_path = os.path.join(os.path.dirname(sys.executable), filename)
            
            with open(save_path, 'wb') as f:
                f.write(img_res.content)
            messagebox.showinfo("NASA", f"Фото успішно збережено!\n{filename}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося зберегти: {e}")

    # ПАНЕЛЬ КНОПОК ВНИЗУ
    btn_frame = tk.Frame(space_win, bg="#0a0a1a")
    btn_frame.pack(side=tk.BOTTOM, pady=20)

    # Кнопка збереження
    tk.Button(btn_frame, text="ЗБЕРЕГТИ ФОТО", command=save_nasa_photo, 
              bg="#27ae60", fg="white", font=("Arial", 10, "bold"), width=15).pack(side=tk.LEFT, padx=5)

    # Кнопка закриття
    tk.Button(btn_frame, text="ЗАКРИТИ ШЛЮЗ", command=space_win.destroy, 
              bg="#1a1a2e", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)

    # Початковий запуск
    fetch_kp()
    load_nasa()

def open_paint():
    paint_win = tk.Toplevel(root)
    paint_win.title("Artemis Paint v1.23.3")
    center_window(paint_win, 900, 700)
    paint_win.configure(bg="#2c3e50")

    # Змінні для малювання
    current_color = tk.StringVar(value="black")
    brush_size = tk.IntVar(value=3)

    # Полотно
    canvas = tk.Canvas(paint_win, bg="white", width=850, height=500, cursor="pencil")
    canvas.pack(pady=10)

    # Для збереження (PIL)
    from PIL import ImageDraw # type: ignore
    output_image = Image.new("RGB", (850, 500), "white")
    draw = ImageDraw.Draw(output_image)

    def paint(event):
        size = brush_size.get()
        color = current_color.get()
        x1, y1 = (event.x - size), (event.y - size)
        x2, y2 = (event.x + size), (event.y + size)
        # Малюємо на екрані
        canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)
        # Малюємо для збереження (лінія робить малювання плавнішим)
        draw.line([x1, y1, x2, y2], fill=color, width=size * 2)

    def save_art():
        file_path = os.path.join(BASE_DIR, "artemis_masterpiece.png")
        output_image.save(file_path)
        messagebox.showinfo("Paint", f"Збережено в:\n{file_path}")

    # Панель інструментів (Frame)
    toolbar = tk.Frame(paint_win, bg="#34495e", bd=2, relief="groove")
    toolbar.pack(fill="x", padx=25, pady=5)

    # 1. Вибір кольору
    colors = [("Black", "black"), ("Red", "#e74c3c"), ("Green", "#2ecc71"), ("Blue", "#3498db"), ("Yellow", "#f1c40f")]
    for text, col in colors:
        tk.Button(toolbar, bg=col, width=3, command=lambda c=col: current_color.set(c)).pack(side=tk.LEFT, padx=5, pady=5)

    # 2. Гумка (просто малює білим)
    tk.Button(toolbar, text="Гумка", bg="#ecf0f1", fg="black", command=lambda: current_color.set("white")).pack(side=tk.LEFT, padx=10)

    # 3. Слайдер товщини
    tk.Label(toolbar, text="Товщина:", bg="#34495e", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Scale(toolbar, from_=1, to_=20, orient=tk.HORIZONTAL, variable=brush_size, bg="#34495e", fg="white", highlightthickness=0).pack(side=tk.LEFT, padx=5)

    # 4. Кнопки керування
    tk.Button(toolbar, text="ОЧИСТИТИ", bg="#95a5a6", command=lambda: [canvas.delete("all"), draw.rectangle([0,0,850,500], fill="white")]).pack(side=tk.LEFT, padx=20)
    tk.Button(toolbar, text="ЗБЕРЕГТИ PNG", bg="#27ae60", fg="white", font=("Arial", 9, "bold"), command=save_art).pack(side=tk.RIGHT, padx=10)

    canvas.bind("<B1-Motion>", paint)

# === ГЕНЕРАЦІЯ КНОПОК ===

def create_btn(parent, text, color, command, col, icon_name):
    frame = tk.Frame(parent, bg="#2c3e50")
    frame.grid(row=1, column=col, padx=8, pady=10)
    
    icon_final = None
    icon_path = os.path.join(BASE_DIR, icon_name)
    
    # Подвійна перевірка шляху (як ми робили вчора)
    if not os.path.exists(icon_path):
        icon_path = os.path.join(os.path.dirname(sys.executable), icon_name)

    if PILLOW_INSTALLED:
        try:
            if os.path.exists(icon_path):
                img = Image.open(icon_path).resize((80, 80), Image.Resampling.LANCZOS)
                icon_final = ImageTk.PhotoImage(img)
        except: pass

    # Створюємо кнопку
    if icon_final:
        b = tk.Button(frame, image=icon_final, command=command, bg="#2c3e50", bd=0, 
                      activebackground="#34495e", cursor="hand2")
        b.image = icon_final
    else:
        b = tk.Button(frame, text=text, command=command, bg=color, fg="white", 
                      width=15, height=2, font=("Arial", 10, "bold"), cursor="hand2")

    # ФУНКЦІЇ ПІДСВІТКИ (Hover Effect)
    def on_enter(e):
        # Змінюємо колір фону кнопки та фрейму на трохи світліший
        if icon_final:
            b.config(bg="#34495e")
        else:
            b.config(bg="#3498db") # Для текстових кнопок — синій акцент

    def on_leave(e):
        # Повертаємо стандартний темно-синій
        if icon_final:
            b.config(bg="#2c3e50")
        else:
            b.config(bg=color)

    # Прив'язуємо події до кнопки
    b.bind("<Enter>", on_enter)
    b.bind("<Leave>", on_leave)
    
    b.pack()
    tk.Label(frame, text=text, bg="#2c3e50", fg="white", font=("Arial", 10)).pack(pady=5)

# === ГОЛОВНЕ ВІКНО ===
root = tk.Tk()
root.title("Artemis Hub v1.23.10")

# 1. Прибираємо верхню смужку Windows і рамки
root.overrideredirect(True)

# 2. Отримуємо розміри твого монітора
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 3. Розгортаємо вікно на весь фізичний екран
root.geometry(f"{screen_width}x{screen_height}+0+0")

# 4. Встановлюємо колір фону
root.config(bg="#2c3e50")

# Кнопка UPDATE
update_btn = tk.Button(root, text="UPDATE OS", command=run_update_process, 
                       bg="#34495e", fg="#00FF00", font=("Arial", 9, "bold"), 
                       relief="flat", width=12) # Задали фіксовану ширину

update_btn.place(relx=1.0, x=-20, y=10, anchor="ne")

# Кнопка ВИХІД
exit_btn = tk.Button(root, text="ВИХІД", command=quit_system, 
                     bg="#34495e", fg="#ff0000", font=("Arial", 9, "bold"), 
                     relief="flat", width=12) # Така сама ширина

exit_btn.place(relx=1.0, x=-20, y=45, anchor="ne")

# Контейнер для часу та дати
info_frame = tk.Frame(root, bg="#2c3e50") # Переконайся, що bg збігається з фоном меню
info_frame.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

# Великий годинник
time_label = tk.Label(info_frame, font=("Arial", 16, "bold"), 
                      fg="white", bg="#2c3e50")
time_label.pack(anchor="e")

# Маленька дата під ним
date_label = tk.Label(info_frame, font=("Arial", 10), 
                      fg="#bdc3c7", bg="#2c3e50")
date_label.pack(anchor="e")

# Запуск циклу оновлення
update_info_panel()

tk.Label(root, text="Мій Центр Керування", font=("Arial", 20, "bold"), bg="#2c3e50", fg="white").grid(row=0, column=0, columnspan=6, pady=20)

create_btn(root, "Годинник", "#27ae60", open_clock, 0, "clock_icon.png")
create_btn(root, "Перекладач", "#2980b9", open_translator, 1, "translator_icon.png")
create_btn(root, "QR-код", "#8e44ad", open_qr, 2, "qr_icon.png")
create_btn(root, "Погода", "#f1c40f", open_weather, 3, "weather_icon.png")
create_btn(root, "Калькулятор", "#e67e22", open_calculator, 4, "calc_icon.png")
create_btn(root, "Звіт", "#34495e", open_system_report, 5, "report_icon.png")
create_btn(root, "Космос", "#1a1a2e", show_space_weather, 6, "cosmos_icon.png")
create_btn(root, "Пейнт", "#1a1a2e", open_paint, 7, "paint_icon.png")

root.mainloop()