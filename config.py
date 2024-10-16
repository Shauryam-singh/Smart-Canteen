from app import db, app
from models import User, Item

with app.app_context():
    db.create_all()

    # Add some test data
    db.session.add(Item(name="Sandwich", available=True))
    db.session.add(Item(name="Burger", available=False))
    db.session.add(Item(name="Pizza", available=True))
    db.session.commit()
