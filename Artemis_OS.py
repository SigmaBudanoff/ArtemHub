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

LANG_DATA = {
    "UA": {
        "title": "Мій Центр Керування",
        "module": "Модуль",
        # Назви модулів
        "clock": "Годинник", 
        "translator": "Перекладач", 
        "qr_gen": "QR-Генератор",
        "weather": "Погода", 
        "calc": "Калькулятор", 
        "report": "Звіт системи",
        "space_station": "Космічна станція", 
        "paint": "Графічний редактор",
        
        # Кнопки та загальні команди
        "exit": "ВИХІД", 
        "update": "UPDATE OS",
        "save_log_btn": "ЗБЕРЕГТИ ЛОГ", 
        "save_photo_btn": "ЗБЕРЕГТИ ФОТО",
        "save_png_btn": "ЗБЕРЕГТИ PNG",
        "close": "ЗАКРИТИ", 
        "close_shuttle": "ЗАКРИТИ ШЛЮЗ",
        "clear_btn": "ОЧИСТИТИ", 
        "show_btn": "ПОКАЗАТИ",
        "gen_btn": "ЗГЕНЕРУВАТИ",
        "translate_btn": "ПЕРЕКЛАСТИ",
        "refresh_btn": "ОНОВИТИ",
        
        # Годинник та будильник
        "set_alarm": "ВСТАНОВИТИ БУДИЛЬНИК (HH:MM:SS):",
        "stop_sound": "ВИМКНУТИ ЗВУК",
        
        # Перекладач та QR
        "enter_text": "Введіть текст:",
        "empty_err": "Будь ласка, введіть текст або посилання!",
        
        # Погода
        "city_label": "Місто:",
        "weather_for": "ПРОГНОЗ ДЛЯ",
        "enter_city_err": "Будь ласка, введіть назву міста.",
        "no_internet": "Відсутнє підключення до інтернету.",
        
        # Система (Звіт)
        "sys_info_head": "ІНФОРМАЦІЯ ПРО СИСТЕМУ",
        "metrics_head": "МЕТРИКИ РЕАЛЬНОГО ЧАСУ",
        "cpu_load": "Завантаження CPU",
        "ram_use": "Використання RAM",
        "disk_label": "Диск C:",
        "disk_free": "вільно",
        "log_saved": "Звіт збережено у файл system_log.txt",
        
        # Космос
        "space_header": "КОСМІЧНА ПОГОДА",
        "kp_quiet": "СПОКІЙНО",
        "kp_active": "АКТИВНІСТЬ",
        "mag_status": "Геомагнітний стан",
        "g_index": "Поточний G-індекс",
        "sat_offline": "Супутники офлайн",
        "nasa_photo_day": "Фото дня від NASA",
        "photo_saved": "Фото успішно збережено!",
        
        # Пейнт
        "eraser": "ГУМКА",
        "brush_label": "Товщина:",
        "art_saved": "Шедевр збережено!",
        
        # Калькулятор
        "invalid_expr": "Невірний вираз",
        
        # Повідомлення
        "success": "Успіх",
        "error": "Помилка",
        "warning": "Увага",
        "loading": "Завантаження...",
        "load_err": "Помилка завантаження",
        "unknown_err": "Сталася помилка"
    },
    "EN": {
        "title": "My Control Center",
        "module": "Module",
        "clock": "Clock", 
        "translator": "Translator", 
        "qr_gen": "QR-Generator",
        "weather": "Weather", 
        "calc": "Calculator", 
        "report": "System Report",
        "space_station": "Space Station", 
        "paint": "Graphics Editor",
        
        "exit": "EXIT", 
        "update": "UPDATE OS",
        "save_log_btn": "SAVE LOG FILE", 
        "save_photo_btn": "SAVE PHOTO",
        "save_png_btn": "SAVE AS PNG",
        "close": "CLOSE", 
        "close_shuttle": "CLOSE AIRLOCK",
        "clear_btn": "CLEAR ALL", 
        "show_btn": "SHOW",
        "gen_btn": "GENERATE",
        "translate_btn": "TRANSLATE",
        "refresh_btn": "REFRESH",
        
        "set_alarm": "SET ALARM (HH:MM:SS):",
        "stop_sound": "STOP SOUND",
        
        "enter_text": "Enter text:",
        "empty_err": "Please enter text or a link!",
        
        "city_label": "City:",
        "weather_for": "FORECAST FOR",
        "enter_city_err": "Please enter a city name.",
        "no_internet": "No internet connection.",
        
        "sys_info_head": "SYSTEM INFORMATION",
        "metrics_head": "REAL-TIME METRICS",
        "cpu_load": "CPU Usage",
        "ram_use": "RAM Usage",
        "disk_label": "Drive C:",
        "disk_free": "free",
        "log_saved": "Report saved to system_log.txt",
        
        "space_header": "SPACE WEATHER",
        "kp_quiet": "QUIET",
        "kp_active": "ACTIVE",
        "mag_status": "Geomagnetic status",
        "g_index": "Current G-index",
        "sat_offline": "Satellites offline",
        "nasa_photo_day": "NASA Photo of the Day",
        "photo_saved": "Photo saved successfully!",
        
        "eraser": "ERASER",
        "brush_label": "Brush size:",
        "art_saved": "Masterpiece saved!",
        
        "invalid_expr": "Invalid expression",
        
        "success": "Success",
        "error": "Error",
        "warning": "Warning",
        "loading": "Loading...",
        "load_err": "Loading error",
        "unknown_err": "An error occurred"
    }
}

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
    # Отримуємо час і дату через strftime
    string_time = strftime('%H:%M:%S')
    string_date = strftime('%d.%m.%Y')

    # Оновлюємо текст у віджетах
    time_label.config(text=string_time)
    date_label.config(text=string_date)

    # Повторюємо через 1 секунду
    root.after(1000, update_info_panel)

