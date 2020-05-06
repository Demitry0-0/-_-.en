class PasswordError(Exception):
    def __init__(self):
        super.__init__()


class LengthError(PasswordError):
    def __init__(self):
        pass

    def __str__(self):
        return 'LengthError'


class LetterError(PasswordError):
    def __init__(self):
        pass

    def __str__(self):
        return 'LetterError'


class DigitError(PasswordError):
    def __init__(self):
        pass

    def __str__(self):
        return 'DigitError'


class SequenceError(PasswordError):
    def __init__(self):
        pass

    def __str__(self):
        return 'SequenceError'


class WordError(PasswordError):
    def __init__(self):
        pass

    def __str__(self):
        return 'WordError'


def check_password(password, flag):
    global words
    if 'ctrl+break' in password.lower() or 'ctrl-break' in password.lower():
        raise KeyboardInterrupt
    up_case = low_case = digits = nearby_letters = False
    if len(password) < 9 and flag == 'LetterError':
        raise LengthError
    for symb in password:
        up_case = up_case or symb.isupper()
        low_case = low_case or symb.islower()
        digits = digits or symb.isdigit()
    if (not up_case or not low_case) and flag == 'LetterError':
        raise LetterError
    if not digits and flag == 'DigitError':
        raise DigitError
    bad_symbs_en = 'qwertyuiop   asdfghjkl   zxcvbnm  '
    bad_symbs_ru = 'йцукенгшщзхъ фывапролджэё ячсмитьбю'
    password = password.lower()
    for i in range(len(password) - 2):
        pos_1 = max(bad_symbs_en.find(password[i]), bad_symbs_ru.find(password[i]))
        pos_2 = max(bad_symbs_en.find(password[i + 1]), bad_symbs_ru.find(password[i + 1]))
        pos_3 = max(bad_symbs_en.find(password[i + 2]), bad_symbs_ru.find(password[i + 2]))
        if pos_1 >= 0 and pos_2 >= 0 and pos_3 >= 0:
            nearby_letters = nearby_letters or (pos_2 - pos_1 == pos_3 - pos_2 == 1)
    if nearby_letters and flag == 'SequenceError':
        raise SequenceError
    if flag == 'WordError':
        password = password.lower()
        for word in words:
            if word in password:
                raise WordError
    return 'ok'


dct = {'SequenceError': 0, 'DigitError': 0, 'LetterError': 0, 'LengthError': 0, 'WordError': 0}
top_password = input('Введите имя файла с паролями. По умолчанию выбран файл top_password.txt\n')
if not top_password:
    top_password = 'top_password.txt'
top_words = input('Введите имя файла со словами. По умолчанию выбран файл top_words.txt\n')
if not top_words:
    top_words = 'top_words.txt'
file = open(top_password, mode='r', encoding='utf-8')
list_password = file.readlines()
file.close()
file = open(top_words, mode='r', encoding='utf-8')
words = file.readlines()
file.close()
for key in list_password:
    for flag in dct.keys():
        try:
            check_password(key, flag)
        except Exception as error:
            dct[str(error)] += 1
mx = len(max(dct.keys(), key=lambda x: len(x)))
for key in sorted(dct.keys()):
    print('Исключение: {}{}    Количество: {}'.format(key, (mx - len(key)) * ' ', dct[key]))
