from tkinter import *
from tkinter.messagebox import showinfo, showerror
from tkinter.ttk import Notebook, Treeview, Combobox

from tkcalendar import DateEntry
from datetime import date
from tabulate import tabulate
import re

label_style = {'font': ('Calibri', 12, 'bold')}
text_style = {'font': ('Calibri', 12)}
label_position = {'sticky': W, 'padx': (20, 100), 'pady': (20, 0)}
text_position = {'sticky': NSEW, 'padx': (20, 100), 'pady': (0, 20)}
styles = [label_style, text_style, label_position, text_position]


class MainWindow(Frame):
    def __init__(self, root):
        super(MainWindow, self).__init__(root)
        root.title("Паспортные данные")
        root.geometry("700x700")
        root.iconbitmap("logo.ico")
        root.resizable(False, False)

        self.tabControl = Notebook(root)
        self.tab1 = Tab1()
        self.tab2 = Tab2()
        self.tab3 = Tab3()
        self.tab4 = Tab4()
        self.tab5 = Tab5()

        self.tabControl.add(self.tab1, text='Основная информация')
        self.tabControl.add(self.tab2, text='Место жительства')
        self.tabControl.add(self.tab3, text='Семейное положение')
        self.tabControl.add(self.tab4, text='Дети')
        self.tabControl.add(self.tab5, text='Воинская обязанность')
        self.tabControl.pack(expand=1, fill="both")

        self.tab1.grid_columnconfigure(0, weight=1)
        self.tab1.grid_columnconfigure(1, weight=1)
        self.tab2.grid_columnconfigure(0, weight=1)
        self.tab2.grid_columnconfigure(1, weight=1)
        self.tab3.grid_columnconfigure(0, weight=1)
        self.tab3.grid_columnconfigure(1, weight=1)
        self.tab4.grid_columnconfigure(0, weight=1)
        self.tab4.grid_columnconfigure(1, weight=1)
        self.tab4.grid_columnconfigure(2, weight=1)
        self.tab5.grid_columnconfigure(0, weight=1)
        self.tab5.grid_columnconfigure(1, weight=1)

        btn = Button(self, text="Сохранить", command=self.click, font=("Calibri", 12))
        btn.pack(pady=20)

        self.tab1.text_surname.focus()

    def check(self, textboxes):
        result = True

        self.tab3.label_SP.configure({"background": "white"})
        self.tab5.label_vo.configure({"background": "white"})
        for x, i in enumerate(textboxes):
            for y, j in enumerate(i):
                if isinstance(j, Entry):
                    j.configure({"background": "white"})
                if isinstance(j, StringVar):
                    self.tab1.text_genderM.configure(font='white')
                    self.tab1.text_genderW.configure(font='white')

        for x, i in enumerate(textboxes):
            if x == 3:
                continue
            else:
                for y, j in enumerate(i):
                    if isinstance(j, Label):
                        j.configure({"background": "tomato2"})
                        result = False
                    elif j.get() == '' or j.get() == '-':
                        if x == 0 and y == 3:
                            self.tab1.text_genderM.configure(font='tomato2')
                            self.tab1.text_genderW.configure(font='tomato2')
                        else:
                            j.configure({"background": "tomato2"})
                        result = False
                    elif x == 0 and y == 10:
                        if len(j.get()) != 7:
                            j.configure({"background": "tomato2"})
                            result = False
                        else:
                            continue
                    elif x == 0 and y == 6:
                        if len(j.get()) != 4:
                            j.configure({"background": "tomato2"})
                            result = False
                        else:
                            continue
                    elif x == 0 and y == 7:
                        if len(j.get()) != 6:
                            j.configure({"background": "tomato2"})
                            result = False
                        else:
                            continue
        return result

    def getInfo(self):
        self.info3 = self.tab3.getInfo()
        self.info5 = self.tab5.getInfo()
        self.textboxes = [self.tab1.info, self.tab2.info, self.info3, [], self.info5]
        if self.check(self.textboxes) is False:
            showerror('Ошибка!', 'Заполните все поля!')
            return False
        else:
            text = []
            all_info = []
            for x, i in enumerate(self.textboxes):
                if x == 3:
                    temp = self.tab4.getData()
                    all_info.append(temp)
                else:
                    for j in i:
                        temp = j.get()
                        text.append(temp)
                    all_info.append(text)
                    text = []
            print(all_info)
            return all_info

    def click(self):
        text = self.getInfo()
        if text is not False:
            with open('passport_data.txt', 'w') as file:
                for x, i in enumerate(text):
                    if x == 0:
                        file.write('Основная информация\n\n')
                        for y, j in enumerate(i):
                            headers = ['Фамилия: ', 'Имя: ', 'Отчество: ', 'Пол: ', 'Дата рождения: ',
                                       'Место жительства: ', 'Серия: ', 'Номер: ', 'Кем выдан: ', 'Когда выдан: ',
                                       'Код подразделения: ']
                            file.write(headers[y])
                            file.write(f'{j}\n')
                    if x == 1:
                        file.write('\n\n\nМесто жительства\n\n')
                        for y, j in enumerate(i):
                            headers = ['Рег-н: ', 'Пункт: ', 'Улица: ', 'Дом: ', 'Кем зарегистрировано: ',
                                       'Когда зарегистрировано: ']
                            file.write(headers[y])
                            file.write(f'{j}\n')
                    if x == 2:
                        file.write('\n\n\nСемейное положение\n\n')
                        if len(i) == 1:
                            for j in i:
                                file.write(f'{j}\n')
                        else:
                            for y, j in enumerate(i):
                                headers = ['', 'ФИО супруга: ', 'Дата рождения супруга: ', 'Кем зарегистрирован: ',
                                           'Когда зарегистрирован: ']
                                file.write(headers[y])
                                file.write(f'{j}\n')

                    if x == 3:
                        file.write('\n\n\nДети\n\n')
                        headers = ['Пол', 'ФИО', 'Дата рождения']
                        file.write(tabulate(i, headers=headers, tablefmt='grid') + '\n')
                    if x == 4:
                        file.write('\n\n\nВоинская обязанность\n\n')
                        if len(i) == 1:
                            for j in i:
                                file.write(f'{j}\n')
                        elif len(i) == 2:
                            for y, j in enumerate(i):
                                headers = ['', 'Дата: ']
                                file.write(headers[y])
                                file.write(f'{j}\n')
                        else:
                            for y, j in enumerate(i):
                                headers = ['', 'Военный комиссариат: ', 'Дата: ']
                                file.write(headers[y])
                                file.write(f'{j}\n')
            showinfo('Сохранение', 'Данные сохранены!')


