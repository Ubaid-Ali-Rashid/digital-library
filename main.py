import os
import sqlite3
from kivy.lang import Builder
from kivy.uix.spinner import Spinner
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import ScreenManager,Screen
import tempfile
from kivymd.uix.list import OneLineListItem,MDList
from kivy.metrics import dp
from kivymd.uix.textfield import MDTextField


class LoginScreen(Screen):
    pass
class SignUpScreen(Screen):
    pass
class SemesterScreen(Screen):
    pass
class BookScreen(Screen):
    pass
class PdfScreen(Screen):
    pass
class AdminScreen(Screen):
    pass
class UserDetailScreen(Screen):
    pass
class AddBookScreen1(Screen):
    pass
class AddBookScreen2(Screen):
    pass
class AddBookScreen3(Screen):
    pass
class ChangeUserStatusScreen(Screen):
    pass
class DeleteUserScreen(Screen):
    pass
class WindowManager(ScreenManager):
    pass


class BooksLibrary(MDApp):
    semester_name = None
    semester_books = None
    semester_books_pdf_list = None
    addBook = None
    semester_select = None#AddBook
    user_table_name = None#AddBook
    pdf_save_path = None#AddBook
    def build(self):
        Window.size= (340,600)
        self.theme_cls.primary_palette = 'Teal'
        return Builder.load_file('main.kv')

    def change_theme(self):
        if self.theme_cls.theme_style == 'Light':
            self.theme_cls.theme_style = 'Dark'
        else:
            self.theme_cls.theme_style = 'Light'



    def go_back(self,go_to_screen):
        if go_to_screen == 'SemesterSelect':
            self.root.ids.ScreenManager.current = 'SemesterSelect'
            screen_book = self.root.ids.ScreenManager.get_screen('Books_Screen')
            screen_book.ids.book_list.clear_widgets()
            self.semester_name = None
            self.semester_books = None
            self.semester_books_pdf_list = None
        elif go_to_screen == 'Books_Screen':
            self.root.ids.ScreenManager.current = 'Books_Screen'
            screen_books = self.root.ids.ScreenManager.get_screen('Books_Screen')
            screen_books.manager.transition.direction = 'right'
            self.pdf_books = None
            screen_pdf = self.root.ids.ScreenManager.get_screen('Pdfs')
            screen_pdf.ids.pdf_list.clear_widgets()
        elif go_to_screen == 'Admin':
            self.root.ids.ScreenManager.current = 'Admin'
            screen = self.root.ids.ScreenManager.get_screen('ChangeUserStatus')
            screen.ids.registration.text = ''
        elif go_to_screen == 'AddBook1':
            self.root.ids.ScreenManager.current = 'AddBook'
            screen = self.root.ids.ScreenManager.get_screen('AddBook')
            screen.ids.semester_select.text = 'Select Semester'
            screen.ids.enter_book.active = False
            screen.ids.select_book.active = False
            screen = self.root.ids.ScreenManager.get_screen('AddBook2')
            screen.remove_widget(self.new_table)
        elif go_to_screen == 'AddBook2':
            screen = self.root.ids.ScreenManager.get_screen('AddBook3')
            screen.manager.transition.direction = 'right'
            self.root.ids.ScreenManager.current = 'AddBook2'
            self.theme_cls.theme_style = 'Light'
        elif go_to_screen == 'AddBook3':
            self.root.ids.ScreenManager.current = 'AddBook'
            screen = self.root.ids.ScreenManager.get_screen('AddBook2')
            screen.ids.file_name.text = 'Not Selected'
            if self.user_table_name[-1] == 'Spinner':
                self.new_table.text = 'Select Book'
            else:
                self.new_table.text = ''
            self.user_table_name = None
            self.pdf_save_path = None

            # screen.manager.transition.direction = 'right'


    def log_out(self):
        self.root.ids.ScreenManager.current = 'login'
        self.semester_name = None
        self.semester_books = None
        self.semester_books_pdf_list = None
        self.addBook = None
        self.semester_select = None
        self.user_table_name = None
        self.pdf_save_path = None


