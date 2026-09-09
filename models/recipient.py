from database.db import query_db, execute_db

class Recipient:
    def __init__(self, recipient_id=None, name="", organization="", contact="", location="", priority=5):
        self.recipient_id = recipient_id
        self.name = name
        self.organization = organization
        self.contact = contact
        self.location = location
        self.priority = priority

    def to_dict(self):
        return {
            'recipient_id': self.recipient_id,
            'name': self.name,
            'organization': self.organization,
            'contact': self.contact,
            'location': self.location,
            'priority': self.priority
        }

    @staticmethod
    def get_all():
        sql = """
        SELECT r.*, COUNT(req.request_id) AS total_requests 
        FROM recipients r 
        LEFT JOIN requests req ON r.recipient_id = req.recipient_id 
        GROUP BY r.recipient_id 
        ORDER BY r.priority DESC, r.recipient_id DESC
        """
        return query_db(sql)

    @staticmethod
    def get_by_id(recipient_id):
        sql = "SELECT * FROM recipients WHERE recipient_id = %s"
        return query_db(sql, (recipient_id,), one=True)

    @staticmethod
    def create(name, organization, contact, location, priority=5):
        sql = "INSERT INTO recipients (name, organization, contact, location, priority) VALUES (%s, %s, %s, %s, %s)"
        return execute_db(sql, (name, organization, contact, location, priority))

    @staticmethod
    def update(recipient_id, name, organization, contact, location, priority):
        sql = "UPDATE recipients SET name = %s, organization = %s, contact = %s, location = %s, priority = %s WHERE recipient_id = %s"
        return execute_db(sql, (name, organization, contact, location, priority, recipient_id))

    @staticmethod
    def delete(recipient_id):
        sql = "DELETE FROM recipients WHERE recipient_id = %s"
        return execute_db(sql, (recipient_id,))
