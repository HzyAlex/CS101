import PySimpleGUI as sg
import sqlite3

conn = sqlite3.connect('Sports Meeting.db')
c = conn.cursor()

mainmenu =  [
    [sg.Submit('Add Class')],
    [sg.Submit('Add Event')],
    [sg.Submit('Input Athlete')],
    [sg.Submit('Record Result')],
    [sg.Submit('View Result')],
    [sg.Submit('Class Score')],
]

addclass = [
    [sg.Text('Grade:'), sg.Combo(['10', '11', '12'])],
    [sg.Text('Class:'), sg.InputText()],
    [sg.Submit('Submit')],
]


addevent = [
    [sg.Text('Name:'), sg.InputText()],
    [sg.Text('Type:'),sg.Combo(['Field', 'Track'])],
    [sg.Text('Gender:'),sg.Combo(['Male', 'Female'])],
    [sg.Text('Grade:'),sg.Combo(['10', '11', '12'])], 
    [sg.Submit('Submit')],
]

inputathlete = [
    [sg.Text('ID:'), sg.InputText()],
    [sg.Text('Name:'), sg.InputText()],
    [sg.Text('Gender:'),sg.Combo(['Male', 'Female'])],
    [],
    [],
    [],
    [],
    [sg.Submit('Submit')],
]

recordresult = [
    [],
    [],
    [sg.Text('Grade:'), sg.Combo(['10', '11', '12'])],
    [sg.Submit('Confirm')]
]


viewresult = [
    [],
    []

]

form = sg.Window('Sports Meeting Tool').Layout(mainmenu)
(event, info) = form.Read()
form.Close()
if not event:
    exit()

