class AccountModel:
    #The account model. Connects to the database to add, edit or get data from accounts.

    def add_account(name, username, password, email, confirm_key):
        query="insert into account (name, username, password, email, confirm_key) values (%s, %s, %s, %s, %s);"
        data=(name, username, password, email, confirm_key)
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        userdata=cursor.fetchone()
        conn.close()
        cursor.close()
        add_person(userdata[0], name)
        pass

    def get_account(email, password):
        query="select * from account where email=%s and password=%s"
        data=(email, password)
        conn=mysql.connect()
        cursor=conn.cursor()
        if cursor.execute(query, data)>0:
            userdata=cursor.fetchone()
            conn.close()
            cursor.close()
            return userdata
        conn.close()
        cursor.close()
        pass

    def get_account(email, username):
        query="select * from account where email=%s and username=%s"
        data=(email, uname)
        conn=mysql.connect()
        cursor=conn.cursor()
        if cursor.execute(query, data)>0:
            userdata=cursor.fetchone()
            conn.close()
            cursor.close()
            return userdata
        conn.close()
        cursor.close()
        pass

    def get_account(ide):
        query="select * from account where id=%s;"
        data=(ide)
        conn=mysql.connect()
        cursor=conn.cursor()
        if cursor.execute(query, data)>0:
            userdata=cursor.fetchone()
            conn.close()
            cursor.close()
            return userdata
        conn.close()
        cursor.close()
        pass

    def update_account(name, username, password, email, ide):
        query="update account set name=%s, username=%s, password=%s, email=%s where id=%s;"
        data=(username, password, email, ide)
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        userdata=cursor.fetchone()
        conn.close()
        cursor.close()
        return userdata

    def update_account(name, username, email, ide):
        query="update account set name=%s, username=%s, email=%s where id=%s;"
        data=(username, email, ide)
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        userdata=cursor.fetchone()
        conn.close()
        cursor.close()
        return userdata

    def get_persons(ide):
        query="select * from person where account_id=%s;"
        data=(ide)
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        userdata=cursor.fetchall()
        conn.close()
        cursor.close()
        return userdata

    def add_person(ide, name):
        query="insert into person (account_id, name) values (%s, %s);"
        data=(ide, name)
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        conn.close()
        cursor.close()
        pass

    def delete_person(ide, name):
        query="delete from person where account_id=%s and name=%s"
        data=(ide, name)
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        conn.close()
        cursor.close()
        pass
