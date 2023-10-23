from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

window=Tk()
window.title("Query Creator Application")
window.geometry("1000x600")
window.configure(bg="SkyBlue")
sb = Scrollbar(window)
sb.pack(side=RIGHT, fill=Y)

f1 = ("Algerian",20)
f2 = ("Times",16)
f3 = ("Arial",14)

nameR = []


def open_page(e):

    btn_text = e.widget.cget('text')

    if(btn_text == 'Create Table Query'):
        attr_field = []
        dt_field = []
        list2 = ["CHAR(10)", "CHAR(20)", "VARCHAR(30)", "VARCHAR(50)", "VARCHAR(255)", "INTEGER", "DATE"]
        E_Name = []
        var = []

        new = Tk()
        new.geometry("1000x600")
        new.title("Insert Query Page")
        new.configure(bg="skyblue")
        sb = Scrollbar(new)
        sb.pack(side=RIGHT, fill=Y)

        f1 = ("Algerian", 20)
        f2 = ("Times", 16)
        f3 = ("Arial", 14)

        def add_another_colum(e):
            row_y = 280
            num = int(column_field.get())

            def option_changed(value):
                dt_field.append(value)


            for i in range(0,num):
                attr_field.append(Entry(new, width=20, font=f3))
                attr_field[i].place(x=100, y=row_y)

                var.append(StringVar(new))
                var[i].set("Datatype")
                E_Name.append(OptionMenu(new, var[i], *list2,command=option_changed))
                E_Name[i].place(x=400, y=row_y)

                row_y = row_y + 50

            create_query.place(x=350, y=row_y+40)

        def home_page():
            new.withdraw()
            window.deiconify()

        def query_generate(e):
            query_values = dict()
            query = ""
            num = int(len(attr_field))
            table_name = str(table_field.get())

            for i in range(0,num):
                query_values.update({str(attr_field[i].get()):str(dt_field[i])})

            count = 1
            for i in query_values:
                if(count == num):
                    query = query + i + " " + query_values[i]
                else:
                    query = query + i + " " + query_values[i] + ","

                count = count + 1


            sql_command = "CREATE TABLE " + table_name + " ( " + query + ");"
            result = messagebox.askyesno("askyesno", "Your Query Was Generated...!\n\n" + sql_command + "\n\n" + "You Want to Run this Query")
            if(result == True):
                conn = sqlite3.connect("APP.db")
                crsr = conn.cursor()
                print("Connected..!")
                crsr.execute(sql_command)
                conn.close()
                home_page()
            else:
                print("Something Went Wrong")

        heading = Label(new, text="--- Create Table Query Page ---", font=f1, bg='skyblue')
        heading.place(x=350, y=50)

        back_btn = Button(new, width=10, text="Back", font=f2,command=home_page)
        back_btn.place(x=50, y=50)

        table_label = Label(new, text="Table Name :- ", font=f2, bg="skyblue")
        table_label.place(x=100, y=150)

        table_field = Entry(new, width=20, font=f3)
        table_field.place(x=270, y=150)

        column_label = Label(new, text="Column Number :- ", font=f2, bg="skyblue")
        column_label.place(x=520, y=150)

        column_field = Entry(new, width=20, font=f3)
        column_field.place(x=700, y=150)

        attr_name = Label(new, text="Attribute Name", font=f2, bg="skyblue")
        attr_name.place(x=100, y=230)

        dt_name = Label(new, text="Datatype", font=f2, bg="skyblue")
        dt_name.place(x=400, y=230)

        next_btn = Button(new, text="Next", width=10, height=1, font=f3)
        next_btn.place(x=700, y=230)
        next_btn.bind('<Button-1>', add_another_colum)

        create_query = Button(new, text="Create Table Query", width=15, height=1, font=f3)
        create_query.bind('<Button-1>', query_generate)

        window.withdraw()
        new.mainloop()

    elif(btn_text == 'Create Insert Query'):
        attr_field = []
        dt_field = []
        flag = 0
        new = Tk()
        new.geometry("1000x600")
        new.title("Insert Query Page")
        new.configure(bg="skyblue")
        sb = Scrollbar(new)
        sb.pack(side=RIGHT, fill=Y)
        cols = []

        f1 = ("Algerian", 20)
        f2 = ("Times", 16)
        f3 = ("Arial", 14)

        def add_another_colum(e):
            cols.clear()
            row_y = 250
            table_name = str(table_field.get())

            conn = sqlite3.connect("APP.db")
            crsr = conn.cursor()
            try:
                data = crsr.execute("SELECT * FROM " + table_name)
                for column in data.description:
                    cols.append(column[0])

                flag = 1
                conn.commit()

            except:
                messagebox.showwarning("warning","No Such Table Found")

            if(flag == 1):
                for i in range(0,len(cols)):
                    attr_field.append(Entry(new, width=20, font=f3))
                    attr_field[i].place(x=100, y=row_y)
                    attr_field[i].insert(0,cols[i])
                    attr_field[i].configure(state="disabled")

                    dt_field.append(Entry(new, width=20, font=f3))
                    dt_field[i].place(x=400, y=row_y)

                    row_y = row_y+50

                create_query.place(x=350, y=row_y)

        def home_page():
            new.withdraw()
            window.deiconify()

        def query_generate(e):
            val = []
            query = ""
            num = int(len(attr_field))
            table_name = str(table_field.get())

            for i in range(0,len(cols)):
                val.append(dt_field[i].get())

            count = 1;
            for i in val:
                print(type(i))
                if(count == len(cols)):
                    query = query + "'" + i + "'"
                else:
                    query = query + "'" + i + "',"
                count = count + 1

            sql_command = "INSERT INTO " + table_name + " VALUES (" + query + ");"
            result = messagebox.askyesno("askyesno",
                                         "Your Query Was Generated...!\n\n" + sql_command + "\n\n" + "You Want to Run this Query")
            if(result == True):
                conn = sqlite3.connect("APP.db")
                crsr = conn.cursor()
                print("Connected..!")
                crsr.execute(sql_command)
                conn.commit()
                conn.close()
                home_page()
            else:
                print("Something Went Wrong")


        heading = Label(new, text="--- Insert Query Page ---", font=f1, bg='skyblue')
        heading.place(x=350, y=50)

        back_btn = Button(new, width=10, text="Back", font=f2,command=home_page)
        back_btn.place(x=50, y=50)

        table_label = Label(new, text="Table Name :- ", font=f2, bg="skyblue")
        table_label.place(x=100, y=150)

        table_field = Entry(new, width=20, font=f3)
        table_field.place(x=300, y=150)

        attr_name = Label(new, text="Attribute Name", font=f2, bg="skyblue")
        attr_name.place(x=100, y=200)

        dt_name = Label(new, text="Values", font=f2, bg="skyblue")
        dt_name.place(x=400, y=200)

        add_btn = Button(new, width=15, text="Search", font=f2)
        add_btn.place(x=600, y=140)
        add_btn.bind('<Button-1>', add_another_colum)

        create_query = Button(new, text="Create Insert Query", width=15, height=1, font=f3)
        create_query.bind('<Button-1>', query_generate)

        window.withdraw()
        new.mainloop()

    elif(btn_text == 'Create Update Query'):
        attr_field = []
        dt_field = []
        flag = 0
        new = Tk()
        new.geometry("1000x600")
        new.title("Insert Query Page")
        new.configure(bg="skyblue")
        sb = Scrollbar(new)
        sb.pack(side=RIGHT, fill=Y)
        cols = []
        data = []

        f1 = ("Algerian", 20)
        f2 = ("Times", 16)
        f3 = ("Arial", 14)

        def add_another_colum(e):
            cols.clear()
            row_y = 280
            table_name = str(table_field.get())
            cond_col = str(cond_field.get())
            cond_val = str(cond_f_VAL.get())

            conn = sqlite3.connect("APP.db")
            crsr = conn.cursor()
            try:
                data = crsr.execute("SELECT * FROM " + table_name)
                for column in data.description:
                    cols.append(column[0])
                data = crsr.fetchall()
                flag = 1

                conn.commit()
                conn.close()

            except:
                messagebox.showwarning("warning", "No Such Table Found")

            print(cols)

            ind = 0
            for i in cols:
                if(i == cond_col):
                    break;
                else:
                    ind = ind+1

            if (flag == 1):
                count = 0
                for i in data:
                    if(cols[ind] == cond_col and str(i[ind]) == cond_val):
                        print("Found")
                        for j in range(0, len(cols)):
                            attr_field.append(Entry(new, width=20, font=f3))
                            attr_field[j].place(x=100, y=row_y)
                            attr_field[j].insert(0, cols[j])
                            attr_field[j].configure(state="disabled")

                            dt_field.append(Entry(new, width=20, font=f3))
                            dt_field[j].place(x=400, y=row_y)
                            dt_field[j].insert(0,i[count])

                            row_y = row_y + 50
                            count = count + 1

                        create_query.place(x=350, y=row_y)


        def home_page():
            new.withdraw()
            window.deiconify()

        def query_generate(e):
            val = []
            query = ""
            num = int(len(attr_field))
            table_name = str(table_field.get())
            cond_col = str(cond_field.get())
            cond_val = str(cond_f_VAL.get())

            for i in range(0, len(cols)):
                val.append(dt_field[i].get())

            for i in range(0,len(cols)):
                if(i == (len(cols)-1)):
                    query =  query + str(cols[i]) + "='" + val[i] + "'"
                else:
                    query = query + str(cols[i]) + "='" + val[i] + "',"

            sql_command = "UPDATE " + table_name +  " SET " + query + " WHERE " + str(cond_col) + " = " + str(cond_val) + ";"
            result = messagebox.askyesno("askyesno", "Your Query Was Generated...!\n\n" + sql_command + "\n\n" + "You Want to Run this Query")
            if (result == True):
                conn = sqlite3.connect("APP.db")
                crsr = conn.cursor()
                print("Connected..!")
                crsr.execute(sql_command)
                conn.commit()
                conn.close()
                home_page()
            else:
                print("Something Went Wrong")

        heading = Label(new, text="--- Update Query Page ---", font=f1, bg='skyblue')
        heading.place(x=350, y=50)

        back_btn = Button(new, width=10, text="Back", font=f2,command=home_page)
        back_btn.place(x=50, y=50)

        table_label = Label(new, text="Table Name :- ", font=f2, bg="skyblue")
        table_label.place(x=100, y=120)

        table_field = Entry(new, width=20, font=f3)
        table_field.place(x=300, y=120)

        cond_label = Label(new, text="Condition Attribute :- ", font=f2, bg="skyblue")
        cond_label.place(x=550, y=120)

        cond_field = Entry(new, width=15, font=f3)
        cond_field.place(x=750, y=120)

        cond_value = Label(new, text="Condition Value :- ", font=f2, bg="skyblue")
        cond_value.place(x=550, y=170)

        cond_f_VAL = Entry(new, width=15, font=f3)
        cond_f_VAL.place(x=750, y=170)


        add_btn = Button(new, width=15, text="Search", font=f2)
        add_btn.place(x=400, y=220)
        add_btn.bind('<Button-1>', add_another_colum)

        create_query = Button(new, text="Create Insert Query", width=15, height=1, font=f3)
        create_query.bind('<Button-1>', query_generate)

        window.withdraw()
        new.mainloop()

    elif(btn_text == 'Create Delete Query'):
        attr_field = []
        dt_field = []
        flag = 0
        new = Tk()
        new.geometry("1000x600")
        new.title("Delete Query Page")
        new.configure(bg="skyblue")
        sb = Scrollbar(new)
        sb.pack(side=RIGHT, fill=Y)
        cols = []
        data = []

        f1 = ("Algerian", 20)
        f2 = ("Times", 16)
        f3 = ("Arial", 14)

        def home_page():
            new.withdraw()
            window.deiconify()

        def query_generate(e):
            table_name = str(table_field.get())
            cond_col = str(attr_field.get())
            cond_val = str(dt_field.get())
            conn = sqlite3.connect("APP.db")
            crsr = conn.cursor()

            try:
                data = crsr.execute("SELECT * FROM " + table_name)
                for column in data.description:
                    cols.append(column[0])

                flag = 1

                conn.commit()
                conn.close()

            except:
                messagebox.showwarning("warning", "No Such Table Found")

            if(flag == 1):
                sql_command = "DELETE FROM " + table_name + " WHERE " + cond_col + " = " + cond_val + ";"
                result = messagebox.askyesno("askyesno",
                                             "Your Query Was Generated...!\n\n" + sql_command + "\n\n" + "You Want to Run this Query")
                if (result == True):
                    conn = sqlite3.connect("APP.db")
                    crsr = conn.cursor()
                    print("Connected..!")
                    crsr.execute(sql_command)
                    conn.commit()
                    conn.close()
                    home_page()
                else:
                    print("Something Went Wrong")

        heading = Label(new, text="--- Delete Query Page ---", font=f1, bg='skyblue')
        heading.place(x=300, y=50)

        back_btn = Button(new, width=10, text="Back", font=f2,command=home_page)
        back_btn.place(x=50, y=50)

        table_label = Label(new, text="Table Name :- ", font=f2, bg="skyblue")
        table_label.place(x=100, y=150)

        table_field = Entry(new, width=20, font=f3)
        table_field.place(x=300, y=150)

        attr_name = Label(new, text="Condition Attribute", font=f2, bg="skyblue")
        attr_name.place(x=100, y=200)

        dt_name = Label(new, text="Condition Value", font=f2, bg="skyblue")
        dt_name.place(x=400, y=200)

        attr_field = Entry(new, width=20, font=f3)
        attr_field.place(x=100, y=250)

        dt_field = Entry(new, width=20, font=f3)
        dt_field.place(x=400, y=250)

        create_query = Button(new, text="Create Delete Query", width=15, height=1, font=f3)
        create_query.place(x=350, y=300)
        create_query.bind('<Button-1>', query_generate)

        window.withdraw()
        new.mainloop()

lbl1 = Label(window,text="--- Query Creator Application ---",font=f1,bg='skyblue')
lbl1.place(x=300,y=50)


btn1 = Button(window,text="Create Table Query",width=15,height=2,bg="LightGreen",font=f2)
btn1.place(x=80,y=250)
btn1.bind('<Button-1>',open_page)

btn2 = Button(window,text="Create Insert Query",width=15,height=2,bg="LightGreen",font=f2)
btn2.place(x=280,y=250)
btn2.bind('<Button-1>',open_page)

btn3 = Button(window,text="Create Update Query",width=15,height=2,bg="LightGreen",font=f2)
btn3.place(x=480,y=250)
btn3.bind('<Button-1>',open_page)

btn4 = Button(window,text="Create Delete Query",width=15,height=2,bg="LightGreen",font=f2)
btn4.place(x=680,y=250)
btn4.bind('<Button-1>',open_page)

window.mainloop()