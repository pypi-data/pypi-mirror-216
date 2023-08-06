import os

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit, QFileDialog, QLabel, QTableWidget

from InfixToPostfix.infix_to_postfix import InfixToPostfix

STYLE_QSS_PATH = os.path.join(os.path.dirname(__file__), "data/style.qss")


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("后缀表达式生成器")
        self.setStyleSheet(open(STYLE_QSS_PATH).read())
        self.resize(1280, 720)
        self.conf = ""

        self.file_chooser = QPushButton("选取配置文件")
        self.file_chooser.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.file_chooser.clicked.connect(self.file_chooser_connect)

        self.conf_process = QPushButton("分析")
        self.conf_process.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.conf_process.clicked.connect(self.conf_process_connect)

        self.init_layout()

        # 配置 conf_window 和 result_window
        self.conf_window = self.init_conf_window()
        self.result_window = self.init_result_window()

        self.data = InfixToPostfix()

        self.show()

    def init_layout(self):

        grid = QGridLayout()

        grid.addWidget(self.file_chooser, 0, 0, 1, 1)
        grid.addWidget(self.conf_process, 0, 1, 1, 1)

        self.setLayout(grid)

    def init_conf_window(self):
        conf_result = QTableWidget()
        conf_result.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        conf_result.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        conf_result.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        conf_result.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        expression = QLineEdit()
        expression.setPlaceholderText("输入表达式")
        expression.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        expression.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        analyze_process = QPushButton("提交")
        analyze_process.clicked.connect(lambda: self.analyze_process_connect(expression.text()))
        analyze_process.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        return ChildWindow("配置结果", conf_result, expression, analyze_process)

    def init_result_window(self):
        analyze_result = QTableWidget()
        analyze_result.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        analyze_result.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        analyze_result.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        analyze_result.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        raw = QLabel(f"中缀表达式")
        raw.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        raw.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        now = QLabel(f"后缀表达式")
        now.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        now.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        return ChildWindow("分析结果", analyze_result, raw, now)

    def file_chooser_connect(self):
        self.conf = QFileDialog().getOpenFileName(self, "选取配置文件", "./", "All Files (*)")[0]
        self.file_chooser.setText(self.conf)

    def conf_process_connect(self):
        self.data = InfixToPostfix() if self.conf == "" else InfixToPostfix(self.conf)
        priority_table = self.data.priority_table

        # 更新 conf_window
        length = len(priority_table.keys())
        self.conf_window.widget1.setRowCount(length)
        self.conf_window.widget1.setColumnCount(length)
        row_headers = list(priority_table.keys())
        column_headers = list(priority_table[row_headers[0]].keys())
        self.conf_window.widget1.setVerticalHeaderLabels(row_headers)
        self.conf_window.widget1.setHorizontalHeaderLabels(column_headers)
        conf_result = self.conf_window.widget1
        conf_result.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        conf_result.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        conf_result.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        conf_result.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        for i, key_left in enumerate(priority_table.keys()):
            for j, key_right in enumerate(priority_table[key_left].keys()):
                item = QtWidgets.QTableWidgetItem(priority_table[key_left][key_right])
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                conf_result.setItem(i, j, item)

        self.conf_window.widget2.setText("")
        self.conf_window.show()

    def analyze_process_connect(self, expression):
        result, words, actions, stack_states, words_states = self.data.analyze(expression)

        # 更新 result_window
        self.result_window.widget1.setRowCount(len(actions))
        self.result_window.widget1.setColumnCount(3)
        analyze_result = self.result_window.widget1
        for i, action, stack_state, words_state in zip(range(len(actions)), actions, stack_states, words_states):
            item0, item1, item2 = QtWidgets.QTableWidgetItem(action), QtWidgets.QTableWidgetItem(stack_state), QtWidgets.QTableWidgetItem(words_state)
            item0.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item1.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item2.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            analyze_result.setItem(i, 0, item0)
            analyze_result.setItem(i, 1, item1)
            analyze_result.setItem(i, 2, item2)

        self.result_window.widget2.setText(f"中缀表达式   {' '.join([word[1] for word in words])}")
        self.result_window.widget3.setText(f"后缀表达式   {' '.join(result)}")

        self.result_window.show()


class ChildWindow(QWidget):

    def __init__(self, title, widget1, widget2, widget3):
        super().__init__()
        self.setStyleSheet(open(STYLE_QSS_PATH).read())
        self.setWindowTitle(title)
        self.resize(1280, 720)
        self.widget1 = widget1
        self.widget2 = widget2
        self.widget3 = widget3
        self.init_layout()

    def init_layout(self):
        grid = QGridLayout()
        grid.addWidget(self.widget1, 0, 0, 4, 2)
        grid.addWidget(self.widget2, 4, 0)
        grid.addWidget(self.widget3, 4, 1)
        for i in range(grid.rowCount()):
            grid.setRowStretch(i, 1)
        for i in range(grid.columnCount()):
            grid.setRowStretch(i, 1)
        self.setLayout(grid)
