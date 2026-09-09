import datetime
from database.db import query_db, execute_db

class Food:
    def __init__(self, food_id=None, donor_id=None, food_name="", category="", quantity=0, expiry_date=None, location="", status="Available"):
        self.food_id = food_id
        self.donor_id = donor_id
        self.food_name = food_name
        self.category = category
        self.quantity = quantity
        self.expiry_date = str(expiry_date) if expiry_date else str(datetime.date.today())
        self.location = location
        self.status = status

    def to_dict(self):
        return {
            'food_id': self.food_id,
            'donor_id': self.donor_id,
            'food_name': self.food_name,
            'category': self.category,
            'quantity': self.quantity,
            'expiry_date': str(self.expiry_date),
            'location': self.location,
            'status': self.status
        }

    @staticmethod
    def get_all():
        sql = """
        SELECT f.*, d.name AS donor_name, d.organization AS donor_org 
        FROM food f 
        LEFT JOIN donors d ON f.donor_id = d.donor_id 
        ORDER BY f.food_id DESC
        """
        rows = query_db(sql)
        for r in rows:
            if 'expiry_date' in r and r['expiry_date']:
                r['expiry_date'] = str(r['expiry_date'])
        return rows

    @staticmethod
    def get_by_id(food_id):
        sql = """
        SELECT f.*, d.name AS donor_name, d.organization AS donor_org 
        FROM food f 
        LEFT JOIN donors d ON f.donor_id = d.donor_id 
        WHERE f.food_id = %s
        """
        row = query_db(sql, (food_id,), one=True)
        if row and 'expiry_date' in row and row['expiry_date']:
            row['expiry_date'] = str(row['expiry_date'])
        return row

    @staticmethod
    def create(donor_id, food_name, category, quantity, expiry_date, location, status="Available"):
        sql = """
        INSERT INTO food (donor_id, food_name, category, quantity, expiry_date, location, status) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return execute_db(sql, (donor_id, food_name, category, quantity, expiry_date, location, status))

    @staticmethod
    def update(food_id, donor_id, food_name, category, quantity, expiry_date, location, status):
        sql = """
        UPDATE food 
        SET donor_id = %s, food_name = %s, category = %s, quantity = %s, expiry_date = %s, location = %s, status = %s 
        WHERE food_id = %s
        """
        return execute_db(sql, (donor_id, food_name, category, quantity, expiry_date, location, status, food_id))

    @staticmethod
    def delete(food_id):
        sql = "DELETE FROM food WHERE food_id = %s"
        return execute_db(sql, (food_id,))
