from flask import Flask
from flask import request
from flask import render_template
from flask import make_response 
from flask import jsonify

import numpy as np

import StringIO
import csv
import time
import logging
from logging.handlers import SysLogHandler

app = Flask(__name__)

# log Flask events
app.logger.setLevel(logging.DEBUG)
# address for OSX
handler = SysLogHandler(address='/var/run/syslog')
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)

app.logger.debug(u"Flask server started " + time.asctime())

@app.after_request
def write_access_log(response):
    app.logger.debug(u"%s %s --> %s" % (time.asctime(), request.path, response.status_code))
    return response

@app.teardown_appcontext
def shutdown_session(exception=None):
    pass

##############

def get_coin_trial(n=100, p=0.5):
    result = list(np.random.choice([0,1],n, p=[p, 1.0-p]))
    return result

def get_coin_ensemble(k=10, n=100, p=0.5):
    result = [get_coin_trial(n, p) for i in range(k)]
    return result

##############

@app.route('/info.html')
def info():
    return render_template( "info.html")

@app.route('/trial')
def trial(n=100, p=0.5):
    n = request.args.get("n", n, type=int)
    p = request.args.get("p", p, type=float)
    result = {
            "n" : n
            , "result" : get_coin_trials(n, p)
            , "p_0" : p
            , "p_1" : 1.0-p
            }
    return jsonify(**result)

@app.route('/ensemble')
def ensemble(k=10, n=100, p=0.5):
    k = request.args.get("k", k, type=int)
    n = request.args.get("n", n, type=int)
    p = request.args.get("p", p, type=float)
    result = {
            "n" : n
            , "results" : get_coin_ensemble(k, n, p)
            , "p_0" : p
            , "p_1" : 1.0-p
            }
    return jsonify(**result)

@app.route('/ensemble/summary')
def ensemble_summary(k=10, n=100, p=0.5):
    k = request.args.get("k", k, type=int)
    n = request.args.get("n", n, type=int)
    p = request.args.get("p", p, type=float)
    res = get_coin_ensemble(k, n, p)
    avgs = [np.average(i) for i in res]
    cnts = [[i.count(0), i.count(1)] for i in res]
    result = { 
            "summary": {
                "counts" : cnts
                , "averages" : avgs
                }, 
            "data": {
                "n" : n
                , "results" : res
                , "p_0" : p
                , "p_1" : 1.0-p
                }
            }
    return jsonify(**result)


@app.route("/plot/demo.png")
def plot_demo():
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    import matplotlib.mlab as mlab
    import matplotlib.pyplot as plt

    mu, sigma = 100, 15
    x = mu + sigma*np.random.randn(10000)

    # the histogram of the data
    n, bins, patches = plt.hist(x, 50, normed=1, facecolor='green', alpha=0.75)

    # add a 'best fit' line
    y = mlab.normpdf( bins, mu, sigma)
    l = plt.plot(bins, y, 'r--', linewidth=1)

    plt.xlabel('Smarts')
    plt.ylabel('Probability')
    plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
    plt.axis([40, 160, 0, 0.03])
    plt.grid(True)

    # Write to the canvas
    fig = plt.gcf()
    fig.set_size_inches(6,5)
    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route("/plot/hist/<spec>.png")
def plot_hist(spec="10_100_500"):
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt

    spec = request.args.get("spec", spec, type=str).split("_")
    assert(len(spec) == 3)

    k = int(spec[0])
    n = int(spec[1])
    p = float(spec[2])/1000.

    res = get_coin_ensemble(k, n, p)
    avgs = [np.average(i) for i in res]

    plt.clf()
    fig = plt.figure()
    l = plt.hist(avgs)

    fig.set_size_inches(5,4)
    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route('/ensemble/table.html')
def table_data(k=5, n=10, p=0.5):
    k = request.args.get("k", k, type=int)
    n = request.args.get("n", n, type=int)
    p = request.args.get("p", p, type=float)
    res = get_coin_ensemble(k, n, p)
    rows = []
    # convert to rows
    for row in range(len(res[0])):
        r = []
        for col in res:
            r.append(col[row])
        rows.append(r)
    return render_template("table.html", rows=rows)

@app.route('/ensemble/csv')
def csv_data(k=5, n=10, p=0.5):
    k = request.args.get("k", k, type=int)
    n = request.args.get("n", n, type=int)
    p = request.args.get("p", p, type=float)
    res = get_coin_ensemble(k, n, p)
    rows = []
    # convert to rows
    for row in range(len(res[0])):
        r = []
        for col in res:
            r.append(col[row])
        rows.append(r)
    si = StringIO.StringIO()
    cw = csv.writer(si)
    cw.writerows(rows)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == '__main__':
    app.run(debug=True)
