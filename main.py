import tkinter as tk
from pynput import keyboard
import threading

# ================================
# ⚙️ الإعدادات الافتراضية للبرنامج
# ================================
BAR_HEIGHT = 20       # سمك/ارتفاع الشريط الأبيض بالبكسل (يمكنك تكبيره أو تصغيره)
SHOW_TIMEOUT = 5.0    # عدد الثواني التي يظل الشريط فيها ظاهراً بعد التوقف عن الكتابة
BAR_COLOR = "white"   # لون الشريط الإضاءة

# إنشاء النافذة الرئيسية
root = tk.Tk()
root.overrideredirect(True)      # إزالة إطار النافذة العادي
root.attributes('-topmost', True) # جعل النافذة فوق جميع البرامج
root.attributes('-alpha', 0.95)   # درجة شفافية وقوة الإضاءة

# حساب أبعاد الشاشة لتطبيق الشريط أسفل الشاشة تماماً
def update_bar_geometry():
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    root.geometry(f"{screen_w}x{BAR_HEIGHT}+0+{screen_h - BAR_HEIGHT}")

update_bar_geometry()
root.configure(bg=BAR_COLOR)

# إخفاء الشريط عند التقديم المبدئي
root.withdraw()

timer = None

def hide_bar():
    root.withdraw()

def show_bar():
    global timer
    root.deiconify()
    if timer and timer.is_alive():
        timer.cancel()
    timer = threading.Timer(SHOW_TIMEOUT, hide_bar)
    timer.start()

def on_press(key):
    root.after(0, show_bar)

# ================================
# 🛠️ نافذة الإعدادات لتغيير المساحة والثواني مباشرة
# ================================
def open_settings():
    settings_win = tk.Toplevel(root)
    settings_win.title("إعدادات إضاءة الشاشة")
    settings_win.geometry("320x220")
    settings_win.attributes('-topmost', True)

    tk.Label(settings_win, text="إعدادات شريط الإضاءة", font=("Arial", 12, "bold")).pack(pady=10)

    # التحكم في ارتفاع/مساحة الشريط
    tk.Label(settings_win, text="ارتفاع/سمك الشريط (بالبكسل):").pack()
    height_slider = tk.Scale(settings_win, from_=5, to=100, orient="horizontal")
    height_slider.set(BAR_HEIGHT)
    height_slider.pack(fill="x", px=20)

    # التحكم في مدة الإضاءة بالثواني
    tk.Label(settings_win, text="مدة ظهور الإضاءة (بالثواني):").pack()
    time_slider = tk.Scale(settings_win, from_=1, to=30, orient="horizontal")
    time_slider.set(int(SHOW_TIMEOUT))
    time_slider.pack(fill="x", px=20)

    def save_settings():
        global BAR_HEIGHT, SHOW_TIMEOUT
        BAR_HEIGHT = height_slider.get()
        SHOW_TIMEOUT = float(time_slider.get())
        update_bar_geometry()
        settings_win.destroy()
        show_bar()

    tk.Button(settings_win, text="حفظ الإعدادات", command=save_settings, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

# الاستماع للاختصار (Ctrl + Shift + S) لفتح نافذة الإعدادات
current_keys = set()
def on_key_press(key):
    current_keys.add(key)
    show_bar()
    
    # فتح الإعدادات عند الضغط على Ctrl + Shift + S
    if {keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.KeyCode.from_char('s')}.issubset(current_keys) or \
       {keyboard.Key.ctrl_r, keyboard.Key.shift, keyboard.KeyCode.from_char('s')}.issubset(current_keys):
        root.after(0, open_settings)

def on_key_release(key):
    if key in current_keys:
        current_keys.remove(key)

listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
listener.start()

root.mainloop()
