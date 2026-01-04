import tkinter as tk
from tkinter import messagebox
import winsound
from datetime import datetime # Потрібно для реального часу

class MiniTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer")
        
        # --- 1. Налаштування вікна ---
        # Трохи збільшив ширину (140), щоб вмістити два часи
        self.root.geometry("140x60")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        
        self.time_left = 0
        self.running = False
        self.timer_id = None 
        
        # --- 2. Верхня панель (Два часи) ---
        top_frame = tk.Frame(root)
        top_frame.pack(side="top", fill="both", expand=True)

        # ЛІВА ЧАСТИНА: Введення / Таймер (Білий колір)
        self.time_var = tk.StringVar()
        self.entry = tk.Entry(top_frame, textvariable=self.time_var, 
                              justify='center', font=("Arial", 12), width=5)
        self.entry.pack(side="left", fill="both", expand=True)
        self.entry.focus_set()

        # ПРАВА ЧАСТИНА: Реальний годинник (Сірий колір - #e0e0e0)
        self.lbl_clock = tk.Label(top_frame, text="00:00", 
                                  bg="#e0e0e0", fg="#333333",
                                  font=("Arial", 10, "bold"))
        self.lbl_clock.pack(side="right", fill="both", expand=True)

        # --- 3. Нижня панель (Кнопки) ---
        btn_frame = tk.Frame(root)
        btn_frame.pack(side="bottom", fill="x") # Висота кнопок фіксована

        # Кнопка Set / Reset
        self.btn_set = tk.Button(btn_frame, text="Set", command=self.toggle_set_reset, font=("Arial", 8), height=1)
        self.btn_set.pack(side="left", fill="both", expand=True)

        # Кнопка Start
        self.btn_start = tk.Button(btn_frame, text="Go", command=self.start_timer, bg="#90ee90", font=("Arial", 8), height=1)
        self.btn_start.pack(side="right", fill="both", expand=True)

        # Запуск оновлення годинника
        self.update_real_time()

    def update_real_time(self):
        """Оновлює правий годинник щосекунди"""
        now = datetime.now().strftime("%H:%M")
        self.lbl_clock.config(text=now)
        # Плануємо наступне оновлення через 1000 мс (1 сек)
        self.root.after(1000, self.update_real_time)

    def toggle_set_reset(self):
        """Логіка фіксації часу"""
        if self.btn_set['text'] == "Set":
            try:
                val = self.time_var.get()
                if not val: return
                
                minutes = float(val)
                self.time_left = int(minutes * 60)
                
                mins, secs = divmod(self.time_left, 60)
                self.time_var.set(f"{mins:02d}:{secs:02d}")
                
                self.entry.config(state='disabled')
                self.btn_set.config(text="Reset", bg="#ffcccb")
            except ValueError:
                messagebox.showerror("Помилка", "Введіть число (хвилини)")
                self.time_var.set("")
                self.entry.focus_set()
        else:
            self.reset_timer()

    def reset_timer(self):
        """Скидання"""
        self.running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            
        self.entry.config(state='normal')
        self.time_var.set("")
        self.btn_set.config(text="Set", bg="SystemButtonFace")
        self.entry.focus_set()

    def start_timer(self):
        """Старт"""
        if self.btn_set['text'] == "Set":
            self.toggle_set_reset()
            
        if not self.running and self.time_left > 0:
            self.running = True
            self.count_down()

    def count_down(self):
        """Відлік"""
        if self.running and self.time_left > 0:
            self.time_left -= 1
            mins, secs = divmod(self.time_left, 60)
            
            self.entry.config(state='normal')
            self.time_var.set(f"{mins:02d}:{secs:02d}")
            self.entry.config(state='disabled')
            
            self.timer_id = self.root.after(1000, self.count_down)
        
        elif self.running and self.time_left == 0:
            self.running = False
            self.entry.config(state='normal')
            self.time_var.set("00:00")
            self.play_sound()
            # Вікно повідомлення тепер не блокує роботу годинника, але зупиняє скрипт
            messagebox.showinfo("Таймер", "Час вийшов!")
            self.reset_timer()

    def play_sound(self):
        try:
            winsound.Beep(1000, 1000)
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniTimer(root)
    root.mainloop()