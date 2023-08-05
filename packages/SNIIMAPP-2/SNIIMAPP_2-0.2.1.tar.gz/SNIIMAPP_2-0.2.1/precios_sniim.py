import datetime
import mysql.connector
import argparse
import csv

class Sniim():

    def __init__(self, product, start_date, end_date):
        self.product = product
        self.start_date = start_date
        self.end_date   = end_date
        self.MYSQL_HOST = '18.215.228.120'
        self.MYSQL_USER = 'fcca_read_1'
        self.MYSQL_PASSW= 'fcca_read_1'
        self.MYSQL_PORT = 3011
        self.MYSQL_DB   = 'fcca_1'

    '''
    def parse_args():
        parser = argparse.ArgumentParser(description = 'Libreria para consulta de precios de productos agriculas FCCA UMICH V.1.1')
        parser.add_argument('product',    help='Producto [fyh: frutas y hortalizas, granos: granos]', choices=['fyh', 'granos'])
        parser.add_argument('start_date', help='Fecha inicio [YYYY-mm-dd]')
        parser.add_argument('end_date',   help='Fecha fin [YYYY-mm-dd]')
        args = parser.parse_args()
        return args

    def main():
        inputs = parse_args()
        db_con(inputs)
    '''

    def get_data(self):
        start_date = self.start_date
        end_date   = self.end_date
        if self.product == 'granos':
            return get_data('granos', 'sniim_maiz_1', start_date, end_date)
        if self.product == 'fyh':
            return get_data('fyh', 'sniim_frutas_hortalizas_1', start_date, end_date)

    def db_con(file_name, product, start_date, end_date):
        mydb = mysql.connector.connect(host=self.MYSQL_HOST, user=self.MYSQL_USER, password=self.MYSQL_PASSW, port=self.MYSQL_PORT, database=self.MYSQL_DB)
        mycursor = mydb.cursor(dictionary=True)
        #mycursor.execute("SELECT * FROM "+ str(product) + " WHERE (STR_TO_DATE(fecha, '%d/%m/%Y') BETWEEN '" + str(start_date) + "' AND '" + str(end_date) + "') ")
        mycursor.execute("SELECT * FROM "+ str(product) + " WHERE fecha BETWEEN '" + str(start_date) + "' AND '" + str(end_date) + "' ")
        return mycursor.fetchall()

