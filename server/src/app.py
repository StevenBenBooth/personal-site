from flask import Flask, render_template, make_response, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

# TODO: can this also be from flask_sqlalchemy?
from sqlalchemy import select

import os

deploy = True
# need to use base_dir to make this work both here and on Docker deploy
db_path = os.path.join(os.path.dirname(__file__), "cafe.db")
os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
# os.environ["FLASK_APP"] = r"D:\dev\sites\steven-booth\.venv\..\server\src\app.py"
os.environ["DEBUG"] = "True"


COFFEE_EMOJI = "\u2615"
YES_SYMBOL = "\u2714"
NO_SYMBOL = "\u2718"
MAYBE_SYMBOL = "?"


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "")
    # FLASK_APP = os.environ.get("FLASK_APP", "")
    DEBUG = os.environ.get("DEBUG", "") == "True"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = "development key"


app = Flask(__name__)
app.config.from_object(Config)

# instantiate representation of database
db = SQLAlchemy(app)


# TODO: It's tragic I had to put all this in one file, but I couldn't get the imports to work in Docker

# class WifiStatus(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), nullable=False)
#     cafes = db.relationship("Cafe", back_populates="wifi_status")


class Locations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    cafes = db.relationship("Cafe", back_populates="location")


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    walkup_window_ind = db.Column(db.Integer, default=0)
    review = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey(Locations.id), nullable=False)
    wifi_status_id = db.Column(db.Integer, nullable=False)
    # db.ForeignKey(WifiStatus.id)
    sparkling_water_ind = db.Column(db.Integer, nullable=False)
    location = db.relationship("Locations", back_populates="cafes")

    def __repr__(self):
        return f"<Cafe {self.cafe_name}>"

    # These are used for formatting in the template
    def get_rating(self):
        return COFFEE_EMOJI * self.rating

    def get_wifi_status(self):
        if self.wifi_status_id == 0:
            return YES_SYMBOL
        elif self.wifi_status_id == 1:
            return NO_SYMBOL
        elif self.wifi_status_id == 2:
            return MAYBE_SYMBOL

    def get_location(self):
        # TODO: how to get the name instead of the value?
        return (
            db.session.execute(
                select(Locations.name).where(Locations.id == self.location_id)
            )
            .fetchone()
            .name
        )

    def has_walkup_window(self):
        if bool(self.walkup_window_ind):
            return YES_SYMBOL
        return NO_SYMBOL

    def has_sparkling_water(self):
        if bool(self.sparkling_water_ind):
            return YES_SYMBOL
        return NO_SYMBOL


# Routes
@app.route("/")
def index():
    template = render_template("index.html")
    response = make_response(template)
    response.headers["Cache-Control"] = "public, max-age=300, s-maxage=600"
    return response


# Note to self: if you want to limit it to actual paths, it will redirect correctly if you include last / but not the other way
@app.route("/reviews/")
def reviews():
    cafes = Cafe.query.all()
    template = render_template("reviews.html", cafes=cafes)
    response = make_response(template)
    response.headers["Cache-Control"] = "public, max-age=300, s-maxage=600"

    return response


# TODO: Do I need this?

# if __name__ == '__main__':
#     app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
