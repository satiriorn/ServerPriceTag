import mysql.connector, os, json

class DataBase:
    def __init__(self):
        self.cursor, self.db = None, None

    def GetValue(self):
        value = None
        for x in self.cursor:
            value = x
        return value

    def GetCursor(self):
        if self.cursor and self.db:
            self.cursor.close()
            self.db.close()
        self.db = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database="heroku_944d93c1a0e7204"
        )
        self.cursor = self.db.cursor(buffered=True)
        sql = "SET @@auto_increment_increment=1;"
        self.cursor.execute(sql)
        return self.cursor

    def GetData(self, id):
        sql = """SELECT Description, Title, Price, SalePrice, Sale, Measurement FROM heroku_944d93c1a0e7204.PriceTag WHERE id_Tag="{0}";""".format(id)
        self.GetCursor()
        self.cursor.execute(sql)
        return self.GetValue()