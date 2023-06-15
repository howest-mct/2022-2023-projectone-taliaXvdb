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
    
    def create_logging(userid, date, time, amount, reached):
        sql = "INSERT INTO logging (usersID, loggingDate, loggingTime, loggingAmount, reached) VALUES (%s,%s,%s,%s,%s)"
        params = [userid, date, time, amount, reached]
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
        sql = "SELECT time FROM reminder WHERE iduser = %s and amount != 0"
        params = [id]
        return Database.get_rows(sql, params)        

    def read_remindertype_by_userid(id):
        sql = "SELECT type FROM reminder WHERE iduser = %s and amount != 0"
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
    
    def read_temperature(id):
        sql = "SELECT date_format(date, '%Y-%m-%d') AS `Date`, date_format(date, '%H:%i') AS `Time`, value FROM history WHERE deviceID = 1 and userID = %s and date >= CURDATE()   AND date < CURDATE() + INTERVAL 1 DAY"
        params = [id]
        return Database.get_rows(sql,params)
    
    def read_weight(id):
        sql = "SELECT date_format(date, '%Y-%m-%d') AS `Date`, date_format(date, '%H:%i') AS `Time`, value FROM history WHERE deviceID = 2 and userID = %s and date >= CURDATE()   AND date < CURDATE() + INTERVAL 1 DAY;"
        params = [id]
        return Database.get_rows(sql,params)

    def read_lastlogging_by_userid(id):
        sql = "select u.name, u.goal as 'daily goal', DATE_FORMAT(h.date,'%d-%m-%y') as date, sum(h.value) as 'total weight water', if(u.goal <= sum(h.value), 'Yes', 'No') as 'Goal reached?' from user u join history h on u.userID = h.userID where u.userid = %s and h.deviceID = 2 GROUP BY year(h.date), month(h.date), day(h.date)"
        params = [id]
        return Database.get_rows(sql,params)
    
    def read_loggedwater_by_userid(id):
        sql = "SELECT date_format(loggingDate, '%Y-%m-%d') AS `date`, sum(loggingAmount) AS `total` from logging where usersID = %s and date_format(loggingDate, '%Y-%m-%d') >= CURDATE() AND date_format(loggingDate, '%Y-%m-%d') < CURDATE() + INTERVAL 1 DAY;"
        params = [id]
        return Database.get_rows(sql,params)

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