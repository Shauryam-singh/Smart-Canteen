from app import db, app
from models import User, Item

# Create users
def create_default_users():
    with app.app_context():
        # Check if users already exist
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(username='admin', password='admin123', role='admin')
            db.session.add(admin_user)

        student_user = User.query.filter_by(username='student').first()
        if not student_user:
            student_user = User(username='student', password='student123', role='student')
            db.session.add(student_user)

        db.session.commit()
        print("Admin and student users created or already exist.")

if __name__ == '__main__':
    create_default_users()
