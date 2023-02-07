from PyQt5.QtWidgets import *
from PyQt5 import uic
import sqlite3


DATA_HEADERS = ["Id", "First name", "Last name", "Job", "Salary", "Address"]

class EmployeeSearchForm(QMainWindow):
	def __init__(self, cursor):
		super(EmployeeSearchForm, self).__init__()
		uic.loadUi("EmployeeSearchForm.ui", self)
		self.cursor = cursor
		self.editEmployeeName.returnPressed.connect(lambda: self.search_employee(self.editEmployeeName.text()))
		self.btnSearch.clicked.connect(lambda: self.search_employee(self.editEmployeeName.text()))

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
				print(results, end='')
		else:
			results = "Employee not found!"
			print(results)

		self.textResults.appendPlainText(results)
	
	def is_employee_exist(self, employeeName: str) -> list:
		database = self.get_employee_database()

		for data in database:
			print(data)
			name = data[1] + " " + data[2]
			if name.lower().strip() == employeeName.lower():
				return data

		return None

	def get_employee_database(self) -> list:
		database = []

		try:
			self.cursor.execute('SELECT * FROM employee;')
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
		connection = sqlite3.connect('EmployeeData.db')
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
			cursor.close()
			print("Closed cursor")
		if connection:
			connection.close()
			print("Closed cursor")
		

if __name__ == "__main__":
	main()
