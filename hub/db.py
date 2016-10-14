from hub import get_db, IntegrityError

def mark_thermostat_as_offline(thermostat_id, db=None):
    if db is None:
        db = get_db()

    db.execute('UPDATE thermostats '
               '   SET online = 0 '
               'WHERE  id = ?',
               [thermostat_id])
    db.commit()

def get_all_thermostats(online_only=False, db=None):
    if db is None:
        db = get_db()

    if online_only:
        sql = 'SELECT * FROM thermostats WHERE online = 1'
    else:
        sql = 'SELECT * FROM thermostats'

    cur = db.execute(sql)
    return cur.fetchall()

def get_thermostat_by_id(unique_id):
    db = get_db()
    cur = db.execute('SELECT * FROM thermostats '
                     'WHERE  id = ?',
                     [unique_id])
    return cur.fetchone()

def add_or_update_thermostat(data):
    db = get_db()
    try:
        db.execute('INSERT INTO thermostats (id, ip_address, port, online) '
                   'VALUES (?, ?, ?, 1)',
                   [data['id'], data['ip_address'], data['port']])
    except IntegrityError:
        db.execute(
            'UPDATE thermostats '
            '   SET ip_address = ?, '
            '       port = ?, '
            '       online = 1 '
            'WHERE  id = ?',
            [data['ip_address'], data['port'],
             data['id']])

    db.commit()
