import tkinter as tk
from pynput import keyboard
import threading

# إنشاء نافذة البرنامج
root = tk.Tk()
root.overrideredirect(True)      # إزالة إطار النافذة العادي
root.attributes('-topmost', True) # جعل الشريط فوق جميع البرامج
root.attributes('-alpha', 0.85)   # درجة الشفافية (يمكنك تقليلها أو زيادتها من 0.1 إلى 1.0)

# حساب أبعاد الشاشة لجعل الارتفاع "ربع الشاشة"
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

BAR_HEIGHT = int(screen_h / 4)  # ربع ارتفاع الشاشة تماماً
SHOW_TIMEOUT = 1.0             # 1 ثواني وتختفي الإضاءة

# تحديد مقاسات ومكان الشريط في أسفل الشاشة
root.geometry(f"{screen_w}x{BAR_HEIGHT}+0+{screen_h - BAR_HEIGHT}")
root.configure(bg='white') # لون الإضاءة أبيض

# إخفاء الشريط في البداية
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

# الاستماع لضغطات لوحة المفاتيح
listener = keyboard.Listener(on_press=on_press)
listener.start()

root.mainloop()
