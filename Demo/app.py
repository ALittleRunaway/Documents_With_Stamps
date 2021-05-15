"""REST-API server"""
from flask import Flask, request, send_file, render_template
# from Demo.push_pull_file import PushPullFile
from push_pull_file import PushPullFile
from answers import AnswerDictionaries
from PyPDF2 import utils
from requests import exceptions
import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # To work with utf-8
app.config['JSON_SORT_KEYS'] = False # To save the right order in the dictionaries


@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def index():
    """Shows the empty main page"""
    errors = request.args.get('errors')
    if errors is None:
        # make logs reversed
        with open("reversed_logs.log", "w") as f:
            for line in reversed(list(open("logs.log"))):
                color_1 = line.find("[37m") - 1
                color_2 = line.find("[0m") - 1
                if color_1 < 0 or color_2 < 0:
                    pass
                else:
                    line = line[:color_1] + line[color_1 + 5:color_2] + line[color_2 + 4:]
                f.write(line.rstrip() + "\n")
        # take uor ready logs and dislay them
        with open("reversed_logs.log", "r") as f:
            logs = f.readlines()
        return render_template("index.html", logs=logs)
    return ":C"


@app.route("/stamp", methods=['GET'])
def stamp():
    """Processes 'stamp' method"""
    take_path = request.args.get('take_path')
    put_path = request.args.get('put_path')

    arguments = {"take_path": take_path,
                 "put_path": put_path,
                 }
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
    logging.basicConfig(filename='logs.log', level=logging.DEBUG, filemode="w")
    # root_logger = logging.getLogger()
    # root_logger.setLevel(logging.DEBUG)  # or whatever
    # handler = logging.FileHandler('logs.log', 'w', 'utf-8')  # or whatever
    # root_logger.addHandler(handler)

    app.run(host='127.0.0.1', debug=True)



























