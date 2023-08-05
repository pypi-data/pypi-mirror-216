import datetime
import mysql.connector

class SNIIM():

    def __init__(self, product, start_date, end_date):
        self.product = product
        self.start_date = start_date
        self.end_date   = end_date
        self.MYSQL_HOST = '18.215.228.120'
        self.MYSQL_USER = 'fcca_read_1'
        self.MYSQL_PASSW= 'fcca_read_1'
        self.MYSQL_PORT = 3011
        self.MYSQL_DB   = 'fcca_1'

    def get_data(self):
        start_date = self.start_date
        end_date   = self.end_date
        if self.product == 'granos':
            result = self.db_con('sniim_maiz_1', start_date, end_date)
        if self.product == 'fyh':
            result = self.db_con('sniim_frutas_hortalizas_1', start_date, end_date)
        return result

    def db_con(self, product, start_date, end_date):
        mydb = mysql.connector.connect(host=self.MYSQL_HOST, user=self.MYSQL_USER, password=self.MYSQL_PASSW, port=self.MYSQL_PORT, database=self.MYSQL_DB)
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM "+ str(product) + " WHERE fecha BETWEEN '" + str(start_date) + "' AND '" + str(end_date) + "' ")
        return mycursor.fetchall()
