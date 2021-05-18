"""REST-API server"""
from flask import Flask, request, send_file, render_template, Response
from push_pull_file import PushPullFile
from answers import AnswerDictionaries
from PyPDF2 import utils
from requests import exceptions
import logging, re, os


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # To work with utf-8
app.config['JSON_SORT_KEYS'] = False # To save the right order in the dictionaries


@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def index():
    """Shows the empty main page"""
    errors = request.args.get('errors')
    error_lines = []

    # make logs reversed
    with open("reversed_logs.log", "w") as f:
        # regex for deleting color ansi symbols
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        for line in reversed(list(open("logs.log"))):
            f.write(ansi_escape.sub('', line.rstrip()) + "\n")

    # take our ready logs and dislay them depending on 'errors' argument
    with open("reversed_logs.log", "r") as f:
        if errors is None:
            logs = f.readlines()
            return render_template("index.html", logs=logs)
        else:
            error_lines = [line for line in f if "ERROR" in line]
            if len(error_lines) == 0:
                error_lines.append("There are no errors yet")
            return render_template("index.html", logs=error_lines)


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
        PushPullFile.push_pull_file(arguments)

    except utils.PdfReadError as e:
        app.logger.error(f'{request.host} - - "{request.method} {request.url}" : '
        f'{AnswerDictionaries.pypdf2_errors(e)["информация_об_ошибке"]["сообщение_ошибки"]} ')
        return AnswerDictionaries.pypdf2_errors(e)

    except FileNotFoundError as e:
        app.logger.error(f'{request.host} - - "{request.method} {request.url}" : '
        f'{AnswerDictionaries.existing_errors(e)["информация_об_ошибке"]["сообщение_ошибки"]} ')
        return AnswerDictionaries.existing_errors(e)

    except AttributeError as e:
        app.logger.error(f'{request.host} - - "{request.method} {request.url}" : '
        f'{AnswerDictionaries.existing_errors(e)["информация_об_ошибке"]["сообщение_ошибки"]} ')
        return AnswerDictionaries.existing_errors(e)

    except OSError as e:
        app.logger.error(f'{request.host} - - "{request.method} {request.url}" : '
        f'{AnswerDictionaries.existing_errors(e)["информация_об_ошибке"]["сообщение_ошибки"]} ')
        return AnswerDictionaries.existing_errors(e)

    except exceptions.MissingSchema as e:
        app.logger.error(f'{request.host} - - "{request.method} {request.url}" : '
        f'{AnswerDictionaries.existing_errors(e)["информация_об_ошибке"]["сообщение_ошибки"]} ')
        return AnswerDictionaries.existing_errors(e)

    else:
        return AnswerDictionaries.no_error_answer()


if __name__ == "__main__":
    logging.basicConfig(filename='logs.log', level=logging.DEBUG, filemode="w",
                        format='%(asctime)s %(levelname)s : %(message)s')
    app.run(host='127.0.0.1', debug=True)


























