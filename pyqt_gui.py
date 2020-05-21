import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from weapon_definitions import *

class MHDatabaseWindow(QMainWindow):
#### Class Constants ####
    IMAGE_LOCATION = './Images/'
    DB_LOCATION = './Data/mhgu.db'
#### Class variables ####
    enabled_settings = {}
    selectable_weapons = {'Palico':PalicoWeapon, 'Sword and Shield':SwordAndShield, 'Great Sword':GreatSword,
                          'Hammer':Hammer, 'Lance':Lance, 'Dual Blades':DualBlades, 'Long Sword':LongSword,
                          'Charge Blade':ChargeBlade, 'Switch Axe':SwitchAxe, 'Hunting Horn':HuntingHorn,
                          'Gunlance':Gunlance, 'Insect Glaive':InsectGlaive, 'Bow':Bow, 'Light Bowgun':LightBowgun}
    selected_weapon_type = LightBowgun
    sharpness_level = 0

    weapon_table = None

#### Class Methods ####

    def __init__(self):
        # initialize main window
        QMainWindow.__init__(self)
        self.setMinimumSize(1250,600)
        self.showMaximized()
        self.setWindowTitle("MHGU Weapon DB")

        # initialize main
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_widget.adjustSize()

        # create layout? (required for alignment to work)
        main_layout = QVBoxLayout(self)
        main_widget.setLayout(main_layout)

        # create settings button
        displayed_settings_button = QPushButton("Settings", self)
        displayed_settings_button.clicked.connect(self.create_settings_dialog)
        main_layout.addWidget(displayed_settings_button, alignment=Qt.AlignRight)

        # create combobox for selecting weapon type
        select_weapons_combobox = QComboBox(self)
        select_weapons_combobox.addItems(list(self.selectable_weapons.keys()))
        index = list(self.selectable_weapons.values()).index(self.selected_weapon_type)
        select_weapons_combobox.setCurrentIndex(index)
        select_weapons_combobox.currentTextChanged.connect(self.weapon_changed)
        main_layout.addWidget(select_weapons_combobox, alignment=Qt.AlignRight)

        self.enabled_settings = {x:True for x in self.selected_weapon_type.HEADERS}

        label = QLabel("MHGU Filter", self)
        label.setAlignment(Qt.AlignHCenter)
        main_layout.addWidget(label)

        # create sublayout for selected weapon
        # layout changes from weapon to weapon
        self.weapon_filter_layout = QVBoxLayout()
        self.create_weapon_layout(self.weapon_filter_layout, self.selected_weapon_type)
        main_layout.addLayout(self.weapon_filter_layout)

        # add table
        self.weapon_table = QTableWidget(self)
        main_layout.addWidget(self.weapon_table)

        # create read all actions button
        read_button = QPushButton("Search")
        read_button.clicked.connect(self.search)
        main_layout.addWidget(read_button, alignment=Qt.AlignBottom)

        # create close button
        quit_button = QPushButton("Close application", self)
        quit_button.clicked.connect(self.close)
        main_layout.addWidget(quit_button, alignment=Qt.AlignBottom)

    # fills layout with relevant comboboxes
    # differs from weapon to weapon
    def create_weapon_layout(self, layout, weapon_type:WeaponDB):
        # cycle through each filter and populate with respective options
        for filter in weapon_type.FILTERABLES:
            combobox_layout = self.create_combobox_label(filter, weapon_type.FILTERABLES[filter])
            layout.addLayout(combobox_layout)
        order_by_layout = self.create_combobox_label('order by', weapon_type.HEADERS)
        layout.addLayout(order_by_layout)

        # only add sharpness option if it's a blademaster weapon
        if issubclass(self.selected_weapon_type, BladeMaster):
            layout.addLayout(self.create_sharpness_level())

        if hasattr(weapon_type, 'CONTAINS'):
            temp = weapon_type(self.DB_LOCATION)
            temp.init_contains()

            for key in weapon_type.CONTAINS:
                contains_layout = self.create_contains_layout(key, weapon_type.CONTAINS[key])
                layout.addLayout(contains_layout)

    def create_sharpness_level(self) -> QHBoxLayout:
        layout = QHBoxLayout(self)
        label = QLabel("Sharpness Level")
        label.setAlignment(Qt.AlignRight)
        layout.addWidget(label)


        radio_group = QHBoxLayout(self)
        radio_group.setAlignment(Qt.AlignHCenter)
        layout.addLayout(radio_group)
        for i in range(3):
            radio_button = QRadioButton(f"Sharpness+{i}")
            radio_group.addWidget(radio_button)
        radio_group.itemAt(0).widget().setChecked(True)
        return layout

    def create_contains_layout(self, label_text: str, content: list) -> QLayout:
        layout = QVBoxLayout(self)

        description_label = QLabel(f"{label_text}", self)
        layout.addWidget(description_label)

        # create new layout for checkmarks
        checkbox_layout = QGridLayout(self)

        # create checkboxes for each selectable option
        # default row size is 7
        row_size = 7

        for count, text in enumerate(content):
            # get position of item
            x = count % row_size
            y = count // row_size

            # create checkbox
            checkbox = QCheckBox(text, self)
            checkbox.setChecked(False)
            checkbox_layout.addWidget(checkbox,y,x)

        layout.addLayout(checkbox_layout)

        return layout


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
            x = count % row_size
            y = count // row_size

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

    # callback when weapon is changed
    # clears the comboboxes from the weapon_filter_layout and replaces them with ones relevant to the weapon
    def weapon_changed(self, selected_weapon:str) -> None:
        # get class of selected weapon type
        self.selected_weapon_type = self.selectable_weapons[selected_weapon]

        # get settings
        self.enabled_settings = {x:True for x in self.selected_weapon_type.HEADERS}

        # clear previous comboboxes
        self.clear_layout(self.weapon_filter_layout)

        # fill with new comboboxes
        self.create_weapon_layout(self.weapon_filter_layout, self.selected_weapon_type)

        # clear contents
        self.weapon_table.clear()

    # recursively clear layout
    def clear_layout(self, layout:QLayout) -> None:
        # while not empty
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            # delete if widget, delete stuff inside if layout
            if widget is not None:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())

    # callback when option is selected, changes the settings
    def option_selected(self) -> None:
        # get information about which checkbox
        checkbox = self.sender()
        option = checkbox.text()
        is_enabled = checkbox.isChecked()

        # change settings
        self.enabled_settings[option] = is_enabled

    # quickly create combobox with label next to it
    def create_combobox_label(self, label_text: str, drop_content: list) -> QLayout:
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
        db = self.selected_weapon_type(self.DB_LOCATION)
        if hasattr(db, 'CONTAINS'):
            db.init_contains()

        # apply selected filters to database
        self.get_selected_options(db)

        # retrieve results
        results = db.execute()

        # fill table
        self.fill_table(self.enabled_settings, results)

    # read selected options and applies to database
    def get_selected_options(self, db: WeaponDB) -> None:
        # cycle through each option
        for child in self.weapon_filter_layout.children():
            # parse data
            label = child.itemAt(0).widget()
            combobox = child.itemAt(1).widget()
            print(label.text())

            # parse combobox
            if isinstance(combobox, QComboBox):
                print(combobox.currentIndex())

                # order by
                if label.text() == 'order by':
                    db.order_results_by(combobox.currentIndex())
                # filter by
                else:
                    db.add_filter(label.text(), combobox.currentIndex())

            # parse Sharpness Level radio buttons
            elif label.text() == 'Sharpness Level':
                radio_group = child.itemAt(1)
                for c in range(radio_group.count()):
                    radio_button = radio_group.itemAt(c).widget()
                    if radio_button.isChecked():
                        self.sharpness_level = int(radio_button.text().split('+')[1])
                        break

            # parse Horn / Shots
            else:
                grid = child.itemAt(1)
                selected = 0
                for c in range(grid.count()):
                    checkbox = grid.itemAt(c).widget()
                    if checkbox.isChecked():
                        selected += pow(2,grid.count() - 1 - c)
                    # print(checkbox.text())

                print(selected)
                if selected > 0:
                    db.add_filter(label.text(), selected)

    # populate table with results from database query
    def fill_table(self, displayed: dict, results: list) -> None:

        # select only data enabled for viewing
        headers = [x for x in displayed.keys() if displayed[x] is True]
        data = [x for x,y in enumerate(displayed.keys()) if displayed[y] is True]   # creates list of indexes of displayed features to cycle through

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

                if type(item) is QTableWidgetItem:
                    # add cell to table at position x,y
                    self.weapon_table.setItem(x_count, y_count, item)
                else:
                    self.weapon_table.setCellWidget(x_count, y_count, item)

        self.weapon_table.resizeColumnsToContents()
        self.weapon_table.resizeRowsToContents()
        # header.setStretchLastSection(True)

    def parse_table_item(self, item_type:str, item_index: int):
        cell = QTableWidgetItem()

        # change background color to match sharpness
        if item_type == 'sharpness':
            if self.selected_weapon_type is PalicoWeapon:
                sharpness_type = db_constants.SHARPNESS_TYPES[item_index + 1]   # get sharpness type
                color = db_constants.SHARPNESS_TO_RGB[sharpness_type]       # get RGB color
                cell.setBackground(QColor(color[0], color[1], color[2]))    # set background color
            else:
                cell = SharpnessBar(item_index.split()[self.sharpness_level])
                cell.setMinimumWidth(45 * SharpnessBar.WIDTH_MULTIPLIER)
                # print(item_index)

        # add icon to cell
        elif item_type == 'element' or item_type == 'element 2':
            picture_location = self.IMAGE_LOCATION + item_index.lower() + '.png'
            icon = QIcon(picture_location)
            cell.setIcon(icon)

        # is text, parse accordingly to make visually clearer
        else:
            text = item_index

            # replace number with 'cutting' or 'blunt'
            if item_type == 'damage type':
                text = db_constants.DAMAGE_TYPES[item_index + 1]

            # replace number with 'balanced', 'melee', or 'boomerang
            elif item_type == 'balance type':
                text = db_constants.BALANCE_TYPES[item_index + 1]

            # list which charges the weapon has
            elif item_type == 'charges':
                charges = []

                # adjust each charge type to be more readable
                for x in text.split('|'):
                    if x != '':
                        y = x.split()
                        charges += [f"{y[0]:6} {y[1]:2}"]

                text = ' | '.join(charges)
                cell.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
                cell.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            # parse ammo string to see what ammo the gun has
            elif item_type == 'ammo':
                all_ammo = item_index.split('|')
                selected_ammo = []
                prev_ammo = 'Normal'

                # cycle through each shot type
                for count in range(len(db_constants.SHOT_TYPES)):
                    minimum_length = 11
                    ammo = all_ammo[count]
                    # if ammo != '':
                        # print(f"{db_constants.SHOT_TYPES[count]:11} {ammo}")
                    # check if gun can naturally load that ammo type
                    if len(ammo) > 1:
                        ammo_name = db_constants.SHOT_TYPES[count]
                        if prev_ammo != ammo_name.split()[0]:
                            prev_ammo = ammo_name.split()[0]
                            ammo_name = '\n' + ammo_name
                            minimum_length += 1
                        selected_ammo.append(f"{ammo_name:{minimum_length}}: {ammo.split('*')[0]:2}")

                # set text to monospace
                cell.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
                cell.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                text = ', '.join(selected_ammo)

            # align all the numbers to the right side
            elif item_type != 'name':
                cell.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            # apply text
            cell.setText(str(text))

        return cell

