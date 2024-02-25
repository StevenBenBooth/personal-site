import os
import pandas as pd
import sqlalchemy as sa
from server.src.app import app, db, Locations, Cafe

# Big TODO: make it so that this more sensibly uses the database session


# TODO: try to maintain signature of inner function
def execute_stmt(func):
    def inner(*args, **kwargs):
        stmt = func(*args, **kwargs)
        with app.app_context():
            res = db.session.execute(stmt)
            db.session.commit()
        return res

    return inner


# @execute_stmt
# def add_wifi_status(status):
#     return sa.insert(WifiStatus).values(name=status)


@execute_stmt
def add_location(location):
    return sa.insert(Locations).values(name=location)


@execute_stmt
def add_cafe(
    name,
    has_walkup_window,
    review,
    rating,
    location_id,
    wifi_status_id,
    sparkling_water_ind,
):
    return sa.insert(Cafe).values(
        name=name,
        walkup_window_ind=int(has_walkup_window),
        review=review,
        rating=rating,
        location_id=location_id,
        wifi_status_id=wifi_status_id,
        sparkling_water_ind=int(sparkling_water_ind),
    )


add_location("Seattle - SLU")
add_location("Seattle - Pioneer Square")
add_location("Seattle - Downtown")
add_location("Seattle - Pike Place")
add_location("Vancouver")
add_location("Oceanside, CA")
add_location("San Diego")

cafe_db = pd.read_csv(
    os.path.join("notes", "cafe info.csv"),
    names=[
        "name",
        "review",
        "rating",
        "location_id",
        "has_walkup_window",
        "wifi_status_id",
        "sparkling_water_ind",
    ],
    quotechar='"',
    header=None,
)

for row in cafe_db.to_dict(orient="records"):
    add_cafe(
        name=row["name"],
        has_walkup_window=row["has_walkup_window"],
        review=row["review"],
        rating=row["rating"],
        location_id=row["location_id"],
        wifi_status_id=row["wifi_status_id"],
        sparkling_water_ind=row["sparkling_water_ind"],
    )
