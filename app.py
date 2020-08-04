"""Main flask app for parsing restitutions xls"""

from flask import Flask, jsonify, request
frm flask_cors import CORS, cross_origin
from modules.scrapingCacaoData import scrapCacaoToJson
import sys
import logging

app = Flask(__name__)
# heroku logging
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


@app.route('/')
def hello_world():
    return "GET CACAO !"


@app.route('/json', methods=["GET"])
def getCacao():
    """
    Post method takes xls from request
    returns json of data with quantiles and risk calculated
    """
    return jsonify(scrapCacaoToJson())


if __name__ == "__main__":
    app.run()
