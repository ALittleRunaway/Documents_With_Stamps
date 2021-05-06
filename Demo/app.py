"""REST-API server"""
from flask import Flask, request, send_file
# from Demo.push_pull_file import PushPullFile
from push_pull_file import PushPullFile


app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False # To work with utf-8
# app.config['JSON_SORT_KEYS'] = False # To save the right order in the dictionaries

@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def index():
    """Shows the empty main page"""
    return ""


@app.route("/stamp", methods=['GET'])
def query():
    """Processes 'stamp' method"""
    take_path = request.args.get('take_path')
    put_path = request.args.get('put_path')

    arguments = {"take_path": take_path,
                 "put_path": put_path,
                 }
    # returns the json dictionary
    path = PushPullFile.pull_file(arguments)
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)


# curl -OL https://raw.githubusercontent.com/ALittleRunaway/for_practice/blob/master/sertificates/test_pdf_3.pdf
# curl https://www.camozzi.ru/netcat_files/541/691/Deklaratsiya_na_resivery_Kamotstsi.pdf -o output.pdf

























