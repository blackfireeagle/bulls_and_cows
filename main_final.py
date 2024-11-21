import tkinter as tk
from tkinter import messagebox
import random

# Основной класс игры "Быки и коровы"
class BullsAndCowsGame:
    def __init__(self, root):
        # Инициализация главного окна и базовых переменных
        self.root = root
        self.root.title("Игра: Быки и Коровы")

        self.secret_number = ""  # Загаданное число
        self.attempts = []  # История попыток

        self.create_widgets()  # Создание интерфейса

    def create_widgets(self):
        # Интерфейс для ввода длины числа
        tk.Label(self.root, text="Введите количество символов:").pack(pady=5)
        self.length_entry = tk.Entry(self.root, width=4)
        self.length_entry.pack(pady=5)

        # Выбор системы счисления: десятичная или шестнадцатеричная
        tk.Label(self.root, text="Выберите систему счисления:").pack(pady=5)
        self.base_var = tk.StringVar(value="10")
        tk.Radiobutton(self.root, text="Десятичная (2-10)", variable=self.base_var, value="10").pack(pady=5)
        tk.Radiobutton(self.root, text="Шестнадцатеричная (2-16)", variable=self.base_var, value="16").pack(pady=5)

        # Кнопка для запуска игры
        tk.Button(self.root, text="Начать игру", command=self.start_game).pack(pady=10)

        # Поле для ввода попыток
        self.attempt_entry = tk.Entry(self.root, width=10)
        self.attempt_entry.pack(pady=5)
        self.attempt_entry.bind('<Return>', self.play)  # Вызов метода play при нажатии Enter

        # Отображение предыдущих попыток
        tk.Label(self.root, text="Предыдущие попытки:").pack(pady=5)
        self.attempts_display = tk.Text(self.root, height=10, width=40, state='disabled')
        self.attempts_display.pack(pady=5)

        # Поле для сообщений о результате
        self.result_msg = tk.Message(width=400, padx=10, pady=5, text='')
        self.result_msg.pack(pady=5)

        # Установка фокуса на поле ввода попыток
        self.attempt_entry.focus()

    def start_game(self):
        # Логика запуска новой игры
        try:
            length = int(self.length_entry.get())  # Получение длины числа
            if self.base_var.get() == "10":
                # Проверка диапазона для десятичной системы
                if not (2 <= length <= 10):
                    raise ValueError
                self.secret_number = ''.join(random.choices('0123456789', k=length))  # Генерация числа
            else:
                # Проверка диапазона для шестнадцатеричной системы
                if not (2 <= length <= 16):
                    raise ValueError
                self.secret_number = ''.join(random.choices('0123456789abcdef', k=length))

            # Сброс истории попыток и обновление интерфейса
            self.attempts = []
            self.attempts_display.config(state='normal')
            self.attempts_display.delete('1.0', tk.END)
            self.attempts_display.config(state='disabled')
            self.result_msg.config(text='Сыграем! Введите вашу попытку:')
            self.length_entry.config(state='disabled')
            self.base_var.set("10" if self.base_var.get() == "10" else "16")

        except ValueError:
            # Обработка ошибки ввода длины числа
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректное количество символов!")

    def play(self, event):
        # Логика обработки попыток пользователя
        attempt = self.attempt_entry.get().lower()  # Приведение попытки к нижнему регистру
        if attempt == "я сдаюсь":
            # Если пользователь сдается, показать загаданное число
            messagebox.showinfo("Сдача", f"Вы сдались. Загаданное число: {self.secret_number}")
            self.root.quit()  # Завершение игры
            return

        if len(attempt) != len(self.secret_number):
            # Проверка длины введенной попытки
            messagebox.showwarning("Ошибка", f"Должно быть {len(self.secret_number)} символов!")
            return

        # Подсчет быков и коров
        bulls, cows = self.calculate_score(attempt)
        self.attempts.append((attempt, bulls, cows))  # Добавление попытки в историю
        self.update_attempts_display()  # Обновление списка попыток

        if bulls == len(self.secret_number):
            # Победа, если число полностью угадано
            messagebox.showinfo("Победа", "Поздравляю! Вы победили!")
            self.root.quit()
        else:
            # Вывод текущего результата
            self.result_msg.config(text=f'Попытка: {attempt} - {bulls} быка(ов), {cows} коровы(ы)')

        self.attempt_entry.delete(0, tk.END)  # Очистка поля ввода

    def calculate_score(self, attempt):
        # Подсчет количества быков и коров
        bulls = sum(a == b for a, b in zip(attempt, self.secret_number))  # Быки: совпадение позиции и символа
        cows = sum(min(attempt.count(x), self.secret_number.count(x)) for x in set(attempt)) - bulls  # Коровы: совпадение символов без учета позиции
        return bulls, cows

    def update_attempts_display(self):
        # Обновление отображения истории попыток
        self.attempts_display.config(state='normal')
        self.attempts_display.delete('1.0', tk.END)
        for attempt, bulls, cows in self.attempts:
            self.attempts_display.insert(tk.END, f"Попытка: {attempt} - {bulls} быка(ов), {cows} коровы(ы)\n")
        self.attempts_display.config(state='disabled')

# Точка входа в программу
if __name__ == "__main__":
    root = tk.Tk()
    game = BullsAndCowsGame(root)  # Создание экземпляра игры
    root.mainloop()  # Запуск основного цикла приложения