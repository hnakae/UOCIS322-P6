"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
# import datetime

import acp_times  # Brevet time calculations
import config

import logging
from pymongo import MongoClient

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times", methods=['POST'])
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    content = request.get_json()
    print(content)

    km_list = content['km_list'];
    distance = float(content['distance']);
    begin_date = content['begin_date'];
    # dt_begin_date = arrow.get(begin_date, 'YYYY-MM-DDTHH:mm');

    print(begin_date);

    result = [];


    for info in km_list:
        print(info)
        n_km = float(info['km'])
        open_time = acp_times.open_time(n_km, distance, begin_date).format('YYYY-MM-DDTHH:mm')

        close_time = acp_times.close_time(n_km, distance, begin_date).format('YYYY-MM-DDTHH:mm')

        result.append(
            {
                "index": int(info['index']),
                "open_time": open_time,
                "close_time": close_time
            }
        )


    print(result)



    # FIXME!
    # Right now, only the current time is passed as the start time
    # and control distance is fixed to 200
    # You should get these from the webpage!
    # open_time = acp_times.open_time(km, distance, begin_date.isoformat).format('YYYY-MM-DDTHH:mm')

    # close_time = acp_times.close_time(km, distance, begin_date.isoformat).format('YYYY-MM-DDTHH:mm')
    # open_time="2021-05-01T00:00"
    # close_time="2021-07-01T00:00"
    # result = {"open_time": open_time, "close_time": close_time}
    return flask.jsonify(result=result)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
