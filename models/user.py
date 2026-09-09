from database.db import query_db, execute_db
from models.donor import Donor
from models.recipient import Recipient

class User:
    def __init__(self, user_id=None, username="", password="", role="donor", name="", donor_id=None, recipient_id=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role
        self.name = name
        self.donor_id = donor_id
        self.recipient_id = recipient_id

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'role': self.role,
            'name': self.name,
            'donor_id': self.donor_id,
            'recipient_id': self.recipient_id
        }

    @staticmethod
    def get_by_username(username):
        sql = "SELECT * FROM users WHERE username = %s"
        return query_db(sql, (username.strip(),), one=True)

    @staticmethod
    def get_by_id(user_id):
        sql = "SELECT * FROM users WHERE user_id = %s"
        return query_db(sql, (user_id,), one=True)

    @staticmethod
    def create(username, password, role="donor", name="", donor_id=None, recipient_id=None):
        sql = """
        INSERT INTO users (username, password, role, name, donor_id, recipient_id) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        return execute_db(sql, (username.strip(), password, role, name, donor_id, recipient_id))

    @staticmethod
    def register_donor(username, password, name, contact, organization, location):
        """
        Registers a new donor: creates record in `donors` table first,
        then creates associated user in `users` table with role='donor'.
        """
        existing = User.get_by_username(username)
        if existing:
            return None, "Username already taken. Please choose another."

        donor_id = Donor.create(name, contact, organization, location)
        user_id = User.create(username, password, role="donor", name=name, donor_id=donor_id)
        return user_id, "Donor registration successful!"

    @staticmethod
    def register_recipient(username, password, name, organization, contact, location, priority=5):
        """
        Registers a new receiver: creates record in `recipients` table first,
        then creates associated user in `users` table with role='receiver'.
        """
        existing = User.get_by_username(username)
        if existing:
            return None, "Username already taken. Please choose another."

        rec_id = Recipient.create(name, organization, contact, location, priority)
        user_id = User.create(username, password, role="receiver", name=name, recipient_id=rec_id)
        return user_id, "Receiver registration successful!"
