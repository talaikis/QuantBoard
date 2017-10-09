from os.path import join

from pandas import DataFrame, read_csv, to_datetime
from flask import Flask, jsonify, make_response, request, abort

import settings


app = Flask(__name__)


def data(symbol):
    if settings.USE_LOCAL:
        filename = join(settings.DATA_FOLDER, 
            "DATA_MODEL_{0}_{1}_{2}.csv".format(settings.BROKER, symbol, settings.PERIOD))
        data = read_csv(filepath_or_buffer=filename, sep=',', header=0, names=None, index_col=0)
        data.sort_index(axis=0, ascending=True, inplace=True)
        data.index = to_datetime(data.index).to_pydatetime()
        data = data.last('12M')
        data.index = data.index.map(str)
        j = {
            'symbol': symbol,
            'data': data.to_dict(orient='index')
        }
        return j


@app.route('/api/v1.0/symbols', methods=['GET'])
def get_symbols():
    symbols = []
    for s in settings.WATCHLIST_MAP:
        symbol = s.split(",")[0]
        symbols.append({"SYMBOL": symbol})
    return jsonify(symbols)


@app.route('/api/v1.0/data/<string:symbol>', methods=['GET'])
def get_data(symbol):
    return jsonify(data(symbol=symbol))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': 'Not found'}), 404)


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'Error': 'Unauthorized access'}), 403)


if __name__ == '__main__':
    app.run(debug=settings.DEBUG)