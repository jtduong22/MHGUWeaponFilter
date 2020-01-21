import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from database_query import *

class HelloWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowTitle("Testing gui")

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)

        title = QLabel("Hello World", self)
        gridLayout.addWidget(title,0,0)

class MHDatabaseWindow(QMainWindow):
    def __init__(self):
        # initialize main window
        QMainWindow.__init__(self)
        self.setMinimumSize(640,400)
        self.setWindowTitle("MHGU Weapon DB")

        # initialize main
        test_widget = QWidget(self)
        self.setCentralWidget(test_widget)

        # create layout? (required for alignment to work)
        test_layout = QVBoxLayout(self)
        test_widget.setLayout(test_layout)

        label = QLabel("MHGU Filter", self)
        label.setAlignment(Qt.AlignHCenter)
        test_layout.addWidget(label)

        # create comboboxes

        damage_layout = self.create_combobox_label("Damage Type: ", db_constants.DAMAGE_TYPES)
        balance_layout = self.create_combobox_label("Balance Type: ", db_constants.BALANCE_TYPES)
        element_layout = self.create_combobox_label("Element Type: ", db_constants.ELEMENT_TYPES)
        sharpness_layout = self.create_combobox_label("Sharpness: ", db_constants.SHARPNESS_TYPES)
        order_layout = self.create_combobox_label("Order By: ", db_constants.ORDER_BY_TYPES)

        # add combobox to application

        test_layout.addLayout(damage_layout)
        test_layout.addLayout(balance_layout)
        test_layout.addLayout(element_layout)
        test_layout.addLayout(sharpness_layout)
        test_layout.addLayout(order_layout)

        # set reference to combobox

        self.damage_type_combobox = damage_layout.itemAt(1).widget()
        self.balance_layout_combobox = balance_layout.itemAt(1).widget()
        self.element_layout_combobox = element_layout.itemAt(1).widget()
        self.sharpness_layout_combobox = sharpness_layout.itemAt(1).widget()
        self.order_layout_combobox = order_layout.itemAt(1).widget()

        # create read all actions button
        read_button = QPushButton("Read all")
        read_button.clicked.connect(self.read_all)
        test_layout.addWidget(read_button, alignment=Qt.AlignBottom)

        # create close button
        quit_button = QPushButton("Close application", self)
        quit_button.clicked.connect(self.close)
        test_layout.addWidget(quit_button, alignment=Qt.AlignBottom)

    def create_combobox_label(self, label_text:str, drop_content: list) -> QLayout:
        layout = QHBoxLayout(self)

        label = QLabel(label_text, self)
        label.setAlignment(Qt.AlignRight)

        combobox = QComboBox(self)
        combobox.addItems(drop_content)

        layout.addWidget(label)
        layout.addWidget(combobox)

        return layout

    def read_all(self):
        d_type_selection = self.damage_type_combobox.currentIndex()
        b_type_selection = self.balance_layout_combobox.currentIndex()
        e_type_selection = self.element_layout_combobox.currentIndex()
        s_type_selection = self.sharpness_layout_combobox.currentIndex()
        o_type_selection = self.order_layout_combobox.currentIndex()

        print(d_type_selection)
        print(b_type_selection)
        print(e_type_selection)
        print(s_type_selection)
        print(o_type_selection)
        print()

        location = './Data/mhgu.db'
        db = weapon_db(location)
        db.add_damage_type_filter(d_type_selection)
        db.add_balance_type_filter(b_type_selection)
        db.add_element_type_filter(e_type_selection)
        db.add_sharpness_filter(s_type_selection)
        db.order_results_by(o_type_selection)

        db.execute()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # mainWin = HelloWindow()
    mainWin = MHDatabaseWindow()
    mainWin.show()

sys.exit(app.exec_())