import os
import sqlite3

class DbHeblper():
    def __init__(self):
        '''
        Some function for work with database

        '''
        self.this_dir = os.getcwd()
        self.filename_db = 'xmltv.db'
        self.columns_channels = ['cid', 'name', 'logo']
        self.columns_shows = ['cid', 'chanel_name', 'start', 'stop', 'duration', 'title', 'category', 'description']

    def create_table(self, tablename:str):
        columns = self.columns_channels if tablename == 'channels' else self.columns_shows

        conn = sqlite3.connect(self.filename_db)
        cursor = conn.cursor()
        columns_in_query = "("
        columns_in_query += ', '.join(columns)
        columns_in_query += ")"
        zapros = f"CREATE TABLE `{tablename}` {columns_in_query}"
        cursor.execute(zapros)
        conn.commit()
        cursor.close()

    def add_new_data(self, tablename:str, content:list):
        conn = sqlite3.connect(self.filename_db)
        cursor = conn.cursor()
        len_content = len(content)
        len_cols_in_content = len(content[0])
        signs_q = ['?'] * len_cols_in_content
        signs_for_query = "("
        signs_for_query += ', '.join(signs_q)
        signs_for_query += ")"
        for data in content:
            this_query = f"INSERT INTO {tablename} VALUES {signs_for_query}"
            cursor.execute(this_query, list(data.values()))
        conn.commit()

    def read_data_between(self, tablename:str, time_range:tuple):
        conn = sqlite3.connect(self.filename_db)
        cursor = conn.cursor()
        this_query = f"SELECT * FROM {tablename} WHERE `start` BETWEEN {str(time_range[0])} AND {str(time_range[1])}"
        cursor.execute(this_query)
        rows = cursor.fetchall()

        return rows