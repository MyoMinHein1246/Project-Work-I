from PyQt5.QtWidgets import *
from PyQt5 import uic
import sqlite3


def resource_path(relative_path) -> str:
    import os, sys

    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


DATA_HEADERS = ["Id", "First name", "Last name", "Job", "Salary", "Address"]


class AddEmployeeForm(QDialog):
    def __init__(self, parent, callback_func):
        super(AddEmployeeForm, self).__init__(parent)

        uic.loadUi(resource_path("./Resources/AddEmployeeForm.ui"), self)

        self.btnAdd.clicked.connect(lambda: self.callback(callback_func))
        self.btnCancel.clicked.connect(lambda: self.destroy(True, True))
        self.closeEvent = self.clear()

    def callback(self, callback_func):
        if (
            self.editFirstName.text() == ""
            or self.editLastName.text() == ""
            or self.editJob.text() == ""
            or self.editSalary.text() == ""
        ):
            QMessageBox.critical(
                None, "Error", "All fields are required except address."
            )
        else:
            callback_func()
            self.clear()
            self.destroy(True, True)

    def clear(self):
        self.editFirstName.setText("")
        self.editLastName.setText("")
        self.editJob.setText("")
        self.editSalary.setText("")
        self.editAddress.setText("")


class EmployeeSearchForm(QMainWindow):
    def __init__(self, cursor):
        super(EmployeeSearchForm, self).__init__()
        uic.loadUi(resource_path("./Resources/EmployeeSearchForm.ui"), self)
        self._addEmployeeForm = AddEmployeeForm(self, self.add_employee)
        self.cursor = cursor
        self.editEmployeeName.returnPressed.connect(
            lambda: self.search_employee(self.editEmployeeName.text())
        )
        self.btnSearch.clicked.connect(
            lambda: self.search_employee(self.editEmployeeName.text())
        )
        self.btnAdd.clicked.connect(lambda: self._addEmployeeForm.show())

    def search_employee(self, employeeName: str):
        if employeeName == "":
            return

        employeeData = self.is_employee_exist(employeeName)

        results = ""

        if employeeData:
            self.editEmployeeName.setText("")
            self.textResults.setPlainText("")
            for i, data in enumerate(employeeData):
                results = results + "{}: {}\n".format(DATA_HEADERS[i], data)
        else:
            results = "Employee not found!"
            print(results)

        print(results)
        self.textResults.appendPlainText(results)

    def is_employee_exist(self, employeeName: str) -> list:
        database = self.get_employee_database()

        for data in database:
            name = data[1] + " " + data[2]
            if name.lower().strip() == employeeName.lower():
                return data

        return None

    def add_employee(self):
        first_name = self._addEmployeeForm.editFirstName.text().strip()
        last_name = self._addEmployeeForm.editLastName.text().strip()
        job = self._addEmployeeForm.editJob.text().strip()
        salary = self._addEmployeeForm.editSalary.text().strip()
        address = self._addEmployeeForm.editAddress.text().strip()

        try:
            self.cursor.execute(
                "INSERT INTO employee(first_name, last_name, job, salary, address) VALUES(?, ?, ?, ?, ?)",
                (first_name, last_name, job, salary, address),
            )

            QMessageBox.information(self, "Succes", "Employee added successfully!")
            print("Employee added successfully!")
        except sqlite3.Error as err:
            print("[Error] ", err)

    def get_employee_database(self) -> list:
        database = []

        try:
            self.cursor.execute("SELECT * FROM employee;")
            results = self.cursor.fetchall()
            for line in results:
                data_list = []
                for data in line:
                    data_list.append(data)

                database.append(data_list)
        except sqlite3.Error as e:
            print("Failed to read database")
            print("[Error] ", e)

        return database


def main():
    try:
        connection = sqlite3.connect(resource_path("./Resources/EmployeeData.db"))
        cursor = connection.cursor()

        app = QApplication.instance()
        if not app:
            app = QApplication([])

        searchForm = EmployeeSearchForm(cursor)
        searchForm.show()

        app.exec_()
    except sqlite3.Error as err:
        print("Failed to connect to sqlite database.")
        print("[Error] ", err)
    finally:
        if cursor:
            connection.commit()

            cursor.close()
            print("Closed cursor.")
            connection.close()
            print("Closed connection.")


if __name__ == "__main__":
    main()
