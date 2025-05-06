from app import app, db, Contact

# Sample data
dummy_contacts = [
    {
        'firstname': 'John',
        'lastname': 'Smith',
        'email': 'john.smith@example.com',
        'phone': '555-0101',
        'phone_type': 'mobile'
    },
    {
        'firstname': 'Sarah',
        'lastname': 'Johnson',
        'email': 'sarah.j@example.com',
        'phone': '555-0102',
        'phone_type': 'home'
    },
    {
        'firstname': 'Michael',
        'lastname': 'Brown',
        'email': 'michael.b@example.com',
        'phone': '555-0103',
        'phone_type': 'work'
    },
    {
        'firstname': 'Emily',
        'lastname': 'Davis',
        'email': 'emily.d@example.com',
        'phone': '555-0104',
        'phone_type': 'mobile'
    },
    {
        'firstname': 'David',
        'lastname': 'Wilson',
        'email': 'david.w@example.com',
        'phone': '555-0105',
        'phone_type': 'home'
    }
]

def seed_database():
    with app.app_context():
        # Clear existing data
        Contact.query.delete()
        
        # Add new contacts
        for contact_data in dummy_contacts:
            contact = Contact(**contact_data)
            db.session.add(contact)
        
        # Commit the changes
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database() 