# User Phase
    def go_to_sign_up(self):
        self.root.ids.ScreenManager.current = 'SignUp'
        pass

    def create_account(self):
        sign_up_screen = self.root.ids.ScreenManager.get_screen('SignUp')
        reg_no = sign_up_screen.ids.registration.text
        name = sign_up_screen.ids.name.text.upper()
        students_data = {}

        with sqlite3.connect('PDFs/Login.db') as connection:
            cursor = connection.cursor()

            cursor.execute("""SELECT * FROM Users_Data;""")
            students_info = cursor.fetchall()
            for i in range(len(students_info)):
                students_data.update({students_info[i][0]: students_info[i][1]})

        if self.check_student_data(reg_no) and (reg_no not in students_data.keys()):
            with sqlite3.connect('PDFs/Login.db') as connection:
                cursor = connection.cursor()
                cursor.execute("""INSERT INTO Users_Data VALUES(?,?,?)""", (reg_no,name,'UNBLOCK'))
            dialog = MDDialog(text='Account is Created Successfully.',
                              buttons=[
                                  MDFlatButton(text='OK',on_release=lambda x: dialog.dismiss()),
                              ])
            dialog.open()
            sign_up_screen.ids.registration.text = ''
            sign_up_screen.ids.name.text = ''
            self.root.ids.ScreenManager.current = 'login'
            screen = self.root.ids.ScreenManager.get_screen('login')
            screen.ids.registration.text = ''
            screen.ids.name.text = ''
        elif reg_no in students_data.keys():
            dialog = MDDialog(title='Error'
                              ,text='Account is already created on this Registration Number!',
                              buttons=[
                                  MDFlatButton(text='Close', text_color= self.theme_cls.primary_color,on_release=lambda x: dialog.dismiss()),
                              ])
            dialog.open()
            sign_up_screen.ids.registration.text = ''
            sign_up_screen.ids.name.text = ''
        elif len(reg_no) == 0:
            dialog = MDDialog(title='Error',
                              text='Please fill the Registration Number Field!',
                              buttons=[
                                  MDFlatButton(text='Close',text_color= self.theme_cls.primary_color,on_release=lambda x: dialog.dismiss())
                              ])
            dialog.open()
        elif len(name) == 0:
            dialog = MDDialog(title='Error',
                              text='Please fill the Name Field!',
                              buttons=[
                                  MDFlatButton(text='Close', text_color=self.theme_cls.primary_color,on_release=lambda x: dialog.dismiss())
                              ])
            dialog.open()



    def submit(self):
        login_screen = self.root.ids.ScreenManager.get_screen('login')
        reg_no = login_screen.ids.registration.text
        name = login_screen.ids.name.text.upper()
        students_data = {}
        admins_data = {}

        with sqlite3.connect('PDFs/Login.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM Users_Data;""")
            students_info = cursor.fetchall()
            for i in range(len(students_info)):
                students_data.update({students_info[i][0]: students_info[i][1:]})
            cursor.execute("""SELECT * FROM Admin_Data;""")
            admins_info = cursor.fetchall()
            for i in range(len(admins_info)):
                admins_data.update({admins_info[i][0]: admins_info[i][1]})
            # print(students_data)

        if self.check_student_data(reg_no):
            if reg_no in list(students_data) and name == students_data[reg_no][0] and students_data[reg_no][1] == 'UNBLOCK':
                self.root.ids.ScreenManager.current = 'SemesterSelect'
            elif reg_no in list(students_data) and name == students_data[reg_no][0] and students_data[reg_no][1] == 'BLOCK':
                dialog = MDDialog(title='Account Blocked'
                                  ,text='Your account has been blocked by the Admin!\nTo unblock, Contact to the Admin.',
                                  buttons=[
                                      MDFlatButton(text='Close',on_release=lambda x: dialog.dismiss(),text_color=self.theme_cls.primary_color),
                                  ])
                dialog.open()
                login_screen.ids.registration.text = ''
                login_screen.ids.name.text = ''
            elif reg_no in list(admins_data) and name == admins_data[reg_no]:
                self.root.ids.ScreenManager.current = 'Admin'
            else:
                dialog = MDDialog(title='Error',
                                  text='Registration no. or Name is Invalid.',
                                       buttons=[
                                           MDFlatButton(text='Close', text_color=self.theme_cls.primary_color,on_release=lambda x: dialog.dismiss())
                                       ])
                dialog.open()

        login_screen.ids.name.text = ''
        login_screen.ids.registration.text = ''


    def check_student_data(self, reg_no):
        try:
            reg_no = reg_no.split('-')
            if len(reg_no) == 3 and reg_no[0].isdigit() and (len(reg_no[1]) == 3 or len(reg_no[1])==2) and reg_no[1].isalpha() and reg_no[1].isupper() and reg_no[2].isdigit():
                return True
            else:
                dialog = MDDialog(title='Error',
                                  text='Registration No. or its format is invalid.',
                                  buttons=[
                                      MDFlatButton(text='Close',text_color=self.theme_cls.primary_color,on_release= lambda x: dialog.dismiss())
                                  ])
                dialog.open()
                self.root.ids.name.text = ''
                self.root.ids.registration.text = ''
        except:
            pass

    def books_page(self):
        semesters = ['Semester 1','Semester 2','Semester 3','Semester 4','Semester 5','Semester 6','Semester 7','Semester 8']
        screen = self.root.ids.ScreenManager.get_screen('SemesterSelect')
        if (screen.ids.Semester_spinner.text not in semesters):
            dialog = MDDialog(title='Error',
                              text='Please Select a Semester.',
                              buttons=[
                                  MDFlatButton(text='Close',text_color=self.theme_cls.primary_color,on_release= lambda x: dialog.dismiss())
                              ])
            dialog.open()
        else:
            self.root.ids.ScreenManager.current = 'Books_Screen'
            self.semester_name = screen.ids.Semester_spinner.text
            book_screen = self.root.ids.ScreenManager.get_screen('Books_Screen')
            with sqlite3.connect('PDFs/'+self.semester_name+'.db') as semester:
                cursor = semester.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                self.semester_books = cursor.fetchall()

            if len(self.semester_books) == 0:
                book_screen.ids.label_no_pdf.text = "No Records Found"

            else:
                book_screen.ids.label_no_pdf.text = ''
                for i in range(len(self.semester_books)):
                    self.semester_books[i] = self.semester_books[i][0]
                for i in range(len(self.semester_books)):
                    item = OneLineListItem(text=self.semester_books[i],on_release= lambda x=self.semester_books[i]: self.open_pdf_screen(x.text))
                    book_screen.ids.book_list.add_widget(item)

            pass


    def open_pdf_screen(self,folder_name):
        self.root.ids.ScreenManager.current = 'Pdfs'
        screen_pdf = self.root.ids.ScreenManager.get_screen('Pdfs')
        screen_pdf.manager.transition.direction = 'left'

        with sqlite3.connect('PDFs/'+self.semester_name+'.db') as pdf:
            cursor = pdf.cursor()
            cursor.execute(f"SELECT Books_Name from '{folder_name}';")
            self.pdf_books = cursor.fetchall()
            for i in range(len(self.pdf_books)):
                self.pdf_books[i] = self.pdf_books[i][0]
            for i in range(len(self.pdf_books)):
                items = OneLineListItem(text=self.pdf_books[i],on_release= lambda x=self.pdf_books[i]: self.open_pdf(x.text,folder_name))
                screen_pdf.ids.pdf_list.add_widget(items)

    def open_pdf(self,pdf_name, table_name):
        extension = os.path.splitext(pdf_name)
        extension = extension[1]
        if not extension:
            extension = '.tmp'
        with sqlite3.connect('PDFs/'+self.semester_name+'.db') as pdf:
            cursor = pdf.cursor()
            cursor.execute(f"SELECT Books_Name,Books_PDF from '{table_name}' WHERE Books_Name = '{pdf_name}';")
            pdf_info = cursor.fetchall()
            with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as f:
                f.write(pdf_info[0][1])
                f.flush()
                f_path = f.name
            os.startfile(f_path)

            # print(pdf_info)
        return

# Admin Phase
    def go_to_admin_options_screen(self):
        admin_screen = self.root.ids.ScreenManager.get_screen('Admin')
        feature = admin_screen.ids.admin_spinner.text
        # print(feature)

        if feature != 'Check Users Details' and feature != 'Add Book' and feature != 'Change User Status' and feature != 'Delete User':
            dialog = MDDialog(text="Please select an option", buttons=[MDFlatButton(text="Close", on_release= lambda x: dialog.dismiss())])
            dialog.open()
        elif feature == 'Change User Status':
            self.root.ids.ScreenManager.current = 'ChangeUserStatus'
        elif feature == 'Add Book':
            self.root.ids.ScreenManager.current = 'AddBook'
        elif feature == 'Check Users Details':
            self.root.ids.ScreenManager.current = 'UserDetails'
            self.User_details()
        else:
            self.root.ids.ScreenManager.current = 'DeleteUser'


# Block User

    def reg_check(self,reg):
        try:
            reg_no = reg.split('-')
            if len(reg_no) == 3 and reg_no[0].isdigit() and (len(reg_no[1]) == 3 or len(reg_no[1]) == 2) and reg_no[1].isalpha() and reg_no[1].isupper() and reg_no[2].isdigit():
                return True
            else:
                dialog = MDDialog(title='Error',
                                  text='Registration No. or its format is invalid.',
                                  buttons=[
                                      MDFlatButton(text='Close', text_color=self.theme_cls.primary_color,
                                                   on_release=lambda x: dialog.dismiss())
                                  ])
                dialog.open()
                self.root.ids.registration.text = ''
        except:
            pass

    def change_status(self):
        screen = self.root.ids.ScreenManager.get_screen('ChangeUserStatus')
        reg_no = screen.ids.registration.text
        if self.reg_check(reg_no):
            with sqlite3.connect('PDFs/Login.db') as user:
                cursor = user.cursor()
                cursor.execute(f"SELECT Reg_No from Users_Data")
                users_reg = cursor.fetchall()
            for i in range(len(users_reg)):
                users_reg[i] = users_reg[i][0]

            if reg_no not in users_reg:
                dialog = MDDialog(title='Error'
                                  , text= 'Registration Number is not registered.',
                                  buttons=[
                                      MDFlatButton(text='Close',text_color=self.theme_cls.primary_color,on_release= lambda x: dialog.dismiss())
                                  ])
                dialog.open()
                screen.ids.registration.text = ''
            else:
                with sqlite3.connect('PDFs/Login.db') as user:
                    cursor = user.cursor()
                    cursor.execute(f"SELECT * from Users_Data where Reg_No = '{reg_no}';")
                    user_data = cursor.fetchall()
                if user_data[0][-1] == 'BLOCK':
                    dialog = MDDialog(text=f'Status of {reg_no} is Block.',
                                      buttons=[
                                          MDFlatButton(text='UnBlock',on_release=lambda x: self.status_change('UNBLOCK',reg_no,dialog)),
                                          MDFlatButton(text='Cancel',on_release=lambda x: dialog.dismiss())
                                      ])
                    dialog.open()

                else:
                    dialog = MDDialog(text=f'Status of {reg_no} is UnBlock.',
                                      buttons=[
                                          MDFlatButton(text='Block',on_release=lambda x: self.status_change('BLOCK', reg_no,dialog)),
                                          MDFlatButton(text='Cancel', on_release=lambda x: dialog.dismiss())
                                      ])
                    dialog.open()

                screen.ids.registration.text = ''

    def status_change(self,status,reg,pre_dialog):
        pre_dialog.dismiss()
        if status == 'UNBLOCK':
            with sqlite3.connect('PDFs/Login.db') as user:
                cursor = user.cursor()
                cursor.execute("UPDATE Users_Data SET status=? WHERE Reg_No=?",(status,reg))
        else:
            with sqlite3.connect('PDFs/Login.db') as user:
                cursor = user.cursor()
                cursor.execute("UPDATE Users_Data SET status=? WHERE Reg_No=?",(status,reg))
        dialog = MDDialog(title='Update',text='Status Updated Successfully.',buttons=[MDFlatButton(text='Close',on_release=lambda x: dialog.dismiss())])
        dialog.open()

# Delete User
    def Delete_User(self):
        screen = self.root.ids.ScreenManager.get_screen('DeleteUser')
        reg = screen.ids.registration.text
        # print(self.reg_check(reg))
        if self.reg_check(reg):
            with sqlite3.connect('PDFs/Login.db') as user:
                cursor = user.cursor()
                cursor.execute("SELECT * from Users_Data WHERE Reg_No=?",(reg,))
                row = cursor.fetchall()
                # print(row)


                if row == []:
                    dialog = MDDialog(title='Error', text='Registration Number is not registered.',
                                      buttons=[
                                          MDFlatButton(text='Close', text_color=self.theme_cls.primary_color,
                                                       on_release=lambda x: dialog.dismiss())
                                      ])
                    dialog.open()
                    screen.ids.registration.text = ''
                else:
                    cursor.execute("DELETE FROM Users_Data WHERE Reg_No = ?",(reg,))
                    dialog = MDDialog(text='Delete User Successfully.',buttons=[MDFlatButton(text='Close',on_release=lambda x: dialog.dismiss())])
                    dialog.open()
                    screen.ids.registration.text = ''

# Check User Details
    def User_details(self):
        screen = self.root.ids.ScreenManager.get_screen('UserDetails')
        with sqlite3.connect('PDFs/Login.db') as user:
            cursor = user.cursor()
            cursor.execute('Select * from Users_Data')
            users = cursor.fetchall()
            row_data = [(str(u[0]),str(u[1]),str(u[2])) for u in users]


        table = MDDataTable(
            use_pagination=True,
            rows_num=10,
            pagination_menu_height='240dp',
            column_data= [('Registration No.',dp(25)),('Name',dp(18)),('Status',dp(17))],
            row_data=row_data,
            size_hint= (.95,.7),
            pos_hint = {'center_x': .5,'center_y': 0.5},
            elevation=10
        )

        table.font_size = 20
        screen.add_widget(table)

# Add Book
    def add_book(self):
        screen = self.root.ids.ScreenManager.get_screen('AddBook')
        if screen.ids.semester_select.text == 'Select Semester':
            dialog = MDDialog(text='Select a Semester.',buttons=[MDFlatButton(text='Close',on_release=lambda x: dialog.dismiss())])
            dialog.open()
        elif screen.ids.select_book.active != True and screen.ids.enter_book.active != True:
            dialog = MDDialog(text='Select the way you want to choose book.',buttons=[MDFlatButton(text='Close',on_release=lambda x: dialog.dismiss())])
            dialog.open()
        else:
            self.semester_select = screen.ids.semester_select.text
            if screen.ids.enter_book.active == True:
                self.addBook = 'type'
            else:
                self.addBook = 'select'
            self.add_book2(self.semester_select,self.addBook)

    def add_book2(self,semester,table):
        self.root.ids.ScreenManager.current = 'AddBook2'
        screen = self.root.ids.ScreenManager.get_screen('AddBook2')
        with sqlite3.connect('PDFs/' + semester + '.db') as semester:
            cursor = semester.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            table_names = cursor.fetchall()
            table_names = [u[0] for u in table_names]
        if table == 'select':
            self.new_table = Spinner(text='Select Book',
                              pos_hint={'center_x': .5,'center_y': 0.7},
                              size_hint= (.7,.1),
                              values=table_names,)
        else:
            self.new_table = MDTextField(multiline=False,
                                    pos_hint={'center_x': .5,'center_y': 0.7},
                                    hint_text= 'New Book Name',
                                    size_hint_x=.7,
                                    icon_right='notebook')
        screen.add_widget(self.new_table)

    def select_file(self):
        self.root.ids.ScreenManager.current = 'AddBook3'
        self.theme_cls.theme_style = 'Dark'

    def save_file(self, filename):
        with sqlite3.connect('PDFs/' + self.semester_select + '.db') as file:
            cursor = file.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            table_names = [u[0] for u in cursor.fetchall()]
            if self.new_table.text.upper() in table_names:
                self.user_table_name = [self.new_table.text.upper(),'Spinner']
            else:
                self.user_table_name = [self.new_table.text.upper(),'TextField']
        self.pdf_save_path = '/'.join(filename[0].split('\\'))
        filename = filename[0].split('\\')[-1]
        self.go_back('AddBook2')
        screen = self.root.ids.ScreenManager.get_screen('AddBook2')
        screen.ids.file_name.text = filename

    def add_in_db(self):
        # screen = self.root.ids.ScreenManager.get_screen('AddBook2')
        if self.new_table.text == 'Select Book' or self.new_table.text == '':
            dialog = MDDialog(text='Select a Book./Type name of Book',buttons=[MDFlatButton(text='Close',on_release=lambda x: dialog.dismiss())])
            dialog.open()
        elif self.pdf_save_path == None:
            dialog = MDDialog(text='Select a File',buttons=[MDFlatButton(text='Close', on_release=lambda x: dialog.dismiss())])
            dialog.open()
        else:
            with open(self.pdf_save_path, 'rb') as file:
                file_binary = file.read()
            file_name = self.pdf_save_path.split('/')[-1]

            with sqlite3.connect('PDFs/' + self.semester_select + '.db') as file:
                cursor = file.cursor()
                cursor.execute(f"""CREATE TABLE IF NOT EXISTS '{self.user_table_name[0]}'(
                                    Books_Name TEXT,
                                    Books_PDF BLOB)""")
                cursor.execute(f"""INSERT INTO '{self.user_table_name[0]}' VALUES (?,?)""",(str(file_name),file_binary))
                file_name = None
                file_binary = None
            dialog = MDDialog(text = 'File Added Successfully.',buttons=[MDFlatButton(text='Ok',on_release=lambda x: dialog.dismiss())])
            dialog.open()
            self.go_back('AddBook3')






if __name__ == '__main__':
    BooksLibrary().run()

# with sqlite3.connect('PDFs/Semester 2.db') as semester:
#     c = semester.cursor()
#     books_location = [x for x in os.listdir("C:/Users/User/OneDrive/Desktop/books/Semester 2/")]
#     # print(books_location)
#     for j in range(len(books_location)):
#         c.execute(f"""CREATE TABLE IF NOT EXISTS "{books_location[j]}"
#                      (
#                          Books_Name TEXT,
#                          Books_PDF BLOB
#                      )""")
#         # print(folder_name)
#         # print(books_location[j])
#         pdf_names = [x for x in os.listdir("C:/Users/User/OneDrive/Desktop/books/Semester 2/"+books_location[j])]
#         # print(pdf_names,sep='\n')
#
#         for p in pdf_names:
#             # print(p)
#             with open("C:/Users/User/OneDrive/Desktop/books/Semester 2/"+books_location[j]+'/'+str(p),'rb') as f:
#                 book_binary = f.read()
#             c.execute(f"""INSERT INTO "{books_location[j]}" VALUES (?,?)""",(str(p),book_binary))

# ->Get tables Name
# with sqlite3.connect('PDFs/Semester 1.db') as semester:
#     cursor = semester.cursor()
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     tables_name = cursor.fetchall()
#     for i in tables_name:
#         print(i[0])/