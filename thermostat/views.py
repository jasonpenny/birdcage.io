from thermostat import app, get_db, jsonify, request, IntegrityError

@app.route('/')
def general_info():
    db = get_db()
    cur = db.execute('SELECT * FROM info')
    info = cur.fetchone()
    return jsonify(dict(info))
