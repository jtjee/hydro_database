import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import psycopg2
from datetime import datetime

class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.conn = psycopg2.connect(dbname="hydro", user="jee")
		self.cur = self.conn.cursor()

		# Attributes for the purchases tab
		self.dateLine = QLineEdit("mm/dd/yyyy")
		self.priceLine = QLineEdit("00.00")
		self.itemCombo = QComboBox()
		self.quantityLine = QLineEdit("0")
		self.supplierCombo = QComboBox()
		self.submitButton = QPushButton("Submit")
		self.submitButton.clicked.connect(self.submit_purchase)

		# Attributes for the insertion tab
		self.itemAdd = QLineEdit()
		self.itemAddCombo = QComboBox()
		self.itemAddButton = QPushButton("Add Item")
		self.itemAddButton.clicked.connect(self.submit_item)
		self.supplierAdd = QLineEdit()
		self.supplierAddAddress= QLineEdit()
		self.supplierAddCity = QLineEdit()
		self.supplierAddState = QLineEdit()
		self.supplierAddZip = QLineEdit()
		self.supplierAddPhone = QLineEdit()
		self.supplierAddButton = QPushButton("Add Supplier")
		self.supplierAddButton.clicked.connect(self.submit_supplier)
		self.categoryAdd = QLineEdit()
		self.categoryAddButton = QPushButton("Add Category")
		self.categoryAddButton.clicked.connect(self.submit_category)

		# Create purchases tab
		tabwidget = QTabWidget()
		tabwidget.addTab(self.createPurchaseGroup(), "Purchases")
		tabwidget.addTab(self.createInsertWidget(), "Insert")

		# Main vertical box layout for the application
		main_vbox = QVBoxLayout()
		main_vbox.addWidget(tabwidget)

		# Create the central widget
		main_widget = QWidget()
		main_widget.setLayout(main_vbox)
		self.setWindowTitle("Hydro Purchases")
		self.setCentralWidget(main_widget)

	def createInsertWidget(self):
		insertWidget = QWidget()
		layout = QVBoxLayout()

		layout.addWidget(self.createItemGroup())
		layout.addWidget(self.createSupplierGroup())
		layout.addWidget(self.createCategoryGroup())

		insertWidget.setLayout(layout)
		return insertWidget	

	def createItemGroup(self):
		groupBox = QGroupBox("Item")
		layout = QFormLayout()
		layout.addRow(QLabel("Name"), self.itemAdd)
		layout.addRow(QLabel("Category"), self.itemAddCombo)
		categories = self.get_categories()
		for c in categories:
			self.itemAddCombo.addItem(c[1] + ' , ' + str(c[0]))
		layout.addRow(self.itemAddButton)
		groupBox.setLayout(layout)
		return groupBox

	def createSupplierGroup(self):
		groupBox = QGroupBox("Supplier")
		layout = QFormLayout()
		layout.addRow(QLabel("Name"), self.supplierAdd)
		layout.addRow(QLabel("Address"), self.supplierAddAddress)
		layout.addRow(QLabel("City"), self.supplierAddCity)
		layout.addRow(QLabel("State"), self.supplierAddState)
		layout.addRow(QLabel("Zip"), self.supplierAddZip)
		layout.addRow(QLabel("Phone"), self.supplierAddPhone)
		layout.addRow(self.supplierAddButton)
		groupBox.setLayout(layout)
		return groupBox

	def createCategoryGroup(self):
		groupBox = QGroupBox("Category")
		layout = QFormLayout()
		layout.addRow(QLabel("Name"), self.categoryAdd)
		layout.addRow(self.categoryAddButton)
		groupBox.setLayout(layout)
		return groupBox

	def createPurchaseGroup(self):
		formGroupBox = QGroupBox("Purchases")
		layout = QFormLayout()
		layout.addRow(QLabel("Date"), self.dateLine)
		layout.addRow(QLabel("Price"), self.priceLine)
		items = self.get_items()
		for i in items:
			self.itemCombo.addItem(i[1] + ' , ' + str(i[0]))
		layout.addRow(QLabel("Item"), self.itemCombo)
		layout.addRow(QLabel("Quantity"), self.quantityLine)
		suppliers = self.get_suppliers()
		for s in suppliers:
			self.supplierCombo.addItem(s[1] + ' , ' + str(s[0]))
		layout.addRow(QLabel("Supplier"), self.supplierCombo)

		layout.addRow(self.submitButton)

		formGroupBox.setLayout(layout)
		return formGroupBox

	def submit_item(self):
		i_id = self.get_new_key('i_id', 'items')
		i_description = self.itemAdd.text()
		i_category = self.itemAddCombo.currentText().split(' , ')[1]
		self.cur.execute("""
			INSERT INTO items
			VALUES (%s, '%s', '%s')
			""" % (i_id, i_description, i_category))
		self.conn.commit()
		print("Added {}into items database, i_id={}".format(i_description, i_id))
		name = i_description + ' , ' + str(i_id)
		self.itemCombo.addItem(name)

	def submit_supplier(self):
		s_id = self.get_new_key('s_id', 'supplier')
		s_name = self.supplierAdd.text()
		s_address = self.supplierAddAddress.text()
		s_city = self.supplierAddCity.text()
		s_state = self.supplierAddState.text()
		s_zip = self.supplierAddZip.text()
		s_phone = self.supplierAddPhone.text()
		self.cur.execute("""
			INSERT INTO supplier
			VALUES (%s, '%s', '%s', '%s', '%s', %s, '%s')
			""" % (s_id, s_name, s_address, s_city, s_state, s_zip, s_phone))
		self.conn.commit()
		print("Added {}into supplier database, s_id={}".format(s_name, s_id))
		name = s_name + ' , ' + str(s_id)
		self.supplierCombo.addItem(name)

	def submit_category(self):
		c_id = self.get_new_key('c_id', "item_category")
		c_description = self.categoryAdd.text()
		self.cur.execute("""
			INSERT INTO item_category
			VALUES (%s, '%s')
			""" % (c_id, c_description))
		self.conn.commit()
		print("Added {}into item_category database, c_id={}".format(c_description, c_id))
		name = c_description + ' , ' + str(c_id)
		self.itemAddCombo.addItem(name)

	def submit_purchase(self):
		p_id = self.get_new_key('p_id', 'purchases')
		try:
			p_date = datetime.strptime(self.dateLine.text(), "%m/%d/%Y")
		except ValueError:
			print("ERROR: Enter a valid daty: mm/dd/yyyy")
			return 0 
		try:
			p_price = round(float(self.priceLine.text()),2)
		except TypeError:
			print("ERROR: Enter a valid float price")

		try:
			p_quantity = int(self.quantityLine.text())
		except ValueError:
			print("ERROR: Enter a valid integer quantity")
			return 0 
		p_name, p_item = self.itemCombo.currentText().split(', ')
		p_supplier = self.supplierCombo.currentText().split(', ')[1]
		self.cur.execute("""
			INSERT INTO purchases
			VALUES (%s, '%s', %s, %s, %s, %s)
			""" % (p_id, p_date, p_price, p_item, p_quantity, p_supplier))
		self.conn.commit()
		print("Added {}into purchases database, p_id={}".format(p_name, p_id))

	def get_new_key(self, t_id, table):
		self.cur.execute("""
			SELECT MAX(%s) FROM %s
			""" % (t_id, table))
		response = self.cur.fetchall()
		key = response[0][0]
		try:
			key = key + 1
			return key
		except TypeError:
			return 1

	def get_items(self):
		self.cur.execute("""
			SELECT i_id, i_description FROM items;
			""")
		response = self.cur.fetchall()
		# print(response)
		return response

	def get_suppliers(self):
		self.cur.execute("""
			SELECT s_id, s_name FROM supplier;
			""")
		response = self.cur.fetchall()
		# print(response)
		return response

	def get_categories(self):
		self.cur.execute("""
			SELECT c_id, c_description FROM item_category;
			""")
		response = self.cur.fetchall()
		# print(response)
		return response

if __name__ == '__main__':
	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()

	app.exec_()