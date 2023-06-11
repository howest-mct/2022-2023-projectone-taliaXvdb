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
    def create_user(id, name, goal, streak):
        sql = "INSERT INTO user (userID, name, goal, streak) VALUES (%s,%s,%s,%s)"
        params = [id, name, goal, streak]
        return Database.execute_sql(sql, params)
    
    def create_reminder(iduser, type, time, amount):
        sql = "INSERT INTO reminder (iduser, type, time, amount) VALUES (%s,%s,%s,%s)"
        params = [iduser, type, time, amount]
        return Database.execute_sql(sql, params)
    
    def create_reading(deviceid, actionid, userid, date, value, comment):
        sql = "INSERT INTO history (deviceID, actionID, userID, date, value, comment) VALUES (%s,%s,%s,%s,%s,%s)"
        params = [deviceid, actionid, userid, date, value, comment]
        return Database.execute_sql(sql, params)
    
    def create_logging(userid, time, amount, reached):
        sql = "INSERT INTO logging (usersID, loggingTime, loggingAmount, reached) VALUES (%s,%s,%s,%s)"
        params = [userid, time, amount, reached]
        return Database.execute_sql(sql,params)
    
    #READ
    def read_all_users():
        sql = "SELECT * FROM user"
        return Database.get_rows(sql)
    
    def read_user(id):
        sql = "SELECT * FROM user WHERE userID = %s"
        params = [id]
        return Database.get_one_row(sql, params)
    
    def read_goal_by_userid(id):
        sql = "SELECT goal FROM user WHERE userID = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    def read_reminders_by_userid(id):
        sql = "SELECT * FROM reminder WHERE iduser = %s"
        params = [id]
        return Database.get_rows(sql, params)
    
    def read_intervalreminder_by_userid(id):
        sql = "SELECT time FROM reminder WHERE iduser = %s"
        params = [id]
        return Database.get_rows(sql, params)        

    def read_remindertype_by_userid(id):
        sql = "SELECT type FROM reminder WHERE iduser = %s"
        params = [id]
        return Database.get_rows(sql, params)                        
    
    def read_one_reminder(id):
        sql = "SELECT * FROM reminder WHERE reminderID = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    def read_all_reminders():
        sql = "SELECT * FROM reminder"
        return Database.get_rows(sql)
    
    def read_reminder_types():
        sql = "SELECT name FROM type"
        return Database.get_rows(sql)
    
    def read_history_by_userid(id):
        sql = "SELECT h.*, a.description FROM history h JOIN action a ON a.actionID = h.actionID WHERE userID = %s"
        params = [id]
        return Database.get_rows(sql, params)
    
    def read_history():
        sql = "SELECT * FROM history"
        return Database.get_rows(sql)
    
    def read_lasttemp():
        sql = "SELECT value FROM history WHERE deviceID = 1 ORDER BY ID DESC LIMIT 1"
        return Database.get_one_row(sql)
    
    def read_lastweight():
        sql = "SELECT value FROM history WHERE deviceID = 2 ORDER BY ID DESC LIMIT 1"
        return Database.get_one_row(sql)
    
    def read_loggings():
        sql = "SELECT * FROM logging"
        return Database.get_rows(sql)
    
    def read_logging_by_userid(id):
        sql = "SELECT * FROM logging WHERE usersID = %s"
        params = [id]
        return Database.get_rows(sql,params)

    def read_lastlogging_by_userid(id):
        sql = "SELECT l.* FROM logging l JOIN (SELECT loggingDate, MAX(loggingTime) AS `last_time` FROM logging GROUP BY loggingDate) lt ON lt.loggingDate = l.loggingDate WHERE l.loggingDate = lt.loggingDate and l.loggingTime = lt.`last_time` HAVING l.usersID = %s;"
        params = [id]
        return Database.get_one_row(sql,params)
    
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