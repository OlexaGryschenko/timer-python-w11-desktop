import tkinter as tk
from tkinter import messagebox
import winsound  # Працює на Windows. Для Mac/Linux див. примітку нижче

class MiniTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer")
        
        # --- 1. Налаштування вікна ---
        # Розмір 100 ширина x 60 висота
        self.root.geometry("150x70")
        # Заборона зміни розміру
        self.root.resizable(False, False)
        # Завжди поверх інших вікон (щоб було видно на робочому столі)
        self.root.attributes('-topmost', True)
        
        self.time_left = 0
        self.running = False
        
        # --- 2. Форма для введення / Відображення часу ---
        # Використовуємо Entry, щоб можна було і вводити, і бачити час
        self.time_var = tk.StringVar()
        self.entry = tk.Entry(root, textvariable=self.time_var, justify='center', font=("Arial", 20))
        self.entry.pack(side="top", fill="x")
        self.entry.insert(0, "0") # Початкове значення
        
        # Фрейм для кнопок, щоб розмістити їх в ряд
        btn_frame = tk.Frame(root)
        btn_frame.pack(side="bottom", fill="both", expand=True)

        # --- 3. Кнопка "Встановити" (Set) ---
        self.btn_set = tk.Button(btn_frame, text="Set", command=self.set_time, font=("Arial", 8))
        self.btn_set.pack(side="left", fill="both", expand=True)

        # --- 4. Кнопка "Пуск" (Start) ---
        self.btn_start = tk.Button(btn_frame, text="Go", command=self.start_timer, bg="#90ee90", font=("Arial", 8))
        self.btn_start.pack(side="right", fill="both", expand=True)

    def set_time(self):
        """Зчитує хвилини та конвертує для відображення, зупиняє таймер"""
        try:
            self.running = False
            # Отримуємо значення з поля (хвилини)
            minutes = float(self.time_var.get())
            self.time_left = int(minutes * 60) # Конвертуємо в секунди
            
            # Форматуємо відображення MM:SS
            mins, secs = divmod(self.time_left, 60)
            self.time_var.set(f"{mins:02d}:{secs:02d}")
            
            # Робимо поле сірим, щоб показати, що час зафіксовано
            self.entry.config(state='disabled') 
        except ValueError:
            messagebox.showerror("Помилка", "Введіть число (хвилини)")

    def start_timer(self):
        """Запускає відлік"""
        if not self.running and self.time_left > 0:
            self.running = True
            self.count_down()
        elif self.time_left == 0:
             # Якщо користувач натиснув Пуск, не натиснувши Set, спробуємо встановити час автоматично
             self.set_time()
             if self.time_left > 0:
                 self.running = True
                 self.count_down()

    def count_down(self):
        """Логіка відліку"""
        if self.running and self.time_left > 0:
            mins, secs = divmod(self.time_left, 60)
            # Оновлюємо те саме поле введення
            # Треба розблокувати, щоб змінити текст, і заблокувати знову
            self.entry.config(state='normal')
            self.time_var.set(f"{mins:02d}:{secs:02d}")
            self.entry.config(state='disabled')
            
            self.time_left -= 1
            # Викликаємо цю ж функцію через 1000 мс (1 секунда)
            self.root.after(1000, self.count_down)
        
        elif self.running and self.time_left == 0:
            # --- 5. Закінчення і Звук ---
            self.running = False
            self.entry.config(state='normal')
            self.time_var.set("00:00")
            self.play_sound()
            messagebox.showinfo("Таймер", "Час вийшов!")

    def play_sound(self):
        # Частота 1000 Гц, тривалість 1000 мс (1 сек)
        # Тільки для Windows
        try:
            winsound.Beep(1000, 1000)
        except:
            pass # Ігнорувати помилку на Linux/Mac

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniTimer(root)
    root.mainloop()