# 1. ГОЛОВНА ПАПКА ПРОГРАМИ
# Це працює і для .py, і для .exe (якщо знадобиться в майбутньому)
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Додаємо шлях до бібліотек, якщо вони у тебе в папці lib
lib_path = os.path.join(BASE_DIR, "lib", "site-packages")
if os.path.exists(lib_path):
    sys.path.append(lib_path)

# 2. ФУНКЦІЯ ДЛЯ ОТРИМАННЯ РЕСУРСІВ (Іконки, Звуки)
def get_path(category, filename):
    """
    category: "icons" або "sounds"
    filename: назва файлу (напр. "alarm.mp3")
    """
    full_path = os.path.join(BASE_DIR, "assets", category, filename)
    # Перевірка: якщо файлу немає, виводимо в консоль, щоб не "впасти"
    if not os.path.exists(full_path):
        print(f"⚠️ Файл не знайдено: {full_path}")
    return full_path

# 3. ПЕРЕВІРКА PILLOW
try:
    from PIL import Image, ImageTk
    PILLOW_INSTALLED = True
except ImportError:
    PILLOW_INSTALLED = False
    print("⚠️ Бібліотека Pillow не знайдена. Іконки можуть не відображатися.")

# === ФУНКЦІЯ ОНОВЛЕННЯ (UPDATE SYSTEM) ===
def run_update_process():
    url = "https://raw.githubusercontent.com/SigmaBudanoff/ArtemHub/main/Artemis_OS.py"
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        if response.status_code == 200:
            new_code = response.text
            if len(new_code) < 100:
                messagebox.showwarning("Update", "Файл занадто малий.")
                return
            
            with open("Artemis_OS.py", "w", encoding="utf-8") as f:
                f.write(new_code)
            
            messagebox.showinfo("Artemis OS", "Оновлення успішне! Тепер запустіть ваш BAT-файл для оновлення системи.")
            
            # ВИДАЛИ ЦЕЙ РЯДОК: os.startfile("Artemis_OS.py") 
            # Замість нього просто закриваємо вікно:
            root.destroy() 
            
        else:
            messagebox.showerror("Помилка", f"Статус: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Помилка", f"Зв'язок розірвано: {e}")

# === ФУНКЦІЇ МОДУЛІВ ===

