from app import create_app, db
from app.models.member import Member
from faker import Faker

fake = Faker()

app = create_app()

def seed_members():
    for _ in range(10):
        # Generate fake data for each member
        fake_member = Member(
            name=fake.name(),
            phone=fake.phone_number(),
            email=fake.email(),
            role=fake.random_element(elements=("member", "admin", "supervisor")),
            is_active=True
        )
        fake_member.set_password('password123')
        db.session.add(fake_member)
    db.session.commit()


    # Create tables and seed data
with app.app_context():
    db.create_all()  # Ensure all tables are created before seeding
    seed_members()  # Seed the database with members
    print("Fake member data seeded successfully!")