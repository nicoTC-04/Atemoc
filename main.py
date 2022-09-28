import mysql.connector
from datetime import date
from datetime import timedelta

from kivy.app import App
from kivy.config import Config
from kivy.uix.label import Label

Config.set('graphics', 'Resizable', '0')
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '740')

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.graphics import Ellipse, Color, Rectangle
from kivy.vector import Vector

from random import random
from math import atan2, sqrt, pow, degrees, sin, cos, radians

user = "Sin asignar"
sm = ""
shower = 0
washingMach = 0
toilet = 0
watering = 0

def readRecord(currDate, usern):
    try:
        #search for userId
        query = ("SELECT `id` FROM `users` WHERE `username`='%s';" % (usern))
        
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query)
        
        result = cursor.fetchall()
        
        for i in result:
            userId = i[0]
        
        #records between dates
        today = date.today()
        dayNum = today.weekday()
        
        beginCurrWeek = today - timedelta(days = dayNum)
        endLastWeek = today - timedelta(days = (dayNum+1))
        beginLastWeek = today - timedelta(days = (dayNum+8))
        
        if(currDate):
            #this weeks records
            query = ("SELECT `superString` FROM `records` WHERE `userId`='%s' AND (`date` BETWEEN '%s' AND '%s');" % (userId, beginCurrWeek, today))
        else:
            #last weeks records
            query = ("SELECT `superString` FROM `records` WHERE `userId`='%s' AND (`date` BETWEEN '%s' AND '%s');" % (userId, beginLastWeek, endLastWeek))
        
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query)
        
        showerTotal = 0
        washingMachTotal = 0
        toiletTotal = 0
        wateringTotal = 0
        
        result = cursor.fetchall()
        
        for i in result:
            superStr = i[0]
            divSuperStr = superStr.split(";")

            #add total water litres spent per record by the shower
            showerInfo = divSuperStr[0].split(",")
            shPressure = showerInfo[0][showerInfo[0].index("=")+1:]

            shTime = int(showerInfo[1][showerInfo[1].index("=")+1:])

            if(shPressure=="high"):
                showerTotal+=(shTime*20)
            elif(shPressure=="medium"):
                showerTotal+=(shTime*16)
            else:
                showerTotal+=(shTime*12)

            #add total water litres spent per record by the washing machine
            washingMachInfo = divSuperStr[1].split(",")
            wmLoad = int(washingMachInfo[0][washingMachInfo[0].index("=")+1:])
            wmTimes = int(washingMachInfo[1][washingMachInfo[1].index("=")+1:])

            if(wmLoad==5):
                washingMachTotal += 45.5*wmTimes
            else:
                washingMachTotal += 52*wmTimes

            #add total water litres spent per record by the toilet    
            toiletInfo = divSuperStr[2].split("=")
            toiletTimes = int(toiletInfo[1])
            toiletTotal += toiletTimes*7.8

            #add total water litres spent per record by watering
            wateringInfo = divSuperStr[3].split(",")
            watPressure = wateringInfo[0][wateringInfo[0].index("=")+1:]
            watTime = int(wateringInfo[1][wateringInfo[1].index("=")+1:])

            if(watPressure=="high"):
                wateringTotal+=(watTime*12)
            elif(watPressure=="medium"):
                wateringTotal+=(watTime*7)
            else:
                wateringTotal+=(watTime*4)
                
        close_connection(connection)
        
        return showerTotal, washingMachTotal, toiletTotal, wateringTotal
    
    except (Exception, mysql.connector.Error) as error:
        print("Error while getting data", error)

# connect to db
def connect():
    connection = mysql.connector.connect(host='XXXXXXXXX',
                                         database='XXXXXXXXX',
                                         user='XXXXXXXX',
                                         password='XXXXXXXXX')
    return connection


# close connection to db
def close_connection(connection):
    if connection:
        connection.close()


##Users
# insert new user to users table
def insert_user(name, last, usern, passc):
    try:
        # search for max current id
        query = ("SELECT MAX(`id`) FROM `users`;")

        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query)

        result = cursor.fetchall()

        for i in result:
            maxId = i[0]

        maxId += 1

        userTpl = (name, last, usern, passc)
        my_list = list(userTpl)
        my_list.insert(0, maxId)

        goodTuple = tuple(my_list)

        # add new user with parameters and maxId
        query = ("INSERT INTO `users` VALUES ('%s', '%s', '%s', '%s', '%s');" % goodTuple)

        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query)

        connection.commit()

        close_connection(connection)
    except (Exception, mysql.connector.Error) as error:
        print("Error while getting data", error)