def open_clock():
    # 1. Отримуємо мову
    lang = lang_combo.get()
    d = LANG_DATA[lang]

    # 2. Створюємо вікно
    clock_window = tk.Toplevel(root)
    clock_window.title(f"{d['module']}: {d['clock']}")
    
    # Далі твій код для годинника...

    # 3. Налаштовуємо заголовок (перевір, щоб була ОДНА дужка в кінці ключів)
    clock_window.title(f"{d['module']}: {d['clock']}")
    
    # 4. Центруємо та колір
    center_window(clock_window, 450, 400)
    clock_window.config(bg="#2c3e50")
    
    # 5. Створюємо головний напис годинника
    label_clock = tk.Label(clock_window, 
                           font=("Consolas", 60, "bold"), 
                           bg="#2c3e50", 
                           fg="white")
    label_clock.pack(pady=10)
    
    # Далі має йти твій код для дати, будильника тощо...
    
    # Дата: тепер теж на синьому фоні та з білим текстом
    label_date = tk.Label(clock_window, font=("Arial", 12), 
                          bg="#2c3e50", fg="white")
    label_date.pack()

    # Пояснювальний напис для будильника
    tk.Label(clock_window, 
             text=d["set_alarm"], 
             font=("Arial", 8, "bold"), 
             bg="#2c3e50", 
             fg="#bdc3c7").pack(pady=(20, 0))

    # Поле вводу: зробимо його трохи світлішим
    entry_alarm = tk.Entry(clock_window, font=("Arial", 12), width=10, bg="#34495e", fg="white", justify='center')
    entry_alarm.insert(0, "00:00:00")
    entry_alarm.pack(pady=10)

    def update_clock():
        curr = strftime('%H:%M:%S')
        label_clock.config(text=curr)
        label_date.config(text=strftime('%A, %d %B %Y'))
        if curr == entry_alarm.get():
            alarm_path = get_path("sounds", "alarm.wav")
            if os.path.exists(alarm_path):
                winsound.PlaySound(alarm_path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
        label_clock.after(1000, update_clock)

    # Кнопка вимкнення звуку (використовуємо d["stop_sound"])
    tk.Button(clock_window, 
              text=d["stop_sound"], 
              command=lambda: winsound.PlaySound(None, winsound.SND_PURGE), 
              bg="#cc0000", 
              fg="white").pack(pady=10)

    # Виклик функції оновлення часу (обов'язково з нового рядка!)
    update_clock()

def open_translator():
    # 1. Отримуємо поточну мову
    lang = lang_combo.get()
    d = LANG_DATA[lang]

    trans_window = tk.Toplevel(root)
    # 2. Динамічний заголовок
    trans_window.title(f"{d['module']}: {d['translator']}")
    center_window(trans_window, 600, 450) # Трохи збільшив висоту для комфорту
    trans_window.config(bg="#2c3e50")

    # 3. Напис "Введіть текст" (додай ключ "enter_text" у LANG_DATA)
    tk.Label(trans_window, text=d["enter_text"], bg="#2c3e50", fg="white", 
             font=("Arial", 10, "bold")).pack(pady=(20, 5))
    
    in_text = tk.Text(trans_window, height=5, width=40, bg="#34495e", fg="white", 
                      bd=0, padx=10, pady=10)
    in_text.pack(padx=20)
    
    # Вибір мови призначення
    lang_names = list(LANGUAGES.values())
    combo_dest = ttk.Combobox(trans_window, values=lang_names, state="readonly")
    combo_dest.set("ukrainian")
    combo_dest.pack(pady=10)
    
    out_text = tk.Text(trans_window, height=5, width=40, bg="#34495e", fg="#bdc3c7", 
                       bd=0, padx=10, pady=10, state=tk.DISABLED)

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
            except Exception as e: 
                # Помилка теж має бути мовною (ключ "error")
                messagebox.showerror(d["error"], str(e))

    # 4. Кнопка "Перекласти"
    tk.Button(trans_window, text=d["translate_btn"], command=translate, bg="#27ae60", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=20, pady=5).pack(pady=10)

    out_text.pack(padx=20)
    
def open_qr():
    # 1. Отримуємо поточну мову та словник
    lang = lang_combo.get()
    d = LANG_DATA[lang]

    qr_window = tk.Toplevel(root)
    # 2. Використовуємо f-рядок для заголовка
    qr_window.title(f"{d['module']}: {d['qr_gen']}")
    center_window(qr_window, 350, 480) # Трохи збільшив висоту
    qr_window.config(bg="#2c3e50")
    
    # Поле для введення тексту/посилання
    entry_url = tk.Entry(qr_window, width=25, font=("Arial", 12), bg="#34495e", fg="white", insertbackground="white")
    entry_url.pack(pady=20)
    
    label_img = tk.Label(qr_window, bg="#2c3e50")
    label_img.pack()

    def generate():
        content = entry_url.get().strip()
        if content:
            # Генерація QR-коду
            img = qrcode.make(content).resize((200, 200))
            img_tk = ImageTk.PhotoImage(img)
            label_img.config(image=img_tk)
            label_img.image = img_tk
        else:
            # Повідомлення, якщо поле порожнє (ключ "empty_err")
            messagebox.showwarning(d["error"], d["empty_err"])
    
    # 3. Кнопка "Згенерувати" (ключ "gen_btn")
    tk.Button(qr_window, 
              text=d["gen_btn"], 
              command=generate, 
              bg="#8e44ad", 
              fg="white", 
              font=("Arial", 10, "bold"),
              padx=10).pack(pady=10)
    
def open_weather():
    # 1. Отримуємо мову
    lang = lang_combo.get()
    d = LANG_DATA[lang]

    weather_win = tk.Toplevel(root)
    # Динамічний заголовок
    weather_win.title(f"{d['module']}: {d['weather']}")
    center_window(weather_win, 650, 450)
    weather_win.config(bg="#34495e")

    ctrl_frame = tk.Frame(weather_win, bg="#34495e")
    ctrl_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

    # Напис "Місто:" зі словника
    tk.Label(ctrl_frame, text=d["city_label"], bg="#34495e", fg="white", 
             font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)
    
    city_entry = tk.Entry(ctrl_frame, font=("Arial", 12), width=15)
    city_entry.insert(0, "Rivne")
    city_entry.pack(side=tk.LEFT, padx=5)

    res_text = tk.Text(weather_win, font=("Consolas", 11), bg="#2c3e50", 
                       fg="#ecf0f1", bd=0, padx=15, pady=15)
    res_text.pack(side=tk.BOTTOM, pady=10, padx=20, expand=True, fill="both")

    def get_weather():
        city = city_entry.get().strip()
        if not city:
            messagebox.showwarning(d["warning"], d["enter_city_err"])
            return

        try:
            # Запит до API
            response = requests.get(f"https://wttr.in/{city}?format=j1", timeout=5)
        
            if response.status_code != 200:
                messagebox.showerror(d["error"], f"Server code: {response.status_code}")
                return

            data = response.json()
            # Шапка прогнозу зі словника
            output = f"{d['weather_for']}: {city.upper()}\n"
            output += "=" * 45 + "\n"
        
            for day in data['weather'][:7]:
                date = day['date']
                max_t = day['maxtempC']
                min_t = day['mintempC']
                # Беремо опис погоди (він залишиться англійською від сервера)
                desc = day['hourly'][4]['weatherDesc'][0]['value']
                output += f"{date:<12} | {min_t:>3}°C...{max_t:>3}°C | {desc}\n"
        
            res_text.config(state=tk.NORMAL)
            res_text.delete("1.0", tk.END)
            res_text.insert(tk.END, output)
            res_text.config(state=tk.DISABLED)

        except requests.exceptions.ConnectionError:
            messagebox.showerror(d["error"], d["no_internet"])
        except Exception as e:
            messagebox.showerror(d["error"], f"{d['unknown_err']}: {e}")

    # Кнопка "ПОКАЗАТИ"
    tk.Button(ctrl_frame, text=d["show_btn"], command=get_weather, 
              bg="#f1c40f", fg="black", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=10)
    
    # Автоматичний запуск при відкритті
    get_weather()
    
def open_calculator():
    # 1. Отримуємо мову та словник
    lang = lang_combo.get()
    d = LANG_DATA[lang]

    calc_win = tk.Toplevel(root)
    # 2. Динамічний заголовок
    calc_win.title(f"{d['module']}: {d['calc']}")
    center_window(calc_win, 400, 500)
    calc_win.config(bg="#1a1a1a")

    # Поле вводу
    entry = tk.Entry(calc_win, font=("Consolas", 25), justify='right', bg="#1a1a1a", fg="white", bd=0)
    entry.grid(row=0, column=0, columnspan=4, padx=20, pady=20, sticky="we")

    def click(char): 
        entry.insert(tk.END, char)
        
    def clear(): 
        entry.delete(0, tk.END)
        
    def calculate():
        try:
            # Замінюємо візуальні символи на математичні оператори Python
            expression = entry.get().replace('×', '*').replace('÷', '/')
            res = eval(expression)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(res))
        except: 
            # 3. Помилка тепер теж мовна (ключі "error" та "invalid_expr")
            messagebox.showerror(d["error"], d["invalid_expr"])
    
    # Список кнопок (текст, рядок, колонка, колір)
    btns = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('÷', 1, 3, "#e67e22"),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('×', 2, 3, "#e67e22"),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3, "#e67e22"),
        ('C', 4, 0, "#e74c3c"), ('0', 4, 1), ('=', 4, 2, "#27ae60"), ('+', 4, 3, "#e67e22")
    ]
    
    for b in btns:
        text, r, c = b[0], b[1], b[2]
        bg = b[3] if len(b) > 3 else "#333"
        
        # Визначаємо команду для кнопки
        if text == '=':
            cmd = calculate
        elif text == 'C':
            cmd = clear
        else:
            cmd = lambda x=text: click(x)
            
        tk.Button(calc_win, text=text, width=5, height=2, font=("Arial", 12, "bold"),
                  bg=bg, fg="white", relief="flat", command=cmd).grid(row=r, column=c, padx=5, pady=5)
        
