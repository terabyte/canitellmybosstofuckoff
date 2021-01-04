from cachetools import cached, LRUCache
from time import time
import concurrent.futures
import json
import os
import random
import re

from flask import Flask, render_template, request, flash, send_from_directory

app = Flask(__name__)

# there is literally nothing at all to secure in this app
# echo "i haz sekurity\!" | sha256sum
app.config['SECRET_KEY'] = "79385337781537646e9c3d04f8b8f2679f4f79e2135d414862966abf244bb292"

defaults = {
    "total_savings": 2000000.0,
    "annual_disbursement": 120000.0,
    "average_return": 0.08,
    "standard_deviation": 0.13,
    "annual_inflation": 0.0225,
    "starting_age": 40,
    "ending_age": 95,
    "inheritance": 0.0,
    "social_security_payout": 0,
    "social_security_age": 70,
    "calculate": False,
    "success": 0.0,
    "issuccess": "Maybe",
    'runtime': None,
}

# https://stackoverflow.com/questions/1006289/how-to-find-out-the-number-of-cpus-using-python/55423170#55423170
parallelism = len(os.sched_getaffinity(0))
batch_size = 1000
simulation_size = 100000
success_threshold = 0.95
maybe_threshold = 0.80

helptext = None
with open('configs/helptext.json') as f:
    helptext = json.load(f)

variants = {
    "shoveit": re.compile(".*shoveit\\.com.*"),
    "fuckoff": re.compile(".*fuckoff\\.com.*"),
    "dev": re.compile(".*:5000/.*"),
}

variant_map = {
    "shoveit": {
        "text": "shove it",
        "capitalized": "Shove It",
        "sentence": "Shove it",
    },
    "fuckoff": {
        "text": "fuck off",
        "capitalized": "Fuck Off",
        "sentence": "Fuck off",
    },
    "dev": {
        "text": "shove it",
        "capitalized": "Shove It",
        "sentence": "Shove it",
    },
}


def add_variant_data(data):
    # default to SFW version I guess
    data['variant'] = 'shoveit'
    data['variant_map'] = variant_map
    # determine if we are NSFW version or SFW version
    for variant, rxp in variants.items():
        print(f"Trying url {request.url} against variant {variant} with regexp {rxp}")
        if rxp.match(request.url):
            print(f"Detected variant {variant}")
            data['variant'] = variant


@app.route('/', methods=('GET', 'POST'))
def index():
    data = dict()

    if request.method == 'POST':
        data = validate_and_parse_form(request.form)
        data['calculate'] = True
        start = time()
        success = monte_the_carlo_parallel(data)
        end = time()
        data['runtime'] = f"{end - start:.3f}"
        data['success'] = f"{success*100:.2f}"
        if success > success_threshold:
            data['issuccess'] = 'YUP!'
        elif success > maybe_threshold:
            data['issuccess'] = 'MAYBE?'
        else:
            data['issuccess'] = 'NOPE!'

    if request.method == 'GET':
        data = defaults

    data['simulation_size'] = simulation_size
    add_variant_data(data)
    add_helptext(data)
    return render_template('index.html', data=data)


@app.route('/about')
def about():
    data = dict()
    add_variant_data(data)
    return render_template('about.html', data=data)


@app.route('/faq')
def faq():
    data = dict()
    add_variant_data(data)
    return render_template('faq.html', data=data)


# https://flask.palletsprojects.com/en/1.1.x/patterns/favicon/
@app.route('/favicon.ico')
def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static', 'favicon'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/browserconfig.xml')
def browserconfig():
        return send_from_directory(os.path.join(app.root_path, 'static', 'favicon'), 'browserconfig.xml', mimetype='application/xml')


