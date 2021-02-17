from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__, static_folder='static', static_url_path=None)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../../data.db"

db = SQLAlchemy(app)
Base = automap_base()
Base.prepare(db.engine, reflect=True)

App = Base.classes.app
AppSdk = Base.classes.app_sdk
Sdk = Base.classes.sdk


@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html', options=db.session.query(Sdk).all())


@app.route('/data')
def data():
    options = request.args.getlist('options[]')
    d = {}
    d['series'] = []
    app_sdk = db.session.query(AppSdk)

    # options to options and none
    for id in options:
        t = {}
        for sdk in options:
            t[sdk] = 0
        t['none'] = 0

        total_temp = app_sdk.filter(AppSdk.sdk_id == int(id))
        t[id] = total_temp.count()

        not_installed = total_temp.filter(AppSdk.installed == 0).all()

        for item in not_installed:

            churned = app_sdk.filter(AppSdk.app_id == item.app_id).filter(AppSdk.installed == 1).all()
            churned_ids = [str(c.sdk_id) for c in churned]

            for cid in churned_ids:
                if cid not in options:
                    t['none'] += 1
                else:
                    t[cid] += 1
        d['series'].append(t)

    # From other to options
    k = {'none': 0}  # Initializing another temp
    other_entries = None

    for id in options:
        k[id] = 0
        other_entries = app_sdk.filter(AppSdk.sdk_id != int(id))    # Eliminating given options

    k['none'] = other_entries.count()
    not_installed = other_entries.filter(AppSdk.installed == 0).all()

    for item in not_installed:
        churned = app_sdk.filter(AppSdk.app_id == item.app_id).filter(AppSdk.installed == 1).all()
        churned_ids = [str(c.sdk_id) for c in churned]
        for cid in churned_ids:
            if cid in options:
                k[cid] += 1
    d['series'].append(k)

    options.append('none')
    res = {
        'series': [
        ],
        'categories': []
    }

    for ind in range(0, len(d['series'])):

        try:
            name = db.session.query(Sdk).filter(Sdk.id == options[ind]).first().name
        except:
            name = '(none)'

        res['series'].append({
                #'name': name,
                'values': [d['series'][ind][j]+0.0 for j in options]
            })
        res['categories'].append(name)

    return jsonify(res)


if __name__ == '__main__':
    app.run()
