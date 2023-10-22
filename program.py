import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction,\
      QLabel, QVBoxLayout, QWidget, QDateTimeEdit, QSizePolicy, QScrollArea,\
        QLineEdit, QPushButton, QComboBox, QMessageBox, QGraphicsRectItem, QGraphicsScene, QGraphicsView, QInputDialog
from PyQt5.QtGui import QPixmap, QColor, QFont, QPen
from PyQt5.QtCore import Qt

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.heroes = {}
        self.player_name_edit = None
        self.player_position_x_edit = None
        self.player_position_y_edit = None
        self.player_datetime_edit = None
        self.selected_character = None
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        self.initUI()

    def reset_ui(self):
        current_central_widget = self.centralWidget()
        if current_central_widget:
            current_central_widget.deleteLater()
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        
        map_label = QLabel(self)
        pixmap = QPixmap('map.jpg')
        map_label.setPixmap(pixmap)
        
        scroll_area = QScrollArea()
        scroll_area.setWidget(map_label)
        
        central_widget.setLayout(layout)
        layout.addWidget(scroll_area)


    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        map_label = QLabel(self)
        pixmap = QPixmap('map.jpg')
        map_label.setPixmap(pixmap)

        scroll_area = QScrollArea()
        scroll_area.setWidget(map_label)

        central_widget.setLayout(layout)
        layout.addWidget(scroll_area)

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        main_menu_action = QAction('Основное меню', self)
        main_menu_action.triggered.connect(self.show_main_menu)
        self.toolbar.addAction(main_menu_action)

        add_character_action = QAction('Добавить персонажа', self)
        add_character_action.triggered.connect(self.add_character)
        self.toolbar.addAction(add_character_action)

        add_geometry_action = QAction('Добавить геометку', self)
        add_geometry_action.triggered.connect(self.add_geometry)
        self.toolbar.addAction(add_geometry_action)

        view_all_action = QAction('Посмотреть на всех', self)
        view_all_action.triggered.connect(self.view_all)
        self.toolbar.addAction(view_all_action)

        view_character_action = QAction('Смотреть на персонажа', self)
        view_character_action.triggered.connect(self.view_character)
        self.toolbar.addAction(view_character_action)

        self.mouse_coords_label = QLabel('X:  Y:', self)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(spacer)
        self.toolbar.addWidget(self.mouse_coords_label)

        self.setMouseTracking(True)
        self.mousePressEvent = self.update_mouse_coords

        self.setGeometry(100, 100, 1100, 760)
        self.setWindowTitle('Приложение с фоновым изображением и кнопками')

    def add_character(self):
        current_central_widget = self.centralWidget()
        if current_central_widget:
            current_central_widget.deleteLater()
        
        central_widget = QWidget(self)
        
        player_name_label = QLabel('Имя игрока:', self)
        self.player_name_edit = QLineEdit(self)
        player_position_label_x = QLabel('Изначальная позиция X:', self)
        self.player_position_x_edit = QLineEdit(self)
        player_position_label_y = QLabel('Изначальная позиция Y:', self)
        self.player_position_y_edit = QLineEdit(self)
        player_datetime_label = QLabel('Дата и время:', self)
        self.player_datetime_edit = QDateTimeEdit(self)
        confirm_button = QPushButton('Подтвердить', self)
        confirm_button.clicked.connect(self.confirm_character)

        character_layout = QVBoxLayout()
        character_layout.addWidget(player_name_label)
        character_layout.addWidget(self.player_name_edit)
        character_layout.addWidget(player_position_label_x)
        character_layout.addWidget(self.player_position_x_edit)
        character_layout.addWidget(player_position_label_y)
        character_layout.addWidget(self.player_position_y_edit)
        character_layout.addWidget(player_datetime_label)
        character_layout.addWidget(self.player_datetime_edit)
        character_layout.addWidget(confirm_button)

        self.centralWidget().setLayout(character_layout)
        self.setCentralWidget(central_widget)
        central_widget.setLayout(character_layout)

    def confirm_character(self):
        player_name = self.player_name_edit.text()
        player_x = self.player_position_x_edit.text()
        player_y = self.player_position_y_edit.text()
        date_time = self.player_datetime_edit.dateTime()

        try:
            player_x = int(player_x)
            player_y = int(player_y)
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Введите целые числа для координат X и Y')
            return

        if player_x < 0 or player_x > 1083 or player_y < 0 or player_y > 744:
            QMessageBox.warning(self, 'Ошибка', 'Координаты должны быть в пределах 1-1083 для X и 1-744 для Y')
            return

        if player_name in self.heroes:
            QMessageBox.warning(self, 'Ошибка', 'Игрок с таким именем уже существует')
            return

        if player_name:
            self.heroes[player_name] = [(player_x, player_y, date_time)]

            message = f'Игрок {player_name} добавлен на дату: {date_time.toString("hh:mm dd.MM.yyyy")} на координаты X: {player_x}, Y: {player_y}.'
            QMessageBox.information(self, 'Добавление игрока', message)

            self.reset_ui()
            
    def add_geometry(self):
        current_central_widget = self.centralWidget()
        if current_central_widget:
            current_central_widget.deleteLater()

        character_label = QLabel('Выберите персонажа:', self)
        character_combobox = QComboBox(self)
        character_combobox.addItem('Выберите персонажа...')
        character_combobox.addItems(self.heroes.keys())

        select_character_button = QPushButton('Выбрать', self)
        select_character_button.clicked.connect(self.select_character_for_geometry)

        character_layout = QVBoxLayout()
        character_layout.addWidget(character_label)
        character_layout.addWidget(character_combobox)
        character_layout.addWidget(select_character_button)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setLayout(character_layout)

    def select_character_for_geometry(self):
        selected_character = self.centralWidget().layout().itemAt(1).widget().currentText()

        if selected_character == 'Выберите персонажа...':
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, выберите персонажа.')
            return

        character_combobox = self.centralWidget().layout().itemAt(1).widget()
        character_combobox.deleteLater()
        self.centralWidget().layout().itemAt(0).widget().deleteLater()

        geometry_position_label_x = QLabel('Местоположение X:', self)
        self.player_position_x_edit = QLineEdit(self)
        geometry_position_label_y = QLabel('Местоположение Y:', self)
        self.player_position_y_edit = QLineEdit(self)
        geometry_datetime_label = QLabel('Дата и время:', self)
        self.player_datetime_edit = QDateTimeEdit(self)

        add_geometry_button = QPushButton('Добавить', self)
        add_geometry_button.clicked.connect(self.add_geometry_for_character)

        geometry_layout = QVBoxLayout()
        geometry_layout.addWidget(geometry_position_label_x)
        geometry_layout.addWidget(self.player_position_x_edit)
        geometry_layout.addWidget(geometry_position_label_y)
        geometry_layout.addWidget(self.player_position_y_edit)
        geometry_layout.addWidget(geometry_datetime_label)
        geometry_layout.addWidget(self.player_datetime_edit)
        geometry_layout.addWidget(add_geometry_button)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setLayout(geometry_layout)
        self.selected_character = selected_character

    def add_geometry_for_character(self):
        geometry_x = self.player_position_x_edit.text()
        geometry_y = self.player_position_y_edit.text()
        geometry_datetime = self.player_datetime_edit.dateTime()

        try:
            geometry_x = int(geometry_x)
            geometry_y = int(geometry_y)
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Введите целые числа для координат X и Y')
            return

        if geometry_x < 0 or geometry_x > 1083 or geometry_y < 0 or geometry_y > 744:
            QMessageBox.warning(self, 'Ошибка', 'Координаты должны быть в пределах 0-1083 для X и 0-744 для Y')
            return

        message = f'Геометка добавлена для персонажа "{self.selected_character}" на координаты X: {geometry_x}, Y: {geometry_y} в {geometry_datetime.toString("hh:mm dd.MM.yyyy")}.'
        QMessageBox.information(self, 'Добавление геометки', message)

        self.heroes[self.selected_character].append((geometry_x, geometry_y, geometry_datetime))
        self.reset_ui()

    def view_all(self):
        if not self.heroes:
            QMessageBox.warning(self, 'Ошибка', 'Нет доступных персонажей для просмотра.')
            return

        scene = QGraphicsScene()

        map_pixmap = QPixmap('map.jpg')
        map_item = scene.addPixmap(map_pixmap)
        r, g, b = 255, 0, 0
        for character, data in self.heroes.items():
            sorted_data = sorted(data, key=lambda x: x[2])
            if sorted_data:
                last_point = sorted_data[-1]
                x, y, date_time = last_point[0], last_point[1], last_point[2]

                rect = QGraphicsRectItem(x, y, 100, 37)
                rect.setBrush(QColor(255, 0, 0))
                scene.addItem(rect)
                scene.addText(f'\"{character}\"\nX={x}, Y={y}', QFont("Arial", 10, QFont.Bold)).setPos(x + 5, y + 5)

        view = QGraphicsView(scene)
        self.setCentralWidget(view)

    def view_character(self):
        if not self.heroes:
            QMessageBox.warning(self, 'Ошибка', 'Нет доступных персонажей для просмотра.')
            return

        character_name, ok = QInputDialog.getItem(self, 'Выберите персонажа', 'Выберите персонажа для просмотра:', self.heroes.keys(), 0, False)
        if not ok:
            return

        data = self.heroes[character_name]
        sorted_data = sorted(data, key=lambda x: x[2])

        scene = QGraphicsScene()

        map_pixmap = QPixmap('map.jpg')
        scene.addPixmap(map_pixmap)

        prev_x, prev_y = None, None
        for point in sorted_data:
            x, y, date_time = point[0], point[1], point[2]

            ellipse = scene.addEllipse(x - 5, y - 5, 10, 10, QColor(255, 0, 0), QColor(255, 0, 0))
            ellipse.setBrush(QColor(255, 0, 0))

            if prev_x is not None and prev_y is not None:
                line = scene.addLine(prev_x, prev_y, x, y, Qt.black)
                line.setPen(QPen(QColor(255, 0, 0), 3, Qt.SolidLine))
            prev_x, prev_y = x, y

        view = QGraphicsView(scene)
        self.setCentralWidget(view)


    def update_mouse_coords(self, event):
        x = event.x()
        y = event.y()
        self.mouse_coords_label.setText(f'X: {x}  Y: {y}')

    def show_main_menu(self):
        self.reset_ui()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