def open_system_report():
    lang = lang_combo.get()
    d = LANG_DATA[lang]

    report_win = tk.Toplevel(root)
    # Динамічний заголовок
    report_win.title(f"{d['module']}: {d['report']}")
    center_window(report_win, 480, 650)
    report_win.configure(bg="#2c3e50")

    # --- 1. ОТРИМАННЯ НАЗВИ ПРОЦЕСОРА ---
    try:
        cpu_raw = os.popen("wmic cpu get name").read()
        clean_cpu = cpu_raw.replace("Name", "").strip()
        if not clean_cpu:
            clean_cpu = platform.processor()
    except:
        clean_cpu = platform.processor()

    # --- 2. СТАТИЧНА ІНФОРМАЦІЯ ---
    # Заголовок розділу зі словника
    header = tk.Label(report_win, text=d["sys_info_head"], font=("Arial", 12, "bold"), 
                      bg="#2c3e50", fg="#1abc9c")
    header.pack(pady=(20, 10))

    # Технічні назви зазвичай залишають англійською, але значення динамічні
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
        tk.Label(report_win, text=line, font=("Consolas", 9), bg="#2c3e50", 
                 fg="#bdc3c7", anchor="w", justify="left").pack(fill="x", padx=40)

    tk.Label(report_win, text="-" * 45, bg="#2c3e50", fg="#34495e").pack()

    # --- 3. МЕТРИКИ РЕАЛЬНОГО ЧАСУ ---
    tk.Label(report_win, text=d["metrics_head"], font=("Arial", 10, "bold"), 
             bg="#2c3e50", fg="#f1c40f").pack(pady=5)

    cpu_label = tk.Label(report_win, text="...", font=("Arial", 11), bg="#2c3e50", fg="white")
    cpu_label.pack(pady=5)

    ram_label = tk.Label(report_win, text="...", font=("Arial", 11), bg="#2c3e50", fg="white")
    ram_label.pack(pady=5)
    
    storage_label = tk.Label(report_win, text="...", font=("Arial", 11), bg="#2c3e50", fg="white")
    storage_label.pack(pady=5)

    def update_stats():
        if not report_win.winfo_exists():
            return

        cpu_usage = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        # Використовуємо d["cpu_load"], d["ram_use"], d["disk_free"]
        cpu_label.config(text=f"{d['cpu_load']}: {cpu_usage}%")
        ram_label.config(text=f"{d['ram_use']}: {ram.percent}% ({ram.used // (1024**2)} MB)")
        storage_label.config(text=f"{d['disk_label']}: {disk.percent}% {d['disk_free']}")

        cpu_label.config(fg="#e74c3c" if cpu_usage > 80 else "white")
        ram_label.config(fg="#e74c3c" if ram.percent > 90 else "white")

        report_win.after(2000, update_stats)

    update_stats()

    # --- 4. ФУНКЦІЯ ЗБЕРЕЖЕННЯ ---
    def save_log(cpu_name):
        try:
            from datetime import datetime
            log_content = [
                f"=== SYSTEM LOG [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ===",
                f"CPU: {cpu_name}",
                f"RAM: {psutil.virtual_memory().percent}%",
                f"DISK: {psutil.disk_usage('/').percent}%",
                "==========================================\n"
            ]
            # Зберігаємо поруч із програмою
            with open("system_log.txt", "a", encoding="utf-8") as f:
                f.write("\n".join(log_content))
            messagebox.showinfo(d["success"], d["log_saved"])
        except Exception as e:
            messagebox.showerror(d["error"], f"Error: {e}")

    # --- 5. КНОПКИ ---
    btn_frame = tk.Frame(report_win, bg="#2c3e50")
    btn_frame.pack(pady=20)

    # Кнопка закриття
    tk.Button(btn_frame, text=d["close"], command=report_win.destroy, 
              bg="#e74c3c", fg="white", width=15).pack(side=tk.LEFT, padx=5)
    
    # Кнопка збереження (текст кнопки теж зі словника)
    tk.Button(btn_frame, text=d["save_log_btn"], 
              command=lambda: save_log(clean_cpu), 
              bg="#34495e", fg="white", width=15).pack(side=tk.LEFT, padx=5)

