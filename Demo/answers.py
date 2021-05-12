"""Class for retuening answers in json format"""
import re

class AnswerDictionaries():
    """Makes json dictionaris for answer"""

    @staticmethod
    def no_error_answer():
        """When everything is fine"""
        d = {'информация_об_ошибке': {}}
        d['информация_об_ошибке'] = {"код_ошибки": 0, "название_ошибки": None,
                                     "сообщение_ошибки": "Ваш файл был успешно сохранён"}
        return d

    @staticmethod
    def pypdf2_errors(e):
        """For the sqlalchemy errors"""
        d = {'информация_об_ошибке': {}}

        if str(e) == "EOF marker not found":
            d['информация_об_ошибке']['код_ошибки'] = 1
            d['информация_об_ошибке']['название_ошибки'] = "Неверная ссылка на файл"
            d['информация_об_ошибке']['сообщение_ошибки'] = "Переданного файла не существует или он в неверном формате"

        return d

    @staticmethod
    def existing_errors(e):
        """For the sqlalchemy errors"""
        d = {'информация_об_ошибке': {}}

        if str(e).startswith("[Errno 2]"):
            d['информация_об_ошибке']['код_ошибки'] = 2
            d['информация_об_ошибке']['название_ошибки'] = "Файл не найден"
            pattern = r'(?<=directory: ).+(?=)'
            message = "Нет такого файла или директории: " + re.findall(pattern, str(e))[0]
            d['информация_об_ошибке']['сообщение_ошибки'] = message

        elif str(e).startswith("Invalid URL"):
            d['информация_об_ошибке']['код_ошибки'] = 3
            d['информация_об_ошибке']['название_ошибки'] = "Неверная ссылка"
            d['информация_об_ошибке']['сообщение_ошибки'] = "Ошибка в запросе. Попробуйте изменить url"

        return d





