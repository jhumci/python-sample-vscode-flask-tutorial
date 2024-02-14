from datetime import datetime
from flask import Flask, render_template, request, jsonify
from . import app
import datetime
import json

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")


@app.route('/lager', methods=['GET'])
def query_records():
    name = request.args.get('name')
    print(name)
    if name == "all":
        with open('static/data.json', 'r') as f:
            data = f.read()
            records = json.loads(data)
            return jsonify(records)
        
    with open('static/data.json', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for record in records:
            if record['name'] == name:
                return jsonify(record)
        return jsonify({'error': 'data not found'})

    
@app.route('/lager', methods=['PUT'])
def create_record():
    # Check if the request JSON is valid
    try:
        record = json.loads(request.data)
        name, machine_id, date, granulate_color, amount_in_g = record["name"], record["machine_id"], record["date"], record["granulate_color"], record["amount_in_g"]
    except ValueError:
        return jsonify({'error': 'Invalid input'})
    
    record = json.loads(request.data)
    with open('static/data.json', 'r') as f:
        data = f.read()
    if not data:
        records = [record]
    else:
        records = json.loads(data)
        records.append(record)
    with open('static/data.json', 'w') as f:
        f.write(json.dumps(records, indent=2))
    record["bestell_status"] = "ok"
    # Make the Datum in the format of YYYY-MM-DD HH:MM and add one day and 3 hours
    geplantes_lieferdatum = datetime.datetime.now() + datetime.timedelta(days=1, hours=3)
    record["geplantes_lieferdatum"] = geplantes_lieferdatum.strftime("%Y-%m-%d %H:%M")
    return jsonify(record)