from database.db import query_db, execute_db

class Donor:
    def __init__(self, donor_id=None, name="", contact="", organization="", location=""):
        self.donor_id = donor_id
        self.name = name
        self.contact = contact
        self.organization = organization
        self.location = location

    def to_dict(self):
        return {
            'donor_id': self.donor_id,
            'name': self.name,
            'contact': self.contact,
            'organization': self.organization,
            'location': self.location
        }

    @staticmethod
    def get_all():
        sql = """
        SELECT d.*, COUNT(f.food_id) AS donation_count, COALESCE(SUM(f.quantity), 0) AS total_quantity 
        FROM donors d 
        LEFT JOIN food f ON d.donor_id = f.donor_id 
        GROUP BY d.donor_id 
        ORDER BY d.donor_id DESC
        """
        return query_db(sql)

    @staticmethod
    def get_by_id(donor_id):
        sql = "SELECT * FROM donors WHERE donor_id = %s"
        return query_db(sql, (donor_id,), one=True)

    @staticmethod
    def create(name, contact, organization, location):
        sql = "INSERT INTO donors (name, contact, organization, location) VALUES (%s, %s, %s, %s)"
        return execute_db(sql, (name, contact, organization, location))

    @staticmethod
    def update(donor_id, name, contact, organization, location):
        sql = "UPDATE donors SET name = %s, contact = %s, organization = %s, location = %s WHERE donor_id = %s"
        return execute_db(sql, (name, contact, organization, location, donor_id))

    @staticmethod
    def delete(donor_id):
        sql = "DELETE FROM donors WHERE donor_id = %s"
        return execute_db(sql, (donor_id,))
