"""Main flask app for parsing restitutions xls"""

from flask import Flask, jsonify, request
from modules.xlsToJsonAssurances import xlsToJson
import sys
import logging

app = Flask(__name__)
# heroku logging
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


@app.route('/')
def hello_world():
    return "Hello!"


@app.route('/json', methods=["POST"])
def postXLS():
    """
    Post method takes xls from request
    returns json of data with quantiles and risk calculated
    """
    return jsonify(xlsToJson(request.get_data()))


if __name__ == "__main__":
    app.run()
