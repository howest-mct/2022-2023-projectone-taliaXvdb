from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.method != 'GET' and request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    #CREATE
    @staticmethod
    def create_user(name, goal, streak):
        sql = "INSERT INTO user (name, goal, streak) VALUES (%s,%s,%s)"
        params = [name, goal, streak]
        return Database.execute_sql(sql, params)
    
    def create_reminder(iduser, type, time, amount, fasterWhenHot):
        sql = "INSERT INTO reminder (iduser, type, time, amount, fasterWhenHot) VALUES (%s,%s,%s,%s,%s)"
        params = [iduser, type, time, amount, fasterWhenHot]
        return Database.execute_sql(sql, params)
    
    #READ
    def read_all_users():
        sql = "SELECT * FROM user"
        return Database.get_rows(sql)
    
    def read_user(id):
        sql = "SELECT * FROM user WHERE userID = %s"
        params = [id]
        return Database.get_one_row(sql, params)
    
    def read_history_by_userid(id):
        sql = "SELECT * FROM history WHERE userID = %s"
        params = [id]
        return Database.get_rows(sql, params)
    
    def read_history():
        sql = "SELECT * FROM history"
        return Database.get_rows(sql)