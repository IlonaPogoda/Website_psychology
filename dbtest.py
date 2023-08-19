import sqlite3

class DataBase:
    def __init__(self):
        pass

    def connect(self):
     self.db = sqlite3.connect("C:/Users/Konstantin/PycharmProjects/pythonProject1/db/database.db")

    def addUser(self, user_data):
        self.connect()
        cursor = self.db.cursor()
        query = "INSERT INTO Users (name, surname, email, password) VALUES( '{name}', '{surname}', '{email}', '{password}')".format(
            name=user_data['name'],
            surname=user_data['surname'],
            email=user_data['email'],
            password=user_data['password']
        )
        cursor.execute(query)
        cursor.close()
        self.db.commit()
        self.disconnect()

    def checkUser(self, user_data):
        self.connect()
        cursor = self.db.cursor()
        query = "SELECT COUNT(*) FROM Users WHERE email='{email1}' AND password='{password1}'".format(
            email1=user_data['email'],
            password1=user_data['password']
        )
        cursor.execute(query)
        record = cursor.fetchone()
        cursor.close()
        print(record[0])
        self.disconnect()
        return record[0]

    def getFullUserData(self, user_data):
        self.connect()
        cursor = self.db.cursor()
        query = "SELECT * FROM Users WHERE email='{email}' AND password='{password}'".format(
            email=user_data['email'],
            password=user_data['password']
        )
        cursor.execute(query)
        record = cursor.fetchone()
        cursor.close()
        print(record)
        self.disconnect()
        return record

    def getDoctor(self, desc):
        self.connect()
        cursor = self.db.cursor()
        query = "SELECT * FROM Doctors WHERE direction='{dir}' AND gender='{gen}'".format(
            dir=desc['direction'],
            gen=desc['gender']
        )
        cursor.execute(query) #Выполняет запрос
        record = cursor.fetchone()
        cursor.close()
        print(record)
        self.disconnect()
        return record

    def addNote(self, note_data):
        self.connect()
        cursor = self.db.cursor()
        query = "INSERT INTO Notes (user_id, doctor_id, reason, date) VALUES( '{user_id}', '{doctor_id}', '{reason}', '{date}')".format(
            user_id=note_data['user_id'],
            doctor_id=note_data['doctor_id'],
            reason=note_data['reason'],
            date=note_data['date']
        )
        cursor.execute(query)
        cursor.close()
        self.db.commit()
        self.disconnect()

    def getUserNotes(self, user_id):
        self.connect()
        cursor = self.db.cursor()
        query = "SELECT * FROM Notes WHERE user_id='{user_id}'".format(
            user_id=user_id
        )
        cursor.execute(query)
        notes_records = cursor.fetchall()

        notes = []
        for note in notes_records:
            query = "SELECT * FROM Doctors WHERE doctor_id='{doc_id}'".format(
                doc_id=note[2]
            )
            cursor.execute(query)
            record_doctor = cursor.fetchone()
            notes.append(
                {
                    'doctor_fio': record_doctor[1] + ' ' + record_doctor[2] ,
                    'reason': note[3],
                    'date': note[4]
                }
            )
        cursor.close()
        print(notes)
        self.disconnect()
        return notes

    def disconnect(self):
        self.db.close()
