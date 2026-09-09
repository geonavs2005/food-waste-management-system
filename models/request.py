from database.db import query_db, execute_db

class FoodRequest:
    def __init__(self, request_id=None, recipient_id=None, food_category="", quantity_requested=0, priority=5, request_date=None, status="Pending"):
        self.request_id = request_id
        self.recipient_id = recipient_id
        self.food_category = food_category
        self.quantity_requested = quantity_requested
        self.priority = priority
        self.request_date = str(request_date) if request_date else None
        self.status = status

    def to_dict(self):
        return {
            'request_id': self.request_id,
            'recipient_id': self.recipient_id,
            'food_category': self.food_category,
            'quantity_requested': self.quantity_requested,
            'priority': self.priority,
            'request_date': str(self.request_date),
            'status': self.status
        }

    @staticmethod
    def get_all(status_filter=None):
        if status_filter:
            sql = """
            SELECT req.*, r.name AS recipient_name, r.organization AS recipient_org, r.location AS recipient_location
            FROM requests req
            JOIN recipients r ON req.recipient_id = r.recipient_id
            WHERE req.status = %s
            ORDER BY req.request_id ASC
            """
            rows = query_db(sql, (status_filter,))
        else:
            sql = """
            SELECT req.*, r.name AS recipient_name, r.organization AS recipient_org, r.location AS recipient_location
            FROM requests req
            JOIN recipients r ON req.recipient_id = r.recipient_id
            ORDER BY req.request_id ASC
            """
            rows = query_db(sql)
        for r in rows:
            if 'request_date' in r and r['request_date']:
                r['request_date'] = str(r['request_date'])
        return rows

    @staticmethod
    def get_by_id(request_id):
        sql = """
        SELECT req.*, r.name AS recipient_name, r.organization AS recipient_org, r.location AS recipient_location
        FROM requests req
        JOIN recipients r ON req.recipient_id = r.recipient_id
        WHERE req.request_id = %s
        """
        row = query_db(sql, (request_id,), one=True)
        if row and 'request_date' in row and row['request_date']:
            row['request_date'] = str(row['request_date'])
        return row

    @staticmethod
    def create(recipient_id, food_category, quantity_requested, priority=5):
        sql = """
        INSERT INTO requests (recipient_id, food_category, quantity_requested, priority, status) 
        VALUES (%s, %s, %s, %s, 'Pending')
        """
        return execute_db(sql, (recipient_id, food_category, quantity_requested, priority))

    @staticmethod
    def update_status(request_id, status):
        sql = "UPDATE requests SET status = %s WHERE request_id = %s"
        return execute_db(sql, (status, request_id))

    @staticmethod
    def delete(request_id):
        sql = "DELETE FROM requests WHERE request_id = %s"
        return execute_db(sql, (request_id,))