class Tab1(Frame):
    def __init__(self):
        super().__init__()
        check_series = (self.register(self.is_valid_seriel), "%P")
        check_number = (self.register(self.is_valid_number), "%P")
        check_kod = (self.register(self.is_valid_kod), "%P")
        maxdate = date.today()
        genders = ['Мужской', 'Женский']

        # Фамилия
        self.label_surname = Label(self, text='Фамилия:', **styles[0]).grid(column=0, row=0, **styles[2])
        self.text_surname = Entry(self, **styles[1])
        self.text_surname.grid(column=0, row=1, **styles[3])
        # Имя
        self.label_name = Label(self, text='Имя:', **styles[0]).grid(column=0, row=2, **styles[2])
        self.text_name = Entry(self, **styles[1])
        self.text_name.grid(column=0, row=3, **styles[3])
        # Отчество
        self.label_lastname = Label(self, text='Отчество:', **styles[0]).grid(column=0, row=4, **styles[2])
        self.text_lastname = Entry(self, **styles[1])
        self.text_lastname.grid(column=0, row=5, **styles[3])
        # Пол
        self.selected_gender = StringVar()
        self.label_gender = Label(self, text='Пол:', **styles[0]).grid(column=0, row=6, **styles[2])
        self.text_genderM = Radiobutton(self, text=genders[0], **styles[1], value=genders[0],
                                        variable=self.selected_gender)
        self.text_genderW = Radiobutton(self, text=genders[1], **styles[1], value=genders[1],
                                        variable=self.selected_gender)
        self.text_genderM.grid(sticky='W', column=0, row=7, padx=(20, 100), pady=(0, 20))
        self.text_genderW.grid(sticky='E', column=0, row=7, padx=(20, 100), pady=(0, 20))
        # Дата рождения
        self.label_datebirth = Label(self, text='Дата рождения:', **styles[0]).grid(column=0, row=8, **styles[2])
        self.text_datebirth = DateEntry(self, maxdate=maxdate, date_pattern='dd.mm.yyyy', **styles[1])
        self.text_datebirth.grid(column=0, row=9, **styles[3])
        # Место рождения
        self.label_address = Label(self, text='Место рождения:', **styles[0]).grid(column=0, row=10, **styles[2])
        self.text_address = Entry(self, **styles[1])
        self.text_address.grid(column=0, row=11, **styles[3])
        # Серия
        self.label_series = Label(self, text='Серия:', **styles[0]).grid(column=1, row=0, **styles[2])
        self.text_series = Entry(self, validate="key", validatecommand=check_series, **styles[1])
        self.text_series.grid(column=1, row=1, **styles[3])
        # Номер
        self.label_number = Label(self, text='Номер:', **styles[0]).grid(column=1, row=2, **styles[2])
        self.text_number = Entry(self, validate="key", validatecommand=check_number, **styles[1])
        self.text_number.grid(column=1, row=3, **styles[3])
        # Кем выдан паспорт
        self.label_whoissued = Label(self, text='Кем выдан паспорт:', **styles[0]).grid(column=1, row=4, **styles[2])
        self.text_whoissued = Entry(self, **styles[1])
        self.text_whoissued.grid(column=1, row=5, **styles[3])
        # Когда выдан паспорт
        self.label_dateissue = Label(self, text='Дата выдачи:', **styles[0]).grid(column=1, row=6, **styles[2])
        self.text_dateissue = DateEntry(self, maxdate=maxdate, date_pattern='dd.mm.yyyy', **styles[1])
        self.text_dateissue.grid(column=1, row=7, **styles[3])
        # Код подразделения
        self.label_kod = Label(self, text='Код подразделения:', **styles[0]).grid(column=1, row=8, **styles[2])
        self.text_kod = Entry(self, validate="key", validatecommand=check_kod, **styles[1])
        self.text_kod.insert(0, '-')
        self.text_kod.grid(column=1, row=9, **styles[3])

        self.info = [self.text_surname, self.text_name, self.text_lastname, self.selected_gender, self.text_datebirth,
                     self.text_address, self.text_series, self.text_number, self.text_whoissued, self.text_dateissue,
                     self.text_kod]

    def is_valid_seriel(self, newval):
        return re.match("^\d{0,4}$", newval) is not None

    def is_valid_number(self, newval):
        return re.match("^\d{0,6}$", newval) is not None

    def is_valid_kod(self, newval):
        return re.match(r"(\d{0,3})-(\d{0,3})$", newval) is not None


