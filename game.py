import telebot 
 
# Создаем бота 
bot = telebot.TeleBot('token') 
 
# Создаем поле для игры 
field = ['🤍', '🤍', '🤍', '🤍', '🤍', '🤍', '🤍', '🤍', '🤍']
current_player = '⭕'  
game_over = False
 
# Функция для отображения игрового поля
def display_board():
    message = ''
    for row in field:
        message += ' '.join(row) + '\n'
    return message

def restart_game(chat_id):
    global field, current_player, game_over
    field = ['🤍', '🤍', '🤍', '🤍', '🤍', '🤍', '🤍', '🤍', '🤍']
    current_player = '⭕'
    game_over = False
    bot.send_message(chat_id, "Игра перезапущена!")
    bot.send_message(chat_id, "Введите число от 1 до 9 \n Ход игрока ⭕")
    draw_field(chat_id)

def check_winner(chat_id):
    global field, game_over
    # Проверка выигрышных комбинаций
    win_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for combination in win_combinations:
        if field[combination[0]] == field[combination[1]] == field[combination[2]] != '🤍':
            bot.send_message(chat_id, f"Игрок {field[combination[0]]} выиграл! 🥳🥳")
            game_over = True
            bot.send_message(chat_id, "Хотите сыграть ещё раз? Введите да или нет")
            return
    # Проверка на ничью
    if '🤍' not in field:
        bot.send_message(chat_id, "Игра окончена. Ничья!")
        game_over = True
        bot.send_message(chat_id, "Хотите сыграть ещё раз? Введите да или нет")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = telebot.types.KeyboardButton('Старт')
    rules_button = telebot.types.KeyboardButton('Правила игры')
    markup.row(start_button, rules_button)
    bot.send_message(message.chat.id, 'Добро пожаловать в игру "Крестики-нолики"! Нажми на кнопку "Старт" или "Правила игры"', reply_markup=markup)
    
# Обработчик команды /rules
@bot.message_handler(commands=['rules'])
def handle_rules(message):
    rules = '🔘 Правила игры "Крестики-нолики" ❌/⭕:\n\n' \
            '🔘 Игроки по очереди ставят свои символы на свободные клетки поля 3x3, вводя числа от 1 до 9.\n\n' \
            '🔘 Игровое поле выглядит следующим образом: \n' \
            '   1  2  3       🤍🤍🤍\n' \
            '   4  5  6   =  🤍🤍🤍\n' \
            '   7  8  9       🤍🤍🤍\n' \
            '🔘 Только вместо чисел - 🤍 (пустая клетка) \n\n' \
            '🔘 Первый, выстроивший в ряд (по горизонтали, вертикали или диагонали) три своих символа, выигрывает 🥳\n\n' \
            '🔘 Если все клетки поля заполнены и ни один из игроков не выиграл, игра считается ничьей.\n \n' 
            
    bot.send_message(message.chat.id, rules)

# Обработчик кнопки "Старт"
@bot.message_handler(func=lambda message: message.text == 'Старт')
def handle_start_button(message):
    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Игра началась! Введите число от 1 до 9 \n' 'Ход игрока ⭕', reply_markup=markup)    
    draw_field(message.chat.id)  # Добавлен вызов функции отображения поля

# Обработчик кнопки "Правила игры"
@bot.message_handler(func=lambda message: message.text == 'Правила игры')
def handle_rules_button(message):
    handle_rules(message)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    global field, current_player, game_over
    if message.text == 'да' and game_over:
        restart_game(message.chat.id)
    elif message.text == 'нет' and game_over:
        bot.send_message(message.chat.id, "Спасибо за игру!😉")
    elif message.text.isdigit() and 1 <= int(message.text) <= 9 and not game_over:
        cell_number = int(message.text) - 1
        if field[cell_number] == '🤍':
            field[cell_number] = current_player
            if current_player == '⭕':
                current_player = '❌'
            else:
                current_player = '⭕'
            bot.send_message(message.chat.id, f"Ход игрока {current_player}")
            draw_field(message.chat.id)
            check_winner(message.chat.id)
        else:
            bot.send_message(message.chat.id, "Ячейка уже занята. Сделайте другой ход.")
    elif not game_over:
        bot.send_message(message.chat.id, "Некорректный ход. Введите число от 1 до 9.")

def draw_field(chat_id):
    global field
    field_str = ' '.join(field[:3]) + '\n' + ' '.join(field[3:6]) + '\n' + ' '.join(field[6:])
    bot.send_message(chat_id, field_str)

# Запускаем бота 
bot.polling()
