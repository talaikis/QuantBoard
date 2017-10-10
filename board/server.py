from os.path import join

from numpy import where
from pandas import DataFrame, read_csv, to_datetime
from flask import Flask, jsonify, make_response, request, abort

import settings
from _private.indicators import Indicators


app = Flask(__name__)


def get_data(symbol, indicator, period):
    if settings.USE_LOCAL:
        filename = join(settings.DATA_FOLDER, 
            "DATA_MODEL_{0}_{1}_{2}.csv".format(settings.BROKER, symbol, settings.PERIOD))
        data = read_csv(filepath_or_buffer=filename, sep=',', header=0, names=None, index_col=0)
        data.sort_index(axis=0, ascending=True, inplace=True)
        data.index = to_datetime(data.index).to_pydatetime()
        data = data.last('12M')
        data.index = data.index.map(str)
        indie = Indicators(data=data, period=period, indicator=indicator)
        data = indie.value()
        prob = sum(where(data.CLOSE.pct_change() > 0, 1, 0)) / len(data.index)

        # 2. get weekly/ monthly data
        # 3. get vix status

        j = {
            'symbol': symbol,
            'daily_stats': {
                'skewness': data.CLOSE.skew(),
                'probability': prob,
                'avg_return': data.CLOSE.pct_change().mean()
            },
            'weekly_stats': {
                'skewness': 0,
                'probability': 0,
                'avg_return': 0
            },
            'monthly_stats': {
                'skewness': 0,
                'probability': 0,
                'avg_return': 0
            },
            'data': data.to_dict(orient='index')
        }
        return j
    else:
        print(">> Non-local data not implemented.")


@app.route('/api/v1.0/symbols', methods=['GET'])
def get_symbols():
    symbols = []
    for s in settings.WATCHLIST_MAP:
        symbol = s.split(",")[0]
        symbols.append({"SYMBOL": symbol})
    return jsonify(symbols)


@app.route('/api/v1.0/data/<string:symbol>/<string:indicator>/<int:period>', methods=['GET'])
def api_data(symbol, indicator, period):
    return jsonify(get_data(symbol=symbol, indicator=indicator, period=period))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=settings.DEBUG)