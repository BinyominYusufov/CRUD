import psycopg2

conn = psycopg2.connect(
        dbname='Product_db',
        user='postgres',
        password='admin2009',
        host='localhost',
        port='5432'
)

cursor = conn.cursor()





class Products:
    def __init__(self,prod_name,quantity,description,price,image):
        self.product_name = prod_name
        self.quantity = quantity
        self.description = description
        self.price = price,
        self.image = image

    @staticmethod
    def get_products():
        cursor.execute('select * from Products')
        data = cursor.fetchall()
        return data
    
    async def add_product(self):
        cursor.execute('insert into Products(prod_name,quantity,description,price,image) values (%s,%s,%s,%s,%s)',(self.product_name,self.quantity,self.description,self.price,self.image))
        data = cursor.fetchone()
        conn.commit()
        return data
    
    def delete_product(self):
        cursor.execute('delete from Products where id = %s')