while True:
    if event == 'Add Class':
        form = sg.Window('Add Class').Layout(addclass)
        (event, info) = form.Read()
        print(info)
        form.Close()
        if event:
            sql = f"INSERT INTO Class (Grade, Class_Number) VALUES ({info[0]},{info[1]})"
            c.execute(sql)
            conn.commit() 
    elif event == 'Add Event':
        form = sg.Window('Add Event').Layout(addevent)
        (event, info) = form.Read()
        form.Close()
        if event:
            genderblob = (info[2] == 'Male')
            type_ = (info[1] == 'Track')
            c.execute(f"INSERT INTO Event (Name,RankSF,Gender,Grade) \
                VALUES ('{info[0]}', {type_}, {genderblob}, {info[3]})")
            conn.commit()
    elif event == 'Input Athlete':
        classlist = []
        classid_list = []
        cursor = c.execute("SELECT Class_Number, ID from Class")
        for row in cursor:
            classlist.append(row[0])
            classid_list.append(row[1])
        eventlist = []
        id_list = []
        cursor = c.execute("SELECT ID, Name, Gender from Event")
        for row in cursor:
            id_list.append(row[0])
            sex = 'male' if row[2] else 'female'
            eventlist.append(f'{row[1]} - {sex}')
        inputathlete[3] = [sg.Combo(classlist)]
        inputathlete[4] = [sg.Combo(eventlist)]
        inputathlete[5] = [sg.Combo(eventlist)]
        form = sg.Window('Input Athlete').Layout(inputathlete)
        (event, info) = form.Read()
        form.Close()
        if event:
            genderblob = (info[2] == 'Male')
            class_id = int(info[3])
            class_index = classlist.index(class_id)
            class_id_ = classid_list[class_index]
            event_1 = info[4]
            event_1_index = eventlist.index(event_1)
            event_2 = info[5]
            event_2_index = eventlist.index(event_2)
            event_id_1 = id_list[event_1_index]
            event_id_2 = id_list[event_2_index]
            c.execute(f"INSERT INTO Athlete (ID,Name,Gender,Class_ID,Event_ID_1,Event_ID_2) \
                VALUES ({info[0]}, '{info[1]}', {genderblob}, {class_id_}, '{event_id_1}', '{event_id_2}')")
            conn.commit()
    elif event == 'Record Result':
        eventlist = []
        id_list = []
        cursor = c.execute("SELECT ID, Name, Gender from Event")
        for row in cursor:
            id_list.append(row[0])
            sex = 'male' if row[2] else 'female'
            eventlist.append(f'{row[1]} - {sex}')
        recordresult[0] = [sg.Combo(eventlist)]
        form = sg.Window('Event Information').Layout(recordresult)
        (event, info) = form.Read()
        if event:
            event_ = info[0]
            event_index = eventlist.index(event_)
            event_id_ = id_list[event_index]
            cursor = c.execute(f"SELECT ID, Name from Athlete WHERE Event_ID_1 = {event_id_} or Event_ID_2 = {event_id_}")
            eventresult = [[sg.Text('Athlete ID'),sg.Text('Athlete Result')]]
            id_list = []
            for row in cursor:
                id_list.append(row[0])
                eventresult.append([sg.Text(f'{row[0]} - {row[1]}'), sg.InputText()])
            eventresult.append([sg.Submit('Submit')])
            form = sg.Window('Record Result').Layout(eventresult)
            (event, info) = form.Read()
            if event:
                scorelist = [7, 6, 5, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0]
                result_info = {}
                for i in range(len(info)):
                    result_info[id_list[i]] = info[i]
                rank_k = []
                cursor = c.execute(f'SELECT RankSF FROM Event WHERE ID = {event_id_}')
                for row in cursor:
                    ranksf = row[0]
                for k in sorted(result_info,key=result_info.__getitem__, reverse=ranksf):
                    rank_k.append(k)
                for i in range(len(info)):
                    c.execute(f"INSERT INTO Result (Event_ID,Athlete_ID,Res,Score) \
                        VALUES ({event_id_}, {rank_k[i]}, {result_info[rank_k[i]]}, {scorelist[i]})")
                conn.commit() 
        form.Close()
    elif event == 'View Result':
        eventlist = {}
        cursor = c.execute("SELECT ID, Name, Gender from Event")
        for row in cursor:
            sex = 'male' if row[2] else 'female'
            eventlist[f'{row[1]} - {sex}'] = row[0]
        viewresult = [
            [sg.Text('Event::'),sg.Combo(list(eventlist.keys()))], 
            #[sg.Text('Grade:'),sg.Combo(['10', '11', '12'])],
            [sg.Submit('submit')],
            ]
        form = sg.Window('View Result').Layout(viewresult)
        (event, info) = form.Read()
        id = eventlist[info[0]]
        form.Close()
        cursor = c.execute(f'SELECT RankSF FROM Event WHERE ID = {id}')
        for row in cursor:
            ranksf = 'ASC' if row[0] else 'DESC'
        cursor_t = c.execute(f'SELECT * FROM Result WHERE Event_ID = {id} ORDER BY Res {ranksf}')
        view = [[sg.Text('Rank'), sg.Text('ID'), sg.Text('Name'), sg.Text('Result')]]
        i = 0
        for row in cursor_t:
            print(row[0])
            c2 = conn.cursor()
            cursor_name = c2.execute(f'SELECT Name FROM Athlete WHERE ID = {row[1]}')
            for row_name in cursor_name:
                name = row_name[0]
            i = i + 1
            view.append([sg.Text(i), sg.Text(row[1]),sg.Text(name), sg.Text(row[2])])
        form = sg.Window('View Result').Layout(view)
        (event, info) = form.Read()
    elif event == 'Class Score':
        cursor_class = c.execute(f'SELECT ID, Class_Number FROM Class')
        class_info = {}
        class_score = {}
        for row_class in cursor_class:
            id_class = row_class[0]
            class_info[id_class] = row_class[1]
            c2 = conn.cursor()
            cursor_athlete = c2.execute(f'SELECT ID FROM Athlete WHERE Class_ID = {id_class}')
            for row_athlete in cursor_athlete:
                id_athlete = row_athlete[0]
                c3 = conn.cursor()
                cursor_result = c3.execute(f'SELECT Score FROM Result WHERE Athlete_ID = {id_athlete}')
                for row_result in cursor_result:
                    score = row_result[0]
                    class_score[id_class] = class_score.get(id_class, 0) + score
        classscore = [[sg.Text('Name'), sg.Text('Score')]]
        for id in class_info.keys():
            classscore.append([sg.Text(class_info[id]), sg.Text(class_score.get(id, 0))])
        form = sg.Window('Class Score').Layout(classscore)
        (event, info) = form.Read()
    else:
        print(event)
        form = sg.Window('Sports Meeting Tool').Layout(mainmenu)
        (event, info) = form.Read()
        form.Close()
        if not event:
            break

conn.close()