def addRecord(usern, shPress, shTime, wmLoad, wmTimes, toTimes, waPress, waTime):
    try:
        # search for userId
        query = ("SELECT `id` FROM `users` WHERE `username`='%s';" % (usern))

        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query)

        result = cursor.fetchall()

        for i in result:
            user_id = i[0]

        # search for current max recordId
        query = ("SELECT MAX(`recordId`) FROM `records`")

        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query)

        result = cursor.fetchall()

        for j in result:
            maxRecordId = j[0]

        maxRecordId += 1

        # get current date
        currDate = date.today()

        # create new superString to insert into DBtable
        superStr = "Shower:pressure=" + shPress + ",time=" + str(shTime) + ";WashingMachine:load=" + str(
            wmLoad) + ",times=" + str(wmTimes) + ";Toilet:times=" + str(
            toTimes) + ";Watering:pressure=" + waPress + ",time=" + str(waTime)

        userTpl = ()
        my_list = list(userTpl)
        my_list.insert(0, superStr)
        my_list.insert(0, currDate)
        my_list.insert(0, maxRecordId)
        my_list.insert(0, user_id)

        goodTuple = tuple(my_list)

        # add new user with parameters and maxId
        query = ("INSERT INTO `records` VALUES ('%s', '%s', '%s', '%s');" % goodTuple)

        print(query)

        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query)

        connection.commit()

        close_connection(connection)
    except (Exception, mysql.connector.Error) as error:
        print("Error while getting data", error)


# check if the username and passcode match any existing user
def check_user(usern, passc):
    try:
        query = ("SELECT `id` FROM `users` WHERE `username`='%s' AND `passcode`='%s';" % (usern, passc))

        flag = False

        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query)

        for (id) in cursor:
            if (id != None):
                flag = True

        close_connection(connection)

        return flag

    except (Exception, mysql.connector.Error) as error:
        print("Error while getting data", error)


class MainWindow(BoxLayout):

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        showerTotal, laundryTotal, toiletTotal, wateringTotal = readRecord(False, 'CarlosMtz')
        
        
        # in_data can take form of either formats below
        
        # in_data = {"Opera": 350,
        #            "Steam": 234,
        #            "Overwatch": 532,
        #            "PyCharm": 485,
        #            "YouTube": 221}

        in_data = {"Shower": (showerTotal, [.1, .1, .4, 1]),
                   "Laundry": (laundryTotal, [.1, .7, .3, 1]),
                   "Toilet flushes": (toiletTotal, [.9, .1, .1, 1]),
                   "Irrigation": (wateringTotal, [.8, .7, .1, 1]),
        }
        
        position = (100, 200)
        size = (250, 300)
        
        
        chart = PieChart(data=in_data, position=position, size=size, legend_enable=True)
        self.add_widget(chart)


class PieChart(FloatLayout):
    def __init__(self, data, position, size, legend_enable=True, **kwargs):
        super(PieChart, self).__init__(**kwargs)

        # main layout parameters
        self.position = position
        self.size_mine = size

        self.data = {}
        
        self.size_hint_y = None
        self.size = (100, 250)
        self.temp = []

        for key, value in data.items():
            if type(value) is int:
                percentage = (value / float(sum(data.values())) * 100)
                color = [random(), random(), random(), 1]
                self.data[key] = [value, percentage, color]

            elif type(value) is tuple:
                vals = []
                for l in data.values():
                    vals.append(l[0])
                percentage = (value[0] / float(sum(vals)) * 100)
                color = value[1]
                self.data[key] = [value[0], percentage, color]

        self.pie = Pie(self.data, self.position, self.size_mine)
        self.add_widget(self.pie)

        if legend_enable:
            self.legend = LegendTree(self.data, self.position, self.size_mine)
            self.add_widget(self.legend)

        self.bind(size=self._update_pie, pos=self._update_pie)

        # yellow background to check widgets size and position
        # with self.canvas:
        #    Rectangle(pos=self.pos, size=self.size, color=Color(1, 1, 0, 0.5))

    def _update_pie(self, instance, value):
        self.legend.pos = (instance.parent.pos[0], instance.parent.pos[1])
        self.pie.pos = (instance.pos[0], instance.pos[1])


