import tkinter as tk
from tkinter import ttk
import sqlite3

# Класс для главного окна, наследуется от класса Frame библиотеки tkinter
class Main(tk.Frame):
    def __init__(self, root) -> None:
        """Создание экземпляра класса Main"""

        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self) -> None:
        """Хранение и инициализация графических элементов на главном окне"""

        toolbar = tk.Frame(bg="#d7d8e0", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопка для открытия дочернего окна для добавления контакта
        self.add_img = tk.PhotoImage(file="phone_book/img/add.png")
        btn_open_dialog = tk.Button(
            toolbar, 
            bg="#d7d8e0", 
            bd=0, 
            image=self.add_img, 
            command=self.open_add_dialog
        )
        btn_open_dialog.pack(side=tk.LEFT)

        # Таблица данных на главном окне
        self.tree = ttk.Treeview(
            self, 
            columns=("ID", "name", "tel", "email"), 
            height=45, 
            show="headings"
        )

        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("tel", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)

        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("tel", text="Телефон")
        self.tree.heading("email", text="E-mail")

        self.tree.pack(side=tk.LEFT)

        # Кнопка для открытия дочернего окна для редактирования контакта
        self.update_img = tk.PhotoImage(file="phone_book/img/update.png")
        btn_edit_dialog = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.update_img,
            command=self.open_update_dialog,
        )
        btn_edit_dialog.pack(side=tk.LEFT)

        # Кнопка для удаления контактов
        self.delete_img = tk.PhotoImage(file="phone_book/img/delete.png")
        btn_delete = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.delete_img,
            command=self.delete_records,
        )
        btn_delete.pack(side=tk.LEFT)

        # Кнопка для поиска контакта
        self.search_img = tk.PhotoImage(file="phone_book/img/search.png")
        btn_search = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.search_img,
            command=self.open_search_dialog,
        )
        btn_search.pack(side=tk.LEFT)

    def open_add_dialog(self) -> None:
        """Метод для открытия дочернего окна для добавления контакта"""

        Add()

    def records(self, name, tel, email) -> None:
        """Метод для добавления контакта"""

        self.db.insert_data(name, tel, email)
        self.view_records()

    def view_records(self) -> None:
        """Метод для обновления таблицы на главном экране"""

        self.db.cursor.execute("SELECT * FROM db")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]

    def open_update_dialog(self) -> None:
        """Метод для открытия дочернего окна для редактирования данных контакта"""

        Update()

    def update_records(self, name, tel, email) -> None:
        """Метод для редактирования контакта"""

        self.db.cursor.execute(
            """UPDATE db SET name=?, tel=?, email=? WHERE id=?""",
            (name, tel, email, self.tree.set(self.tree.selection()[0], "#1")),
        )
        self.db.conn.commit()
        self.view_records()

    def delete_records(self) -> None:
        """Метод для удаления контактов"""

        for selection_items in self.tree.selection():
            self.db.cursor.execute(
                "DELETE FROM db WHERE id=?", (self.tree.set(selection_items, "#1"))
            )
            self.db.conn.commit()
            self.view_records()

    def open_search_dialog(self):
        """Метод для открытия дочернего окна для поиска"""

        Search()

    def search_records(self, name) -> None:
        """Метод для поиска контакта по имени"""

        name = "%" + name + "%"
        self.db.cursor.execute("SELECT * FROM db WHERE name LIKE ?", (name,))

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]


# Класс дочернего окна, на котором добавляем новый контакт,
# наследуется от класса Toplevel библиотеки tkinter
class Add(tk.Toplevel):
    def __init__(self) -> None:
        """Метод создания экзмепляра класса Add"""

        super().__init__(root)
        self.init_add()
        self.view = app

    def init_add(self) -> None:
        """Хранение и инициализация графических элементов на дочернем окне"""

        # Настройки окна
        self.title("Добавить")
        self.geometry("400x220")
        self.resizable(False, False)

        # Обработка событий
        self.grab_set()
        self.focus_set()

        # форма для записи данных
        label_name = tk.Label(self, text="ФИО:")
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text="Телефон:")
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text="E-mail:")
        label_sum.place(x=50, y=110)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)

        # Кнопка для закрытия окна
        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=220, y=170)

        # Кнопка для добавления данных в базу данных 
        self.btn_ok = ttk.Button(self, text="Добавить")
        self.btn_ok.place(x=300, y=170)

        self.btn_ok.bind(
            "<Button-1>",
            lambda event: self.view.records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get()
                )
        )


# Класс дочернего окна, на котором редактируют данные контакта,
# наследуется от класса Add
class Update(Add):
    def __init__(self) -> None:
        """Метод создания экзмепляра класса Update"""

        super().__init__()
        self.init_update()
        self.view = app
        self.db = db
        self.default_data()

    def init_update(self) -> None:
        """Метод редактирования данных контакта"""

        self.title("Редактирование контакта")

        # Кнопка для редактировния данных контакта и закрытия окна
        btn_edit = ttk.Button(self, text="Редактировать")
        btn_edit.place(x=205, y=170)

        btn_edit.bind(
            "<Button-1>",
            lambda event: self.view.update_records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get()
            ),
        )

        btn_edit.bind("<Button-1>", lambda event: self.destroy(), add="+")
        self.btn_ok.destroy()

    def default_data(self) -> None:
        """Метод вставки уже имеющихся данных контакта в поля редактирования"""

        self.db.cursor.execute(
            "SELECT * FROM db WHERE id=?",
            self.view.tree.set(self.view.tree.selection()[0], "#1"),
        )
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])


# Класс дочернего окна для поиска контакта по имени в базе данных,
# наследуется от класса Toplevel библиотеки tkinter
class Search(tk.Toplevel):
    def __init__(self) -> None:
        """Метод создания экземпляра класса Search"""

        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        """Метод для поиска контакта"""

        # Настройки окна
        self.title("Поиск контакта")
        self.geometry("300x100")
        self.resizable(False, False)

        label_search = tk.Label(self, text="Имя:")
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=100, y=20, width=150)

        # Кнопка для закрытия окна
        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=185, y=50)

        # Кнопка для поиска контакта по имени и закрытия окна
        btn_search = ttk.Button(self, text="Найти")
        btn_search.place(x=105, y=50)
        btn_search.bind(
            "<Button-1>",
            lambda event: self.view.search_records(self.entry_search.get()),
        )
        btn_search.bind("<Button-1>", lambda event: self.destroy(), add="+")


# Класс для выполнения действий с базой данных
class DB:
    def __init__(self) -> None:
        """Создание экземпляра класса DB"""

        self.conn = sqlite3.connect("db.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS db (
                id INTEGER PRIMARY KEY,
                name TEXT,
                tel TEXT,
                email TEXT
            )"""
        )
        self.conn.commit()

    def insert_data(self, name, tel, email) -> None:
        """Метод для добавления данных в базу данных"""

        self.cursor.execute(
            """INSERT INTO db(name, tel, email) VALUES(?, ?, ?)""", (name, tel, email)
        )
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Телефонная книга")
    root.geometry("665x450")
    root.resizable(False, False)
    root.mainloop()

