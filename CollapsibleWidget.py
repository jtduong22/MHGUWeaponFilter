from PyQt5 import QtWidgets

# simple collapsible widget class since PyQt doesn't have one by default
class CollapsibleWidget(QtWidgets.QWidget):
    # init widget
    def __init__(self, title="", parent=None):
        # init parent class
        super(CollapsibleWidget, self).__init__(parent)

        # create layout for widget
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        # create expand / collapse button
        self._toggle_button = QtWidgets.QToolButton(text=title)
        self._toggle_button.clicked.connect(self._toggle_widgets)
        main_layout.addWidget(self._toggle_button)

        # create collapsible layout
        # note: cannot adjust height of a layout directly, a container widget is needed
        self._container_layout = QtWidgets.QVBoxLayout()
        self._container_widget = QtWidgets.QWidget()
        self._container_widget.setLayout(self._container_layout)

        main_layout.addWidget(self._container_widget)

        self._is_hidden = False

    def get_item_at(self, index: int) -> QtWidgets.QWidget:
        item = self._container_layout.itemAt(index)

        if not isinstance(item, QtWidgets.QLayout):
            item = item.widget()
        return item

    def remove_item_at(self, index: int) -> None:
        widget = self.get_item_at(index)
        widget.setParent(None)

    def count(self) -> int:
        return self._container_layout.count()

    # hide / show all widgets based on self._is_hidden
    def _toggle_widgets(self) -> None:
        # if set to hide, set height to 0
        # else set height to default
        height = (0, self._container_layout.sizeHint().height(), )[self._is_hidden == True]

        # toggle _is_hidden
        self._is_hidden = not self._is_hidden

        # set height
        self._container_widget.setFixedHeight(height)

    # add widget
    def add_widget(self, widget):
        self._container_layout.addWidget(widget)

    # add layout
    def add_layout(self, layout):
        self._container_layout.addLayout(layout)

    # set toggled state
    def set_hidden(self, state: bool):
        if state != self._is_hidden:
            self._toggle_widgets()

    # return list of all widgets
    def get_widgets(self) -> list:
        return [self._container_layout.itemAt(x).widget() for x in range(self._container_layout.count())]

    def set_text(self, text: str) -> None:
        self._toggle_button.setText(text)

    def get_text(self) -> str:
        return self._toggle_button.text()