# Widget Class that takes in a sharpness value and draws rectangles to represent it
class SharpnessBar(QWidget):
    COLORS = [db_constants.SHARPNESS_TO_RGB[x] for x in db_constants.SHARPNESS_TYPES if x != 'any']
    HEIGHT = 30
    WIDTH_MULTIPLIER = 2

    # init, takes in a sharpness string from database
    def __init__(self, sharpness_str):
        super().__init__()

        # convert string to list
        self.sharpness = [int(x) for x in sharpness_str.split('.')]
        # print(self.sharpness)

    # draw the rectangles
    def paintEvent(self,e):
        p = QPainter(self)
        self.width = 0
        # keep track of position of xpos
        # i.e place next rectangle on the very right side
        x_pos = 0
        for s, c in zip(self.sharpness, self.COLORS):
            # don't create anything if sharpness is 0
            if s == 0:
                continue

            self.width += s * self.WIDTH_MULTIPLIER

            # get color
            color = QColor(c[0], c[1], c[2])

            # set color
            p.setPen(QPen(color))
            p.setBrush(QBrush(color, Qt.SolidPattern))

            # draw rectangle
            p.drawRect(x_pos, 0, s * self.WIDTH_MULTIPLIER, self.HEIGHT)

            # increment next place to place rectangle
            x_pos += s * self.WIDTH_MULTIPLIER

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MHDatabaseWindow()
    mainWin.show()
    sys.exit(app.exec_())