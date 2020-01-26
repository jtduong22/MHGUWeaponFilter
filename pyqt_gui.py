import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from database_query import *

class MHDatabaseWindow(QMainWindow):
#### Class Constants ####
    IMAGE_LOCATION = './Images/'

#### Class variables ####
    enabled_settings = {x:True for x in db_constants.ORDER_BY_TYPES.keys()}

    damage_type_combobox = None
    balance_layout_combobox = None
    element_layout_combobox = None
    sharpness_layout_combobox = None
    order_layout_combobox = None

    weapon_table = None

#### Class Methods ####

    def __init__(self):
        # initialize main window
        QMainWindow.__init__(self)
        self.setMinimumSize(1200,400)
        self.setWindowTitle("MHGU Weapon DB")

        # initialize main
        test_widget = QWidget(self)
        self.setCentralWidget(test_widget)

        # create layout? (required for alignment to work)
        test_layout = QVBoxLayout(self)
        test_widget.setLayout(test_layout)

        # create settings button
        displayed_settings_button = QPushButton("Settings", self)
        displayed_settings_button.clicked.connect(self.create_settings_dialog)
        test_layout.addWidget(displayed_settings_button, alignment=Qt.AlignRight)

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

        # add table
        self.weapon_table = QTableWidget(self)
        test_layout.addWidget(self.weapon_table)

        # create read all actions button
        read_button = QPushButton("Search")
        read_button.clicked.connect(self.search)
        test_layout.addWidget(read_button, alignment=Qt.AlignBottom)

        # create close button
        quit_button = QPushButton("Close application", self)
        quit_button.clicked.connect(self.close)
        test_layout.addWidget(quit_button, alignment=Qt.AlignBottom)

    # initializes the settings dialog
    def create_settings_dialog(self) -> None:
        # create a new dialog
        layout = QVBoxLayout(self)
        dialog = QDialog(self)
        dialog.setLayout(layout)

        # create description at the top
        description_label = QLabel("Choose which options to display / hide", self)
        layout.addWidget(description_label)

        # create new layout for checkmarks
        checkbox_layout = QGridLayout(self)

        # create checkboxes for each selectable option
        # default row size is 3
        row_size = 3
        for count, key in enumerate(self.enabled_settings.keys()):
            # get position of item
            x = count % 3
            y = count // 3

            # create checkbox
            checkbox = QCheckBox(key, self)
            checkbox.setChecked(self.enabled_settings[key])
            checkbox.clicked.connect(self.option_selected)
            checkbox_layout.addWidget(checkbox,y,x)

        layout.addLayout(checkbox_layout)

        # add close button
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)

        # show dialog
        dialog.exec_()

    # callback when option is selected, changes the settings
    def option_selected(self) -> None:
        # get information about which checkbox
        checkbox = self.sender()
        option = checkbox.text()
        is_enabled = checkbox.isChecked()

        # change settings
        self.enabled_settings[option] = is_enabled

    # quickly create combobox with label next to it
    def create_combobox_label(self, label_text:str, drop_content: list) -> QLayout:
        layout = QHBoxLayout(self)
        label = QLabel(label_text, self)
        label.setAlignment(Qt.AlignRight)

        combobox = QComboBox(self)
        combobox.addItems(drop_content)

        layout.addWidget(label)
        layout.addWidget(combobox)

        return layout

    # search database for results
    def search(self) -> None:
        # open database
        location = './Data/mhgu.db'
        db = weapon_db(location)

        # apply selected filters to database
        self.get_selected_options(db)

        # retrieve results
        results = db.execute()

        # fill table
        self.fill_table(self.enabled_settings, results)

    # read selected options and applies to database
    def get_selected_options(self, db: weapon_db) -> None:
        # read selected option of all the comboboxes
        d_type_selection = self.damage_type_combobox.currentIndex()  # damage type: any, cutting, blunt
        b_type_selection = self.balance_layout_combobox.currentIndex()  # balance type: any, balanced, melee, boomerang
        e_type_selection = self.element_layout_combobox.currentIndex()  # element type: any, fire, water, thunder, ice, dragon, poison, sleep, paralysis, blastblight
        s_type_selection = self.sharpness_layout_combobox.currentIndex()  # sharpness type: any, red, yellow, green, blue, white, purple
        o_type_selection = self.order_layout_combobox.currentIndex()  # order by type: name, rarity, attack (melee), attack (ranged), element, sharpness, affinity (melee), affinty (ranged), blunt, balance type

        # add filters to database
        db.add_damage_type_filter(d_type_selection)
        db.add_balance_type_filter(b_type_selection)
        db.add_element_type_filter(e_type_selection)
        db.add_sharpness_filter(s_type_selection)
        db.order_results_by(o_type_selection)

    # populate table with results from database query
    def fill_table(self, displayed: dict, results: list) -> None:

        # select only data enabled for viewing
        headers = [x for x in displayed.keys() if displayed[x] == True]
        data = [x for x,y in enumerate(displayed.keys()) if displayed[y] == True]   # creates list of indexes of displayed features to cycle through

        # get size of table
        column_count = len(data)
        row_count = len(results)

        # set table size
        self.weapon_table.setColumnCount(column_count)
        self.weapon_table.setRowCount(row_count)

        # set headers
        self.weapon_table.setHorizontalHeaderLabels(headers)

        # cycle through each row
        for x_count, row in enumerate(results):                 # note: enumerate returns a tuple with the index number followed by the content, ie (0, [content])
            for y_count, column in enumerate(data):

                # add info to the cell
                item = self.parse_table_item(headers[y_count], row[column])

                # add cell to table at position x,y
                self.weapon_table.setItem(x_count, y_count, item)

        self.weapon_table.resizeColumnsToContents()
        self.setMinimumWidth(self.weapon_table.size().width()+75)

        print(self.weapon_table.size().width())

    def parse_table_item(self, item_type:str, item_index: int):
        cell = QTableWidgetItem()

        # change background color to match sharpness
        if item_type == 'sharpness':
            sharpness_type = db_constants.SHARPNESS_TYPES[item_index]   # get sharpness type
            color = db_constants.SHARPNESS_TO_RGB[sharpness_type]       # get RGB color
            cell.setBackground(QColor(color[0], color[1], color[2]))    # set background color

        # add icon to cell
        elif item_type == 'element':
            picture_location = self.IMAGE_LOCATION + item_index.lower() + '.png'
            icon = QIcon(picture_location)
            cell.setIcon(icon)

        # is text, parse accordingly to make visually clearer
        else:
            text = item_index

            # replace number with 'cutting' or 'blunt'
            if item_type == 'blunt':
                text = db_constants.DAMAGE_TYPES[item_index + 1]

            # replace number with 'balanced', 'melee', or 'boomerang
            elif item_type == 'balance type':
                text = db_constants.BALANCE_TYPES[item_index + 1]

            # align all the numbers to the right side
            elif item_type != 'name':
                cell.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            # apply text
            cell.setText(str(text))

        return  cell


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MHDatabaseWindow()
    mainWin.show()

sys.exit(app.exec_())