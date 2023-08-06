import ujson as json
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *
import sys
import jsonschema

class choose_setting(QComboBox):
    def __init__(self,setting: dict , page: str, name: str, schema: dict, check_func):
        super().__init__()
        self.setting , self.page, self.schema, self.name,self.check_func = setting , page, schema, name, check_func
        # self.addItems(self.schema['item_list'])
        j = 0
        for i in self.schema['item_list']:
            self.addItem(i)
            if i == self.setting[self.page][self.name]:
                self.setCurrentIndex(j)
            j += 1
        self.currentTextChanged.connect(self.change)
        self.setMinimumHeight(20)
        if 'description' in self.schema:
            self.setToolTip(self.tr((self.schema['description'] + f"(default:{self.schema['default']})")))
    def change(self):
        self.setting[self.page][self.name] = self.currentText()
        self.check_func()

class bool_setting(QCheckBox):
    def __init__(self,setting: dict , page: str, name: str, schema: dict, check_func):
        super().__init__()
        self.setting , self.page, self.schema, self.name,self.check_func = setting , page, schema, name, check_func
        self.setChecked(self.setting[self.page][self.name])
        self.setText(self.tr(self.schema['title']))
        if 'description' in self.schema:
            self.setToolTip(self.tr(self.schema['description'] + f"(default:{self.schema['default']})"))

        self.stateChanged.connect(self.change)
    def change(self):
        self.setting[self.page][self.name] = self.isChecked()
        self.check_func()
    
class str_setting(QLineEdit):
    def __init__(self,setting: dict , page: str, name: str, schema: dict, check_func):
        super().__init__()
        self.setting , self.page, self.schema, self.name,self.check_func = setting , page, schema, name, check_func
        self.setText(self.tr(self.setting[self.page][self.name]))
        self.textEdited.connect(self.change)
        self.setMinimumHeight(20)
        if 'description' in self.schema:
            self.setToolTip(self.tr((self.schema['description'] + f"(default:{self.schema['default']})")))
    def change(self):
        self.setting[self.page][self.name] = self.text()
        self.check_func()

class int_setting(QLineEdit):
    def __init__(self,setting: dict , page: str, name: str, schema: dict, check_func):
        super().__init__()
        self.setting , self.page, self.schema, self.name,self.check_func = setting , page, schema, name, check_func
        self.setText(str(self.setting[self.page][self.name]))
        self.textEdited.connect(self.change)
        self.setMinimumHeight(20)
        if 'description' in self.schema:
            self.setToolTip(self.tr((self.schema['description'] + f"(default:{self.schema['default']})")))
    def change(self):
        self.setting[self.page][self.name] = int(self.text())
        self.check_func()

class setting_widget(QWidget):
    def __init__(self,setting: dict , page: str, name: str,schema: dict):
        super().__init__()
        self.setting , self.page, self.name, self.schema, self.type = setting , page, name, schema, schema['type']

        self.main_layout = QVBoxLayout(self)
        self.err_msg = QLabel(self)
        self.err_msg.setStyleSheet('color: red;')
        
        self.setLayout(self.main_layout)

        if self.type == 'boolean':
            self.main_layout.addWidget(
                    bool_setting(self.setting, self.page, self.name, self.schema, self.check)
            )
        elif self.type == 'string':
            name_label = QLabel()
            name_label.setText(self.tr(self.schema['title']))
            self.main_layout.addWidget(name_label)
            if 'item_list' in self.schema:
                self.main_layout.addWidget(
                    choose_setting(self.setting, self.page, self.name, self.schema, self.check)
                )
            else:
                self.main_layout.addWidget(
                    str_setting(self.setting, self.page, self.name, self.schema, self.check)
                )
        elif self.type == 'integer':
            name_label = QLabel()
            name_label.setText(self.tr(self.schema['title']))
            self.main_layout.addWidget(name_label)
            self.main_layout.addWidget(
                int_setting(self.setting, self.page, self.name, self.schema, self.check)
            )
        self.main_layout.addWidget(self.err_msg)
    def check(self):
        try:
            jsonschema.validate(self.setting[self.page][self.name], self.schema)
            self.err_msg.clear()
            return True
        except jsonschema.exceptions.ValidationError as err: # 捕捉错误
            self.err_msg.setText(str(err).split("\n")[0])

class seting_window(QWidget):
    def __init__(self, json_path: str, json_schema_path: str):
        super().__init__()
        # 读取文件
        self.json_path = json_path
        with open(json_path, 'r') as f:
            self.setting: dict = json.decode(f.read())
        with open(json_schema_path, 'r') as f:
            self.json_schema = json.decode(f.read())

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.setting_page_widget = QTabWidget(self)
        self.main_layout.addWidget(self.setting_page_widget)
        self.setting_page = {}

        self.btns = QHBoxLayout(self)
        self.main_layout.addLayout(self.btns)
        self.btns.addStretch(1)
        self.appely_btn = QPushButton(text = self.tr('appely'))
        self.appely_btn.clicked.connect(self.save)
        self.close_btn = QPushButton(text = self.tr('close'))
        self.close_btn.clicked.connect(sys.exit)
        self.ok_btn = QPushButton(text = self.tr('ok'))
        self.ok_btn.clicked.connect(lambda: self.save(close=True))
        self.btns.addWidget(self.appely_btn)
        self.btns.addWidget(self.close_btn)
        self.btns.addWidget(self.ok_btn)

        for page, setting in self.setting.items():
            self.setting_page[page] = QScrollArea()
            tab_widget = QWidget()
            self.setting_page[page].setWidget(tab_widget)
            self.setting_page[page].setWidgetResizable(True)
            page_layout = QVBoxLayout(self.setting_page[page])
            tab_widget.setLayout(page_layout)
            self.setting_page_widget.addTab(self.setting_page[page], self.tr(self.json_schema['properties'][page]['title']))
            for name in setting:
                _schema = self.json_schema['properties'][page]['properties'][name]
                page_layout.addWidget(setting_widget(self.setting, page, name,_schema))

    def save(self, close=False):
        with open(self.json_path, 'w') as f:
            f.write(json.encode(self.setting))
        if close:
            sys.exit()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = seting_window('./example/example.json', './example/example-schema.json')
    win.show()
    app.exec_()