"""Class for retuening answers in json format"""

class AnswerDictionaries():
    """Makes json dictionaris for answer"""

    @staticmethod
    def no_error_answer():
        """When everything is fine"""
        d = {'error_info': {}}
        d['error_info'] = {"error_code": 0, "error_name": None,
                           "error_message": "Your file has been saved successfully"}
        return d

    @staticmethod
    def pypdf2_errors(e):
        """For the sqlalchemy errors"""
        d = {'error_info': {}}

        if str(e) == "EOF marker not found":
            d['error_info']['error_code'] = 1
            d['error_info']['error_name'] = str(e)
            d['error_info']['error_message'] = "There is no file or it is not in the right format"

        return d

    @staticmethod
    def existing_errors(e):
        """For the sqlalchemy errors"""
        d = {'error_info': {}}

        if str(e).startswith("[Errno 2]"):
            d['error_info']['error_code'] = 2
            d['error_info']['error_name'] = "FileNotFoundError"
            d['error_info']['error_message'] = str(e)

        elif str(e).startswith("Invalid URL"):
            d['error_info']['error_code'] = 3
            d['error_info']['error_name'] = "InvalidURLError"
            d['error_info']['error_message'] = "No schema supplied. Try changing your url"

        return d





