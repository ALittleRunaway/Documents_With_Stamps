"""REST-API server"""
from flask import Flask, request, send_file
# from Demo.push_pull_file import PushPullFile
from push_pull_file import PushPullFile
from answers import AnswerDictionaries
from PyPDF2 import utils
from requests import exceptions


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # To work with utf-8
app.config['JSON_SORT_KEYS'] = False # To save the right order in the dictionaries

@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def index():
    """Shows the empty main page"""
    return "fdgf"


@app.route("/stamp", methods=['GET'])
def stamp():
    """Processes 'stamp' method"""
    take_path = request.args.get('take_path')
    put_path = request.args.get('put_path')

    arguments = {"take_path": take_path,
                 "put_path": put_path,
                 }
    # Для открытия окна загрузки раскомментировапть строчку ниже
    # return send_file(path, as_attachment=True)
    # handling errors
    try:
        path = PushPullFile.pull_file(arguments)
        # PushPullFile.push_file()
    except utils.PdfReadError as e:
        return AnswerDictionaries.pypdf2_errors(e)
    except FileNotFoundError as e:
        return AnswerDictionaries.existing_errors(e)
    except exceptions.MissingSchema as e:
        return AnswerDictionaries.existing_errors(e)
    else:
        return AnswerDictionaries.no_error_answer()


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)


