# ПЕРЕКОНАЙСЯ, ЩО ПІСЛЯ ЦІЄЇ ФУНКЦІЇ ЙДЕ ПОРОЖНІЙ РЯДОК
def show_space_weather():
    lang = lang_combo.get()
    d = LANG_DATA[lang]

    space_win = tk.Toplevel(root)
    # Динамічний заголовок
    space_win.title(f"{d['module']}: {d['space_station']}")
    center_window(space_win, 500, 750)
    space_win.configure(bg="#0a0a1a")

    tk.Label(space_win, text=d["space_header"], font=("Arial", 16, "bold"), 
             bg="#0a0a1a", fg="#00f2ff").pack(pady=10)

    # 1. МАГНІТНІ БУРІ
    kp_frame = tk.Frame(space_win, bg="#0a0a1a")
    kp_frame.pack(fill="x", padx=20)

    def fetch_kp():
        for widget in kp_frame.winfo_children():
            widget.destroy()
        try:
            res = requests.get("https://services.swpc.noaa.gov/products/noaa-scales.json", timeout=5).json()
            kp_val = int(res['0']['g']['value']) if '0' in res else 0
            
            # Визначаємо статус за словником
            if kp_val < 2:
                status = d["kp_quiet"]
                color = "#00ff00"
            else:
                status = d["kp_active"]
                color = "#ffcc00"
                
            tk.Label(kp_frame, text=f"{d['mag_status']}: {status}", font=("Arial", 12), bg="#0a0a1a", fg=color).pack()
            tk.Label(kp_frame, text=f"{d['g_index']}: {kp_val}/5", font=("Arial", 10), bg="#0a0a1a", fg="white").pack()
        except:
            tk.Label(kp_frame, text=f"⚠ {d['sat_offline']}", bg="#0a0a1a", fg="red").pack()

    # Кнопка оновлення
    tk.Button(space_win, text=d["refresh_btn"], command=fetch_kp, bg="#1a1a2e", 
              fg="#00f2ff", font=("Arial", 8)).pack(pady=5)

    # 2. ФОТО ДНЯ NASA
    tk.Label(space_win, text=f"--- {d['nasa_photo_day']} ---", bg="#0a0a1a", fg="#555").pack(pady=10)
    img_container = tk.Label(space_win, bg="#0a0a1a")
    img_container.pack(pady=5)
    title_label = tk.Label(space_win, text=d["loading"], wraplength=400, justify="center", bg="#0a0a1a", fg="#00f2ff")
    title_label.pack()

    current_img_data = {"url": "", "title": ""}

    def load_nasa():
        try:
            nasa_res = requests.get("https://api.nasa.gov/planetary/apod?api_key=ojjKnJA3h9wuCvta3dt2PDfEOuPtwXBWDG7qv35j", timeout=7).json()
            media_type = nasa_res.get("media_type")
            url = nasa_res.get("url")
            title = nasa_res.get("title", "Space_Photo")
            
            current_img_data["url"] = url
            current_img_data["title"] = title

            if media_type == "image":
                response = requests.get(url, timeout=10)
                img = Image.open(BytesIO(response.content))
                img.thumbnail((440, 300))
                photo = ImageTk.PhotoImage(img)
                img_container.config(image=photo)
                img_container.image = photo 
                title_label.config(text=title)
            else:
                # Якщо сьогодні відео замість фото
                title_label.config(text=f"Today is a Video: {title}\n(Check NASA APOD website)")
        except Exception as e:
            title_label.config(text=f"{d['load_err']}: {e}", fg="gray")

    # 3. ФУНКЦІЯ ЗБЕРЕЖЕННЯ
    def save_nasa_photo():
        url = current_img_data["url"]
        if not url:
            messagebox.showwarning(d["warning"], d["load_first_err"])
            return
            
        try:
            from datetime import datetime
            img_res = requests.get(url, timeout=15)
            clean_title = "".join(x for x in current_img_data["title"] if x.isalnum() or x in "._- ").strip()
            filename = f"NASA_{datetime.now().strftime('%Y-%m-%d')}_{clean_title[:15]}.jpg"
            
            with open(filename, 'wb') as f:
                f.write(img_res.content)
            messagebox.showinfo(d["success"], f"{d['photo_saved']}\n{filename}")
        except Exception as e:
            messagebox.showerror(d["error"], f"{d['save_err']}: {e}")

    # ПАНЕЛЬ КНОПОК
    btn_frame = tk.Frame(space_win, bg="#0a0a1a")
    btn_frame.pack(side=tk.BOTTOM, pady=20)

    # Кнопка збереження
    tk.Button(btn_frame, text=d["save_photo_btn"], command=save_nasa_photo, 
              bg="#27ae60", fg="white", font=("Arial", 10, "bold"), width=15).pack(side=tk.LEFT, padx=5)

    # Кнопка закриття (використовуємо існуючий d["close"] або новий d["close_shuttle"])
    tk.Button(btn_frame, text=d["close_shuttle"], command=space_win.destroy, 
              bg="#1a1a2e", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)

    fetch_kp()
    load_nasa()