class Tab2(Frame):
    def __init__(self):
        super().__init__()
        maxdate = date.today()
        # Рег-н
        self.label_region = Label(self, text='Рег-н:', **styles[0]).grid(column=0, row=0, **styles[2])
        self.text_region = Entry(self, **styles[1])
        self.text_region.grid(column=0, row=1, **styles[3])
        # Пункт
        self.label_point = Label(self, text='Пункт:', **styles[0]).grid(column=0, row=2, **styles[2])
        self.text_point = Entry(self, **styles[1])
        self.text_point.grid(column=0, row=3, **styles[3])
        # Улица
        self.label_street = Label(self, text='Улица:', **styles[0]).grid(column=0, row=4, **styles[2])
        self.text_street = Entry(self, **styles[1])
        self.text_street.grid(column=0, row=5, **styles[3])
        # Дом
        self.label_house = Label(self, text='Дом:', **styles[0]).grid(column=0, row=6, **styles[2])
        self.text_house = Entry(self, **styles[1])
        self.text_house.grid(column=0, row=7, **styles[3])
        # Кем зарегистрирован
        self.label_whoreg = Label(self, text='Кем зарегистрирован:', **styles[0]).grid(column=1, row=0, **styles[2])
        self.text_whoreg = Entry(self, **styles[1])
        self.text_whoreg.grid(column=1, row=1, **styles[3])
        # Когда зарегистрирован
        self.label_datereg = Label(self, text='Когда зарегистрирован:', **styles[0]).grid(column=1, row=2, **styles[2])
        self.text_datereg = DateEntry(self, maxdate=maxdate, date_pattern='dd.mm.yyyy', **styles[1])
        self.text_datereg.grid(column=1, row=3, **styles[3])

        self.info = [self.text_region, self.text_point, self.text_street, self.text_house, self.text_whoreg,
                     self.text_datereg]


