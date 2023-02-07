from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys


FILE_NAME = "database.txt"
DATA_HEADERS = ["Name", "Job", "Salary", "Address"]

class EmployeeSearchForm(QMainWindow):
	def __init__(self):
		super(EmployeeSearchForm, self).__init__()
		uic.loadUi("EmployeeSearchForm.ui", self)
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
			if data[0].lower() == employeeName.lower():
				return data

		return None

	def get_employee_database(self) -> list:
		database = []

		try:
			with open(FILE_NAME, 'r') as f:
				for line in f.readlines():
					data_list = []
					for data in line.split(','):
						data_list.append(data.strip())
					
					database.append(data_list)
		except OSError:
			print("Failed to read database")

		return database
		
def main():
	app = QApplication.instance()
	if not app:
		app = QApplication([])

	searchForm = EmployeeSearchForm()
	searchForm.show()

	sys.exit(app.exec_())


if __name__ == "__main__":
	main()
