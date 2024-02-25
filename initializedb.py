# you need this line even though they're not accessed bc of how the tables were setup
# I believe you could get around this using a MetaData object, but I'm not sure
from server.src.app import app, db, Locations, Cafe

with app.app_context():
    db.drop_all()
    db.create_all()