class Tab3(Frame):
    def __init__(self):
        super().__init__()
        self.label_SP = Label(self, text='Семейное положение:', **styles[0])
        self.label_SP.grid(column=0, row=0, **styles[2])
        self.text_SP = Combobox(self, **styles[1],
                                values=('Не состою в браке', 'Состою в браке', 'Разведен(-а)', 'Вдова/вдовец'),
                                state="readonly")
        self.text_SP.grid(sticky='NSEW', column=0, row=1, columnspan=2, padx=(20, 50), pady=(10, 10))
        self.text_SP.bind("<<ComboboxSelected>>", self.viewEntry)

    def viewEntry(self, event):
        if self.text_SP.get() != 'Не состою в браке' and self.text_SP.get() != '':
            self.clear_frame()
            maxdate = date.today()
            self.label_fio = Label(self, text='ФИО супруга:', **styles[0]).grid(column=0, row=2, **styles[2])
            self.text_fio = Entry(self, **styles[1])
            self.text_fio.grid(column=0, row=3, **styles[3])

            self.label_datebirth_spouse = Label(self, text='Дата рождения супруга:', **styles[0]).grid(column=0, row=4,
                                                                                                       **styles[2])
            self.text_datebirth_spouse = DateEntry(self, maxdate=maxdate, date_pattern='dd.mm.yyyy', **styles[1])
            self.text_datebirth_spouse.grid(column=0, row=5, **styles[3])

            self.label_whoreg_sp = Label(self, text='Кем зарегистрирован:', **styles[0]).grid(column=1, row=2,
                                                                                              **styles[2])
            self.text_whoreg_sp = Entry(self, **styles[1])
            self.text_whoreg_sp.grid(column=1, row=3, **styles[3])

            self.label_datereg_sp = Label(self, text='Когда зарегистрирован:', **styles[0]).grid(column=1, row=4,
                                                                                                 **styles[2])
            self.text_datereg_sp = DateEntry(self, maxdate=maxdate, date_pattern='dd.mm.yyyy', **styles[1])
            self.text_datereg_sp.grid(column=1, row=5, **styles[3])
        else:
            self.clear_frame()

    def clear_frame(self):
        if self.winfo_exists() != 0:
            temp = self.winfo_children()
            for num, i in enumerate(temp):
                if num != 0 and num != 1:
                    i.destroy()
                else:
                    continue

    def getInfo(self):
        if self.text_SP.get() == '':
            info = [self.label_SP]
        elif self.text_SP.get() != 'Не состою в браке':
            info = [self.text_SP, self.text_fio, self.text_datebirth_spouse, self.text_whoreg_sp, self.text_datereg_sp]
        else:
            info = [self.text_SP]
        return info