def validate_and_parse_form(form):
    data = dict()
    data['total_savings'] = validate_dollars("Total Savings", form['total_savings'])
    data['annual_disbursement'] = validate_dollars("Annual Disbursement", form['annual_disbursement'])
    data['average_return'] = validate_percent("Average Return", form['average_return'])
    data['standard_deviation'] = validate_percent("Standard Deviation", form['standard_deviation'])
    data['annual_inflation'] = validate_percent("Annual Inflation", form['annual_inflation'])
    data['starting_age'] = validate_age("Starting Age", form['starting_age'])
    data['ending_age'] = validate_age("Ending Age", form['ending_age'])
    data['inheritance'] = validate_dollars("Inheritance", form['inheritance'])
    data['social_security_payout'] = validate_dollars("Social Security Payout", form['social_security_payout'])
    data['social_security_age'] = validate_dollars("Social Security Age", form['social_security_age'])
    return data


def validate_dollars(field_name, value):
    try:
        return float(value)
    except Exception:
        flash(f"'{field_name}' must be a floating point number, got '{value}'")
        return 0.0


def validate_percent(field_name, value):
    try:
        val = float(value)
        if val < 0.0 or val > 1.0:
            flash(f"WARNING: {field_name} ({value}) is outside range 0% (0.0) to 100% (1.0), did you mean to do that?")

        return val
    except Exception:
        flash(f"'{field_name}' must be a floating point number (i.e. 8% => 0.08), got '{value}'")
        return 0.0


def validate_age(field_name, value):
    try:
        val = int(value)
        if val < 1 or val > 200:
            flash(f"'{field_name}' must be an integer number from 1 to 200, got '{value}'")
            return 0
        return val
    except Exception:
        flash(f"'{field_name}' must be an integer number from 1 to 200, got '{value}'")
        return 1


def run_sim_batch(data):
    yes_count = 0
    total_count = 0
    for i in range(0, batch_size):
        total_count += 1
        if simulate_universe(data['average_return'], data['standard_deviation'], data['total_savings'], data['annual_disbursement'], data['annual_inflation'], data['starting_age'], data['ending_age'], data['inheritance'], data['social_security_payout'], data['social_security_age']):
            yes_count += 1
    return yes_count, total_count


def freezehash(o):
    return frozenset(o.items())


# After some testing, discovered that parallelism with batch sizes of 1000 turn
# a 100k simulation load from 3.5s to just under 1s, on my 12core laptop.
@cached(cache=LRUCache(maxsize=1000000), key=freezehash)
def monte_the_carlo_parallel(data):
    yes_count = 0
    total_count = 0

    with concurrent.futures.ProcessPoolExecutor(max_workers=parallelism) as executor:
        for yes, total in executor.map(run_sim_batch, map(lambda x: data, range(0, int(simulation_size / batch_size)))):
            yes_count += yes
            total_count += total

    return 1.0 * yes_count / total_count


def monte_the_carlo(data):
    yes_count = 0
    for i in range(0, simulation_size):
        if simulate_universe(data['average_return'], data['standard_deviation'], data['total_savings'], data['annual_disbursement'], data['annual_inflation'], data['starting_age'], data['ending_age'], data['inheritance'], data['social_security_payout'], data['social_security_age']):
            yes_count += 1
    return 1.0 * yes_count / simulation_size


def simulate_universe(avg_ret, std_dev, savings, disbursement, inflation, s_age, e_age, req_leftover, ss_payout, ss_age):
    for i in range(s_age, e_age):
        ret = random.normalvariate(avg_ret, std_dev)
        savings = savings * (1.0 + ret)
        if i >= ss_age:
            savings = savings - (disbursement - (ss_payout * 12))
        else:
            savings = savings - disbursement
        if savings < req_leftover:
            return False
        # inflate things
        disbursement = disbursement * (1.0 + inflation)
        req_leftover = req_leftover * (1.0 + inflation)
        ss_payout = ss_payout * (1.0 + inflation)
    return True


def add_helptext(data):
    data['helptext'] = helptext


if __name__ == "__main__":
    app.run(host='0.0.0.0')