class LegendTree(GridLayout):
    def __init__(self, data, position, size, **kwargs):
        super(LegendTree, self).__init__(**kwargs)

        # Legend layout parameters.
        # Initial rows is 1, then for each next data entry new one is added.
        self.cols = 1
        self.rows = 1
        self.position = position
        self.size = size
        self.row_default_height = 60
        self.spacing = 5

        count = 0
        for key, value in data.items():
            percentage = value[1]
            color = value[2]
            # add legend (rectangle and text)
            self.legend = Legend(pos=(self.position[0], self.position[1] - count * self.size[1] * 0.15),
                                 size=self.size,
                                 color=color,
                                 name=key,
                                 value=percentage)
            self.add_widget(self.legend)
            self.rows += 1
            count += 1

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.legend.pos = (instance.parent.pos[0], instance.parent.pos[1])
        self.pos = (instance.parent.pos[0] + 260, instance.parent.pos[1])


# Class for creating Legend
class Legend(FloatLayout):
    def __init__(self, pos, size, color, name, value, **kwargs):
        super(Legend, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 1
        self.size_hint_x = 200
        self.size_hint_y = 50
        self.name = name
        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle(pos=(pos[0] + size[0] * 1.3, pos[1] + size[1] * 0.9),
                                  size=(size[0] * 0.1, size[1] * 0.1))
            self.label = Label(text=str("%.2f" % value + "%\n  -  " + name),
                               pos=(pos[0] + size[0] * 1.3 + size[0]*0.5, pos[1] + size[1] * 0.9 - 30),
                               halign='left',
                               text_size=(size[1], size[1] * 0.1))

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = (instance.pos[0] + 100, instance.pos[1] + 100)
        self.label.pos = (instance.pos[0] + 220, instance.pos[1] + 65)


class Pie(FloatLayout):
    def __init__(self, data, position, size, **kwargs):
        super(Pie, self).__init__(**kwargs)
        self.position = position
        self.size = size
        angle_start = 0
        count = 0
        self.temp = []
        for key, value in data.items():
            percentage = value[1]
            angle_end = angle_start + 3.6 * percentage
            color = value[2]
            # add part of Pie
            self.temp.append(PieSlice(pos=self.position, size=self.size,
                                      angle_start=angle_start,
                                      angle_end=angle_end, color=color, name=key))
            self.add_widget(self.temp[count])
            angle_start = angle_end
            count += 1
        self.bind(size=self._update_temp, pos=self._update_temp)

    def _update_temp(self, instance, value):
        for i in self.temp:
            i.pos = (instance.parent.pos[0] + 55, instance.parent.pos[1] + 60)


# Class for making one part of Pie
# Main functions for handling move out/in and click inside area recognition
class PieSlice(FloatLayout):
    def __init__(self, pos, color, size, angle_start, angle_end, name, **kwargs):
        super(PieSlice, self).__init__(**kwargs)
        self.moved = False
        self.angle = 0
        self.name = name
        with self.canvas.before:
            Color(*color)
            self.slice = Ellipse(pos=pos, size=size,
                                 angle_start=angle_start,
                                 angle_end=angle_end)
        self.bind(size=self._update_slice, pos=self._update_slice)

    def _update_slice(self, instance, value):
        self.slice.pos = (instance.pos[0], instance.pos[1])

class Login(Screen):
    pass


class RegisterUser(Screen):
    pass


class Home(Screen):
    showerTotal, laundryTotal, toiletTotal, wateringTotal = readRecord(True, 'CarlosMtz')
    totalwater = "Total consumption: " + str(showerTotal + laundryTotal + toiletTotal + wateringTotal)
    pass


class Help(Screen):
    pass

class Optimization(Screen):
    showerValue = "Hola"
    laundryValue = "Hola"
    toiletValue = "Hola"
    irrigationValue = "Hola" 

    def __init__(self, **kwargs):
        super(Optimization, self).__init__(**kwargs)
        shower, washingMach, toilet, watering = readRecord(False,"CarlosMtz")
        self.showerValue = ("      "+str(round(shower,2)) + " L / 448 L \n (Weekly usage / recommended weekly usage)")
        self.laundryValue = ("      "+str(round(washingMach,2)) + " L / 156 L \n (Weekly usage / recommended weekly usage)")
        self.toiletValue = ("      "+str(round(toilet,2)) + " L / 62.4 L \n (Weekly usage / recommended weekly usage)")
        self.irrigationValue = ("      "+str(round(watering,2)) + " L / 300 L \n (Weekly usage / recommended weekly usage)")

class History(Screen):
    pass


class ScreenManagement(ScreenManager):
    pass


class FloatLayoutEx(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.userIn = TextInput(size_hint=(None, None), size=("200dp", "40dp"), multiline=False,
                                pos_hint={"center_x": .5, "y": .6})
        self.passwordIn = TextInput(size_hint=(None, None), size=("200dp", "40dp"), multiline=False,
                                    pos_hint={"center_x": .5, "y": .4})

        self.error = ""

        self.add_widget(self.userIn)
        self.add_widget(self.passwordIn)

    def login_button(self):
        global user

        if check_user(self.userIn.text, self.passwordIn.text):
            global sm
            user = self.userIn.text
            sm = self.parent.parent
            sm.switch_to(sm.ids.home_screen)
            print(user)
        else:
            self.ids.error_label.text = "Invalid user or password"

        print(user)


class NewUser(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label_warning = ""

    def newuser_button(self):
        name = self.ids.name_field.text
        last_name = self.ids.last_name_field.text
        user_name = self.ids.user_name_field.text
        password = self.ids.password_field.text
        global sm
        if name and last_name and user_name and password and not sm:
            sm = self.parent
            insert_user(name, last_name, user_name, password)
            sm.switch_to(sm.ids.home_screen)
        else:
            self.ids.warning_label.text = "Warning, one or more fields were not filled."

        """
        if self.user_name.text and self.user_lastname.text and self.user_name and self.new_password:
            insert_user(self.user_name.text, self.user_lastname.text, self.username, self.new_password)
            sm.switch_to(sm.ids.home_screen)
        else:
            #print("User name:", temp)
            print("Last name:", self.user_lastname.text)
            print("Username:", self.username.text)

            self.ids.warning_label.text = "Warning, one or more fields were not filled."
            print(self.label_warning)
            """


class BottomBar(FloatLayout):
    pass
        


class TopBar(FloatLayout):
    pass


class BothBars(FloatLayout):
    pass


class Register(Screen):
    shower_pressure = False
    laundry_weight = False
    watering_pressure = False

    numshower = StringProperty("0")
    countershower = 0

    def counter_showerplus(self):
        self.countershower = self.countershower + 5
        self.numshower = str(self.countershower)

    def counter_showerminus(self):
        if self.countershower > 0:
            self.countershower = self.countershower - 5
            self.numshower = str(self.countershower)

        else:
            pass

    numwash = StringProperty("0")
    counterwash = 0

    def counter_washplus(self):
        self.counterwash = self.counterwash + 1
        self.numwash = str(self.counterwash)

    def counter_washminus(self):
        if self.counterwash > 0:
            self.counterwash = self.counterwash - 1
            self.numwash = str(self.counterwash)

        else:
            pass

    numtoilet = StringProperty("0")
    countertoilet = 0

    def counter_toiletplus(self):
        self.countertoilet = self.countertoilet + 1
        self.numtoilet = str(self.countertoilet)

    def counter_toiletminus(self):
        if self.countertoilet > 0:
            self.countertoilet = self.countertoilet - 1
            self.numtoilet = str(self.countertoilet)

        else:
            pass

    numwatering = StringProperty("0")
    counterwatering = 0

    def counter_wateringplus(self):
        self.counterwatering = self.counterwatering + 2
        self.numwatering = str(self.counterwatering)

    def counter_wateringminus(self):
        if self.counterwatering > 0:
            self.counterwatering = self.counterwatering - 2
            self.numwatering = str(self.counterwatering)

        else:
            pass

    def checkbox_click(self, instance, value, pressure):
        if value:
            self.shower_pressure = pressure

    def checkbox_kg_click(self, instance, value, load):
        if value:
            self.laundry_weight = load

    def checkbox_water_click(self, instance, value, watering):
        if value:
            self.watering_pressure = watering

    def add_data(self):
        if self.shower_pressure and self.watering_pressure and self.laundry_weight:
            addRecord(user, self.shower_pressure, self.numshower, self.laundry_weight, self.counterwash, self.numtoilet,
                      self.watering_pressure, self.counterwatering)
            global sm
            print(sm.ids)
            sm.switch_to(sm.ids.home_screen)


file = Builder.load_file('kivy.kv')


class Quiz_v_1App(App):
    def build(self):
        return file


Quiz_v_1App().run()
