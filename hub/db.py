from hub import get_db

def mark_thermostat_as_offline(thermostat_id):
    db = get_db()
    db.execute('UPDATE thermostats '
               '   SET online = 0 '
               'WHERE  id = ?',
               [thermostat_id])
    db.commit()
