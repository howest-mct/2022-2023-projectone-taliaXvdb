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
    
    def create_reading(deviceid, actionid, userid, date, value, comment):
        sql = "INSERT INTO history (deviceID, actionID, userID, date, value, comment) VALUES (%s,%s,%s,%s,%s,%s)"
        params = [deviceid, actionid, userid, date, value, comment]
        return Database.execute_sql(sql, params)
    
    #READ
    def read_all_users():
        sql = "SELECT * FROM user"
        return Database.get_rows(sql)
    
    def read_user(id):
        sql = "SELECT * FROM user WHERE userID = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    def read_reminders_by_userid(id):
        sql = "SELECT * FROM reminder WHERE iduser = %s"
        params = [id]
        return Database.get_rows(sql, params)
    
    def read_one_reminder(id):
        sql = "SELECT * FROM reminder WHERE reminderID = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    def read_all_reminders():
        sql = "SELECT * FROM reminder"
        return Database.get_rows(sql)
    
    def read_history_by_userid(id):
        sql = "SELECT * FROM history WHERE userID = %s"
        params = [id]
        return Database.get_rows(sql, params)
    
    def read_history():
        sql = "SELECT * FROM history"
        return Database.get_rows(sql)
    
    def read_lasttemp():
        sql = "SELECT value FROM history WHERE deviceID = 1 ORDER BY ID DESC LIMIT 1"
        return Database.get_one_row(sql)
    
    #UPDATE
    def update_user(id, name, goal, streak):
        sql = "UPDATE user SET name = %s, goal = %s, streak = %s  WHERE userID = %s"
        params = [name, goal, streak, id]
        return Database.execute_sql(sql, params)
    
    def update_reminder(id, iduser, type, time, amount, fasterWhenHot):
        sql = "UPDATE reminder SET iduser = %s, type = %s, time = %s, amount = %s, fasterWhenHot = %s WHERE reminderID = %s"
        params = [iduser, type, time, amount, fasterWhenHot, id]
        return Database.execute_sql(sql, params)
    
    #DELETE
    def delete_user(id):
        sql = "DELETE FROM user WHERE userID = %s"
        params = [id]
        return Database.execute_sql(sql, params)
    
    def delete_reminder(id):
        sql = "DELETE FROM reminder WHERE reminderID = %s"
        params = [id]
        return Database.execute_sql(sql, params)