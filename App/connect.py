#!/usr/bin/env python
import os
import sys
import MySQLdb

class Database:
    def __init__(self):
        self.car_db = MySQLdb.connect(user="root", host="127.0.0.1", db="car", passwd="tkachvova2468", port=4040)
        self.cursor = self.car_db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor_returns_list = self.car_db.cursor()

    def drop_tables(self):
        self.cursor.execute('SET AUTOCOMMIT = 0; DELETE FROM engine1 where id > 0; COMMIT;')
        self.cursor.execute('SET AUTOCOMMIT = 0; DELETE FROM interior where id > 0; COMMIT;')
        self.cursor.execute('SET AUTOCOMMIT = 0; DELETE FROM body where id > 0; COMMIT;')
        self.cursor.execute('SET AUTOCOMMIT = 0; DELETE FROM car where id > 0; COMMIT;')
        self.car_db.commit()

    def load_xml_data(self):
        self.cursor.execute('DELETE FROM engine1 where id > 0;')
        self.cursor.execute('DELETE FROM interior where id > 0;')
        self.cursor.execute('DELETE FROM body where id > 0;')
        self.cursor.execute('DELETE FROM car where id > 0;')
        print(0)
        self.cursor.execute("""LOAD XML LOCAL INFILE "body.xml" REPLACE INTO TABLE body
                               ROWS IDENTIFIED BY "<body>";""")
        print(1)
        self.cursor.execute("""LOAD XML LOCAL INFILE "engine.xml"
                               REPLACE INTO TABLE engine1 ROWS IDENTIFIED BY "<engine1>";""")
        print(2)
        self.cursor.execute("""LOAD XML LOCAL INFILE "interior.xml" REPLACE INTO TABLE interior
                               ROWS IDENTIFIED BY "<interior>";""")
        print(3)
        self.cursor.execute("""LOAD XML LOCAL INFILE "car.xml"
                                REPLACE INTO TABLE car ROWS IDENTIFIED BY "<car>";""")
        self.car_db.commit()
        print(4)

    def car_insert(self, producer_, model_, car_class_, drive_, engine, interior, body, cost_):
        self.cursor.execute("INSERT INTO car(producer, model, class, drive, engine_id, interior_id, body_id, cost)"
                            "VALUES('%s','%s','%s','%s',%s,%s,%s,%s);" %
                            (str(producer_), str(model_), str(car_class_), str(drive_), int(engine), int(interior),
                             int(body), int(cost_)))
        self.car_db.commit()


    def car_edit(self, pk, producer_, model_, car_class_, drive_, engine, interior, body, cost_):
        self.cursor.execute("""UPDATE car SET producer = '%s', model = '%s', class = '%s', drive = '%s', engine_id = %s,
                              interior_id = %s, body_id= %s, cost = %s WHERE id = %s;""" % (str(producer_), str(model_),
                                    str(car_class_), str(drive_), int(engine), int(interior), int(body), int(cost_),
                                    int(pk)))
        self.car_db.commit()

    def get_car_instance(self, pk):
        self.cursor.execute("""SELECT producer, model, class as car_class, drive, engine_id as engine,
                                interior_id as interior, body_id as body, cost FROM car WHERE id = %s;""" % pk)
        return self.cursor.fetchone()


    def formDataSearch(self, cost, hpower, interior, doors):
        sql_querry = ''
        sql_querry += """SELECT car.id, car.producer, car.model, car.class as car_class, car.drive, car.cost FROM car
                         JOIN engine1 engine ON car.engine_id = engine.id JOIN body ON car.body_id = body.id
                         JOIN interior ON car.interior_id = interior.id """
        if cost != '-' or hpower != '-' or interior != '-' or doors != '-':
            sql_querry += "WHERE ( "
            if cost == 'less':
                sql_querry += "car.cost < 30000 "
            if cost == 'from':
                sql_querry += "car.cost between 30000 and 60000 "
            if cost == 'more':
                sql_querry += "car.cost > 60000 "
            if cost != '-' and hpower != '-':
                sql_querry += "AND "
            if hpower == 'less':
                sql_querry += "engine.hpower < 150 "
            if hpower == 'from':
                sql_querry += "engine.hpower between 150 and 300 "
            if hpower == 'more':
                sql_querry += "engine.hpower > 300 "
            if (cost != '-' or hpower != '-') and interior != '-':
                sql_querry += "AND "
            if interior == 'leather':
                sql_querry += "interior.material = 'leather' "
            if interior == 'textile':
                sql_querry += "interior.material ='textile' "
            if (cost != '-' or hpower != '-' or interior != '-') and doors != '-':
                sql_querry += 'AND '
            if doors == 'less':
                sql_querry += "body.amount_of_doors < 3 "
            if doors == 'from':
                sql_querry += "body.amount_of_doors between 3 and 5 "
            if doors == 'more':
                sql_querry += "body.amount_of_doors > 5"
            sql_querry += ");"
            print(sql_querry)
        self.cursor.execute(sql_querry)
        return self.cursor.fetchall()



    def car_delete(self, pks):
        for a in pks:
            self.cursor.execute("DELETE FROM car WHERE id=%s;" % a)
        self.car_db.commit()

    def engine_choices(self):
        self.cursor_returns_list.execute("""SELECT id, hpower, torgue, volume, amount_of_cylynders,
                                          fuel_type,fuel_consumption FROM engine1;""")
        list = self.cursor_returns_list.fetchall()
        dict = []
        for a in list:
            d = []
            d.append(a[0])
            d.append("hp = " + str(a[1]) + "; torgue = " + str(a[2]) + "; volume = " + str(a[3])
                     + "; amount of cylynders = " + str(a[4]) + "; fuel type = " + str(a[5]) + "; fuel consumption = "
                        +str(a[6]))
            dict.append(d)
        return dict

    def interior_choices(self):
        self.cursor_returns_list.execute("""SELECT id, material, color, amount_of_seats from interior;""")
        list = self.cursor_returns_list.fetchall()
        dict = []
        for a in list:
            d = []
            d.append(a[0])
            d.append("material = " + str(a[1]) + "; color = " + str(a[2]) + "; amount of seats = " + str(a[3]))
            dict.append(d)
        return dict

    def body_choices(self):
        self.cursor_returns_list.execute("""SELECT id, length, width, amount_of_doors, volume_of_boot from body;""")
        list = self.cursor_returns_list.fetchall()
        dict = []
        for a in list:
            d = []
            d.append(a[0])
            d.append("length = " + str(a[1]) + "; width = " + str(a[2]) + "; amount of doors = " + str(a[3])
                     + "; volume of boot = " + str(a[4]))
            dict.append(d)
        return dict



    def get_all_from_car(self):
        self.cursor.execute('SELECT id, producer, model, class as car_class, drive, cost FROM car;')
        return self.cursor.fetchall()

    def get_all_from_engine(self):
        self.cursor_returns_list.execute('SELECT id, hpower FROM engine1')
        return self.cursor_returns_list.fetchall()

    def get_all_from_interior(self):
        self.cursor_returns_list.execute('SELECT id, material FROM interior')
        return self.cursor_returns_list.fetchall()

    def get_all_from_body(self):
        self.cursor_returns_list.execute('SELECT id, length FROM body')
        return self.cursor_returns_list.fetchall()