class Tab4(Frame):
    def __init__(self):
        super().__init__()
        maxdate = date.today()
        self.id = 0

        self.label_gender_children = Label(self, text='Пол:', **styles[0]).grid(sticky='W', column=0, row=0,
                                                                                padx=(20, 0), pady=(10, 10))
        self.text_gender_children = Combobox(self, **styles[1], values=('Мужской', 'Женский'), state="readonly")
        self.text_gender_children.grid(sticky='NSEW', column=1, row=0, padx=(20, 50), pady=(10, 10))

        self.label_fio_children = Label(self, text='ФИО:', **styles[0]).grid(sticky='W', column=0, row=1, padx=(20, 0),
                                                                             pady=(10, 10))
        self.text_fio_children = Entry(self, **styles[1])
        self.text_fio_children.grid(sticky='NSEW', column=1, row=1, padx=(20, 50), pady=(10, 10))

        self.label_datereg_children = Label(self, text='Дата рождения:', **styles[0]).grid(sticky='W', column=0, row=2,
                                                                                           padx=(20, 0), pady=(10, 10))
        self.text_datereg_children = DateEntry(self, maxdate=maxdate, date_pattern='dd.mm.yyyy', **styles[1])
        self.text_datereg_children.grid(sticky='NSEW', column=1, row=2, padx=(20, 50), pady=(10, 10))

        columns = ("gender", "fio", "birthdate")
        self.tree = Treeview(self, columns=columns, show="headings")
        self.tree.grid(sticky='NSEW', column=0, row=3, columnspan=3, padx=(20, 50), pady=(10, 10))
        self.tree.heading("gender", text="Пол")
        self.tree.heading("fio", text="ФИО")
        self.tree.heading("birthdate", text="Дата рождения")

        btn = Button(self, text="Добавить", command=self.add, font=("Calibri", 12))
        btn.grid(sticky='NSEW', column=2, row=0, padx=(20, 50), pady=(10, 10))

        btn = Button(self, text="Удалить", command=self.delete, font=("Calibri", 12))
        btn.grid(sticky='NSEW', column=2, row=1, padx=(20, 50), pady=(10, 10))

    def add(self):
        if self.text_fio_children.get() != '' and self.text_gender_children.get() != '':
            self.tree.insert("", END, iid=self.id, values=(
                self.text_gender_children.get(), self.text_fio_children.get(), self.text_datereg_children.get()))
            self.id = self.id + 1
        else:
            showerror('Ошибка', 'Заполните все поля!')

    def delete(self):
        row_id = self.tree.focus()
        if row_id != '':
            self.tree.delete(row_id)
        else:
            showerror('Ошибка', 'Строка не выбрана!')

    def getData(self):
        child = []
        children = []
        for line in self.tree.get_children():
            for value in self.tree.item(line)['values']:
                child.append(value)
            children.append(child)
            child = []
        return children


class Tab5(Frame):
    def __init__(self):
        super().__init__()
        self.label_vo = Label(self, text='Воинская обязанность:', **styles[0])
        self.label_vo.grid(column=0, row=0, **styles[2])
        self.text_vo = Combobox(self, **styles[1], values=(
            'Военнообязанный(-ая)', 'Невоеннообязанный(-ая)', 'Освобождён(-а) от исполнения воинской обязанности'),
                                state="readonly")
        self.text_vo.grid(sticky='NSEW', column=0, row=1, columnspan=2, padx=(20, 50), pady=(10, 10))
        self.text_vo.bind("<<ComboboxSelected>>", self.view_entry)

    def view_entry(self, event):
        maxdate = date.today()
        if self.text_vo.get() == 'Военнообязанный(-ая)':
            self.clear_frame()
            self.label_date_vo = Label(self, text='Дата:', **styles[0]).grid(column=0, row=2, **styles[2])
            self.text_date_vo = DateEntry(self, maxdate=maxdate, date_pattern='dd.mm.yyyy', **styles[1])
            self.text_date_vo.grid(column=0, row=3, **styles[3])
        elif self.text_vo.get() == 'Освобождён(-а) от исполнения воинской обязанности':
            self.clear_frame()
            self.label_vk_vo = Label(self, text='Военный комисстариат:', **styles[0]).grid(column=0, row=4, **styles[2])
            self.text_vk_vo = Entry(self, **styles[1])
            self.text_vk_vo.grid(column=0, row=5, **styles[3])

            self.label_date_vo = Label(self, text='Дата:', **styles[0]).grid(column=0, row=6, **styles[2])
            self.text_date_vo = DateEntry(self, maxdate=maxdate, date_pattern='dd.mm.yyyy', **styles[1])
            self.text_date_vo.grid(column=0, row=7, **styles[3])
        else:
            self.clear_frame()

    def clear_frame(self):
        if self.winfo_exists() != 0:
            temp = self.winfo_children()
            for num, i in enumerate(temp):
                if num != 0 and num != 1:
                    i.destroy()
                else:
                    continue

    def getInfo(self):
        if self.text_vo.get() == 'Военнообязанный(-ая)':
            self.info = [self.text_vo, self.text_date_vo]
        elif self.text_vo.get() == 'Освобождён(-а) от исполнения воинской обязанности':
            self.info = [self.text_vo, self.text_vk_vo, self.text_date_vo]
        elif self.text_vo.get() == 'Невоеннообязанный(-ая)':
            self.info = []
        else:
            self.info = [self.label_vo]
        return self.info


if __name__ == '__main__':
    root = Tk()
    app = MainWindow(root)
    app.pack()
    root.mainloop()
