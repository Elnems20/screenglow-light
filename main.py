import tkinter as tk
from pynput import keyboard
import threading

# إعداد النافذة الرئيسية
root = tk.Tk()
root.overrideredirect(True)      # إزالة إطار النافذة العادي
root.attributes('-topmost', True) # جعل النافذة فوق جميع البرامج
root.attributes('-alpha', 0.9)    # درجة الشفافية

# حساب أبعاد الشاشة
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
bar_h = 14  # سمك شريط الإضاءة بالبكسل

# تحديد موضع الشريط أسفل الشاشة بالكامل
root.geometry(f"{screen_w}x{bar_h}+0+{screen_h - bar_h}")
root.configure(bg='white') # لون الإضاءة (أبيض)

# إخفاء الشريط عند بدء التشغيل
root.withdraw()

timer = None
TIMEOUT = 5.0 # مدة ظهور الإضاءة بالثواني (يمكنك تغييرها لاحقاً)

def hide_bar():
    root.withdraw()

def show_bar():
    global timer
    root.deiconify()
    if timer and timer.is_alive():
        timer.cancel()
    timer = threading.Timer(TIMEOUT, hide_bar)
    timer.start()

def on_press(key):
    root.after(0, show_bar)

# بدء الاستماع لضغطات لوحة المفاتيح
listener = keyboard.Listener(on_press=on_press)
listener.start()

root.mainloop()
