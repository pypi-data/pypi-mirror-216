import traceback

from PySide6.QtGui import QColor, QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QListWidget, QListWidgetItem, QAbstractItemView

from log_translate.data_struct import Log, Level
from log_translate.read_log_file import LogReader


def log_to_list_item(log: Log):
    item = QListWidgetItem(log.__str__())
    item.setForeground(QColor(log.level.color()))
    return item


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🤖日志解析")
        self.resize(400, 300)
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setAcceptDrops(True)
        self.setCentralWidget(self.list_widget)
        self.create_menu_bar()
        self.log_reader = LogReader()
        self.data_item_logs = {
            Level.d.value: [],
            Level.i.value: [],
            Level.w.value: [],
            Level.e.value: [],
        }
        self.log_reader.log_stream.subscribe_(lambda log: {
            self.collect_logs_and_show(log),
        })
        self.list_widget.addItem("💫 💭 把文件拖入到窗口开始解析日志 💭 💫")

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        action_menu = QMenu("操作", self)

        clear_action = QAction("Level_D", self)
        clear_action.setShortcut('Ctrl+D')
        clear_action.triggered.connect(self.filtter_logs_d)
        action_menu.addAction(clear_action)

        clear_action = QAction("Level_I", self)
        clear_action.setShortcut('Ctrl+I')
        clear_action.triggered.connect(self.filtter_logs_i)
        action_menu.addAction(clear_action)

        clear_action = QAction("Level_W", self)
        clear_action.setShortcut('Ctrl+W')
        clear_action.triggered.connect(self.filtter_logs_w)
        action_menu.addAction(clear_action)

        clear_action = QAction("Level_E", self)
        clear_action.setShortcut('Ctrl+E')
        clear_action.triggered.connect(self.filtter_logs_e)
        action_menu.addAction(clear_action)
        menu_bar.addMenu(action_menu)

    def clear_list(self):
        self.list_widget.clear()

    def add_line(self):
        self.list_widget.addItem("-" * 40)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            if not self.isMaximized():
                self.showMaximized()
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file = url.toLocalFile()
            # f-string 可以使用 {变量} 语法将表达式嵌入到字符串中
            self.list_widget.clear()
            self.list_widget.addItem(f"\n👇👇👇👇👇👇👇👇 {file} 💥 日志解析如下 👇👇👇👇👇👇👇👇")
            try:
                self.log_reader.concurrency([file])
            except:
                item = QListWidgetItem(traceback.format_exc())
                item.setForeground(QColor("red"))
                self.list_widget.addItem(item)

    def collect_logs_and_show(self, log: Log):
        for log_level in self.data_item_logs:
            if log.level.value >= log_level:
                self.data_item_logs[log_level].append(log)
        if log.level.value > Level.w.value:
            self.list_widget.addItem(log_to_list_item(log))

    def filtter_logs_d(self):
        self.filtter_logs(Level.d)

    def filtter_logs_i(self):
        self.filtter_logs(Level.i)

    def filtter_logs_w(self):
        self.filtter_logs(Level.w)

    def filtter_logs_e(self):
        self.filtter_logs(Level.e)

    def filtter_logs(self, level: Level):
        first = self.list_widget.item(0).text()
        self.list_widget.clear()
        self.list_widget.addItem(first)
        show_logs = self.data_item_logs[level.value]
        for log in show_logs:
            self.list_widget.addItem(log_to_list_item(log))


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

#  打包命令
# pyinstaller --name=log_translator --onefile --windowed ui_pyside2.py
# -F, --onefile   产生单个的可执行文件
# -n NAME, --name NAME   指定项目（产生的 spec）名字。如果省略该选项，那么第一个脚本的主文件名将作为 spec 的名字
# -w, --windowed, --noconsole   指定程序运行时不显示命令行窗口（仅对 Windows 有效）
# -i <FILE.ico>, --icon <FILE.ico>  指定icon

#  打包执行以下命令
# pyinstaller --hidden-import -n log_translator -F -w -i tools.ico ui_pyside2.py
# --hidden-import 设置导入要动态加载的类 因为没被引用 所以不会导入需要手动设置

# pip install PyInstaller
# pyinstaller --name=<your_exe_name> --onefile --windowed --add-data "<your_data_folder>;<your_data_folder>" <your_script_name>.py

# 上述命令中的选项说明：
# --name: 可执行文件名称。
# --onefile: 将整个项目打包为一个单独的可执行文件。
# --windowed: 隐藏控制台窗口，将打包的应用程序显示为GUI应用程序。
# --add-data: 添加项目资源，支持文件夹和文件，前面是资源路径，后面是输出路径，用分号进行分割。
# 执行上述命令后，会在项目目录下生成一个.spec文件，这个文件会告诉PyInstaller如何将项目打包成exe文件。
