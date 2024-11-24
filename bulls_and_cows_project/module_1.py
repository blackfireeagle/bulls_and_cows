from main_final import BullsAndCowsGame

def run_game():
    '''
    Точка входа для запуска игры. Создает окно и tkinter запускает приложение.
    '''
    root = tk.Tk()
    game = BullsAndCowsGame(root) #Создание экземпляра игры
    root.mainloop()

# Проверка н прямой запуск модуля
if __name__ == '__main__':
    run_game()