def open_paint():
    lang = lang_combo.get()
    d = LANG_DATA[lang]

    paint_win = tk.Toplevel(root)
    # Динамічний заголовок
    paint_win.title(f"{d['module']}: {d['paint']}")
    center_window(paint_win, 900, 750)
    paint_win.configure(bg="#2c3e50")

    # Змінні для малювання
    current_color = tk.StringVar(value="black")
    brush_size = tk.IntVar(value=3)
    last_x, last_y = None, None # Для плавності ліній

    # Полотно
    canvas = tk.Canvas(paint_win, bg="white", width=850, height=500, cursor="pencil")
    canvas.pack(pady=10)

    # Об'єкт для збереження картинки
    from PIL import ImageDraw
    output_image = Image.new("RGB", (850, 500), "white")
    draw = ImageDraw.Draw(output_image)

    def paint(event):
        nonlocal last_x, last_y
        size = brush_size.get()
        color = current_color.get()
        
        if last_x and last_y:
            # Малюємо лінію на екрані
            canvas.create_line(last_x, last_y, event.x, event.y, 
                               fill=color, width=size*2, capstyle=tk.ROUND, smooth=True)
            # Малюємо лінію для файлу
            draw.line([last_x, last_y, event.x, event.y], fill=color, width=size*2)
            
        last_x, last_y = event.x, event.y

    def reset_coords(event):
        nonlocal last_x, last_y
        last_x, last_y = None, None

    def save_art():
        try:
            file_name = "artemis_masterpiece.png"
            output_image.save(file_name)
            messagebox.showinfo(d["success"], f"{d['art_saved']}\n{file_name}")
        except Exception as e:
            messagebox.showerror(d["error"], str(e))

    # Панель інструментів
    toolbar = tk.Frame(paint_win, bg="#34495e", bd=2, relief="groove")
    toolbar.pack(fill="x", padx=25, pady=5)

    # 1. Кнопки кольорів
    colors = ["black", "#e74c3c", "#2ecc71", "#3498db", "#f1c40f"]
    for col in colors:
        tk.Button(toolbar, bg=col, width=3, relief="flat",
                  command=lambda c=col: current_color.set(c)).pack(side=tk.LEFT, padx=5, pady=5)

    # 2. Гумка (d["eraser"])
    tk.Button(toolbar, text=d["eraser"], bg="#ecf0f1", fg="black", 
              command=lambda: current_color.set("white")).pack(side=tk.LEFT, padx=10)

    # 3. Слайдер товщини (d["brush_label"])
    tk.Label(toolbar, text=d["brush_label"], bg="#34495e", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Scale(toolbar, from_=1, to_=20, orient=tk.HORIZONTAL, variable=brush_size, 
             bg="#34495e", fg="white", highlightthickness=0).pack(side=tk.LEFT, padx=5)

    # 4. Керівні кнопки (d["clear_btn"], d["save_png_btn"])
    tk.Button(toolbar, text=d["clear_btn"], bg="#95a5a6", 
              command=lambda: [canvas.delete("all"), draw.rectangle([0,0,850,500], fill="white")]).pack(side=tk.LEFT, padx=20)
    
    tk.Button(toolbar, text=d["save_png_btn"], bg="#27ae60", fg="white", 
              font=("Arial", 9, "bold"), command=save_art).pack(side=tk.RIGHT, padx=10)

    # Прив'язка подій миші
    canvas.bind("<B1-Motion>", paint)
    canvas.bind("<ButtonRelease-1>", reset_coords)
    
# === ГЕНЕРАЦІЯ КНОПОК ===
def create_btn(parent, text, color, command, col, icon_name):
    frame = tk.Frame(parent, bg="#2c3e50")
    # Додав padx=15, щоб кнопки не злипалися в одну кучу
    frame.grid(row=0, column=col, padx=15, pady=10) 
    
    icon_final = None
    # Вказуємо шлях саме до папки assets
    icon_path = os.path.join("assets", "icons", icon_name)
    
    if PILLOW_INSTALLED:
        try:
            if os.path.exists(icon_path):
                img = Image.open(icon_path).resize((80, 80), Image.Resampling.LANCZOS)
                icon_final = ImageTk.PhotoImage(img)
            else:
                print(f"⚠️ Файл не знайдено: {icon_path}")
        except Exception as e: 
            print(f"❌ Помилка іконки {icon_name}: {e}")

    # Створюємо кнопку
    if icon_final:
        # Якщо іконка є — створюємо прозору кнопку з картинкою
        b = tk.Button(frame, image=icon_final, command=command, bg="#2c3e50", bd=0, 
                      activebackground="#34495e", cursor="hand2")
        b.image = icon_final
    else:
        # Якщо іконки немає — малюємо кольорову кнопку (як зараз)
        b = tk.Button(frame, text=text[:2], command=command, bg=color, fg="white", 
                      width=4, height=2, font=("Arial", 12, "bold"), cursor="hand2")

    b.bind("<Enter>", lambda e: b.config(bg="#34495e" if icon_final else "#3498db"))
    b.bind("<Leave>", lambda e: b.config(bg="#2c3e50" if icon_final else color))
    
    b.pack()
    
    # Текстовий підпис під іконкою (завжди білий)
    lbl = tk.Label(frame, text=text, bg="#2c3e50", fg="white", font=("Arial", 10, "bold"))
    lbl.pack(pady=5)
    
    return b, lbl

# === ЗМІНА МОВИ ===
def change_language(event=None):
    global lang_combo, main_title_label, exit_btn, update_btn
    global btn_clock, btn_trans, btn_qr, btn_weather, btn_calc, btn_report, btn_space, btn_paint
    
    lang = lang_combo.get()
    d = LANG_DATA[lang]
    
    # Оновлюємо заголовок та системні кнопки
    main_title_label.config(text=d["title"])
    exit_btn.config(text=d["exit"])
    update_btn.config(text=d["update"])
   
    # Оновлюємо підписи кнопок (використовуємо індекс [1], бо це Label)
    btn_clock[1].config(text=d["clock"])
    btn_trans[1].config(text=d["translator"])
    btn_qr[1].config(text=d["qr_gen"])
    btn_weather[1].config(text=d["weather"])
    btn_calc[1].config(text=d["calc"])
    btn_report[1].config(text=d["report"])
    btn_space[1].config(text=d["space_station"])
    btn_paint[1].config(text=d["paint"])

# === ГОЛОВНЕ ВІКНО ===
root = tk.Tk()
root.title("Artemis Hub v1.24 ")
root.overrideredirect(True) 

sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{sw}x{sh}+0+0")
root.config(bg="#2c3e50")

# Кнопки вгорі (UPDATE та EXIT)
update_btn = tk.Button(root, text="UPDATE OS", command=run_update_process, 
                       bg="#34495e", fg="#00FF00", font=("Arial", 9, "bold"), relief="flat", width=12)
update_btn.place(relx=1.0, x=-20, y=10, anchor="ne")

exit_btn = tk.Button(root, text="ВИХІД", command=root.quit,

bg="#34495e", fg="#ff0000", font=("Arial", 9, "bold"), relief="flat", width=12)

exit_btn.place(relx=1.0, x=-20, y=45, anchor="ne")

# Нижня панель (Версія та Мова)
version_label = tk.Label(root, text="V. 1.24.2.3 ", font=("Arial", 10, "bold"), fg="#5d6d7e", bg="#2c3e50")
version_label.place(relx=0.0, rely=1.0, x=20, y=-20, anchor="sw")

lang_combo = ttk.Combobox(root, values=["UA", "EN"], state="readonly", width=5)
lang_combo.current(0)
lang_combo.place(relx=0.0, rely=1.0, x=20, y=-55, anchor="sw")
lang_combo.bind("<<ComboboxSelected>>", change_language)

# Заголовок (трохи вище центру)
main_title_label = tk.Label(root, text="Мій Центр Керування", font=("Arial", 28, "bold"), bg="#2c3e50", fg="white")
main_title_label.place(relx=0.5, rely=0.25, anchor="center")

# Контейнер для кнопок (піднімаємо на рівень 45% висоти екрану)
btn_container = tk.Frame(root, bg="#2c3e50")
btn_container.place(relx=0.5, rely=0.45, anchor="center")

# Створення кнопок (тепер вони шукатимуть файли в assets/)
btn_clock  = create_btn(btn_container, "Годинник", "#27ae60", open_clock, 0, "clock_icon.png")
btn_trans  = create_btn(btn_container, "Перекладач", "#2980b9", open_translator, 1, "translator_icon.png")
btn_qr     = create_btn(btn_container, "QR-код", "#8e44ad", open_qr, 2, "qr_icon.png")
btn_weather = create_btn(btn_container, "Погода", "#f1c40f", open_weather, 3, "weather_icon.png")
btn_calc   = create_btn(btn_container, "Калькулятор", "#e67e22", open_calculator, 4, "calc_icon.png")
btn_report = create_btn(btn_container, "Звіт", "#34495e", open_system_report, 5, "report_icon.png")
btn_space  = create_btn(btn_container, "Космос", "#1a1a2e", show_space_weather, 6, "cosmos_icon.png")
btn_paint  = create_btn(btn_container, "Пейнт", "#c0392b", open_paint, 7, "paint_icon.png")

root.mainloop()
