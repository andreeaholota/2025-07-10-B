from database.DB_connect import DBConnect
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllCategories():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT category_id, category_name 
            FROM categories 
        """

        cursor.execute(query)
        for row in cursor:
            results.append((row["category_id"], row["category_name"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllProducts(category_id):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT *
            FROM products
            WHERE category_id = %s
        """

        cursor.execute(query, (category_id,))
        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getProductByOrder(category, dataI, dataF):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT v1.product_id AS v1, v2.product_id AS v2, (v1.peso + v2.peso) AS weight  
            FROM (SELECT p.product_id AS product_id, SUM(oi.quantity) AS peso 
                 FROM products p, order_items oi, orders o 
                 WHERE p.category_id = %s  
                    AND p.product_id = oi.product_id 
                    AND oi.order_id = o.order_id 
                    AND o.order_date BETWEEN %s AND %s  
                 GROUP BY p.product_id 
                 ORDER BY p.product_id) v1, 
                (SELECT p.product_id AS product_id, SUM(oi.quantity) AS peso 
                 FROM products p, order_items oi, orders o 
                 WHERE p.category_id = %s 
                    AND p.product_id = oi.product_id 
                    AND oi.order_id = o.order_id 
                    AND o.order_date BETWEEN %s AND %s 
                 GROUP BY p.product_id 
                 ORDER BY p.product_id) v2 
            WHERE v1.peso <= v2.peso 
                AND v1.product_id <> v2.product_id 
        """

        cursor.execute(query, (category, dataI, dataF, category, dataI, dataF))
        for row in cursor:
            results.append((row["v1"], row["v2"], row["weight"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last
