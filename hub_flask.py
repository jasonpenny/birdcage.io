import os

from hub import app, init_db

# initialize database if it doesn't exist
if not os.path.isfile(app.config['DATABASE']):
    init_db()

app.run(port=3000)
