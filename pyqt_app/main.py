import argparse
import sys
from dataclasses import dataclass

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


@dataclass
class SensorSample:
    name: str
    area: str
    temperature: float
    humidity: float
    temp_alarm: bool = False
    humid_alarm: bool = False


SAMPLE_DATA = [
    SensorSample("一号库房", "A区", 21.6, 45.2),
    SensorSample("二号库房", "A区", 28.4, 71.0, temp_alarm=True, humid_alarm=True),
    SensorSample("制剂间", "B区", 23.2, 48.8),
    SensorSample("原料间", "B区", 19.1, 40.2),
    SensorSample("冷链区", "C区", 5.7, 67.9),
]


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("登录")
        self.setModal(True)
        self.setMinimumWidth(360)

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(12)

        title = QLabel("鸿软温湿度监测系统 · PyQt")
        title.setObjectName("loginTitle")
        root.addWidget(title)

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("用户名")
        self.username_edit.setText("admin")
        root.addWidget(self.username_edit)

        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("密码")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setText("admin123")
        root.addWidget(self.password_edit)

        button_row = QHBoxLayout()
        button_row.addStretch(1)
        login_btn = QPushButton("登录")
        login_btn.clicked.connect(self._try_login)
        button_row.addWidget(login_btn)
        root.addLayout(button_row)

    def _try_login(self):
        if self.username_edit.text().strip() == "admin" and self.password_edit.text() == "admin123":
            self.accept()
            return
        QMessageBox.warning(self, "登录失败", "用户名或密码错误（演示版本仅支持 admin/admin123）")


class SensorCard(QFrame):
    def __init__(self, sample: SensorSample, parent=None):
        super().__init__(parent)
        self.setObjectName("sensorCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)

        name = QLabel(sample.name)
        name.setObjectName("sensorName")
        layout.addWidget(name)

        temp = QLabel(f"温度：{sample.temperature:.1f} ℃")
        humid = QLabel(f"湿度：{sample.humidity:.1f} %RH")
        temp.setObjectName("alarmValue" if sample.temp_alarm else "normalValue")
        humid.setObjectName("alarmValue" if sample.humid_alarm else "normalValue")

        layout.addWidget(temp)
        layout.addWidget(humid)
        layout.addStretch(1)


class PlaceholderPage(QWidget):
    def __init__(self, title: str, desc: str, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        title_label = QLabel(title)
        title_label.setObjectName("pageTitle")
        desc_label = QLabel(desc)
        desc_label.setWordWrap(True)
        desc_label.setObjectName("pageDesc")
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch(1)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("鸿软温湿度监测系统 - PyQt 版本")
        self.resize(1280, 820)

        root = QWidget()
        self.setCentralWidget(root)
        outer = QHBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        side_layout = QVBoxLayout(self.sidebar)
        side_layout.setContentsMargins(14, 18, 14, 14)
        side_layout.setSpacing(8)

        title = QLabel("温湿度监测")
        title.setObjectName("brandTitle")
        side_layout.addWidget(title)

        self.stack = QStackedWidget()

        self.dashboard = self._build_dashboard_page()
        self.data_query = PlaceholderPage("数据查询", "保留原 Qt 版本的数据列表、统计、曲线和导出能力；此处为 PyQt 页面骨架。")
        self.alarm = PlaceholderPage("系统报警", "保留原报警分页与处理逻辑；此处为 PyQt 页面骨架。")
        self.floor_plan = PlaceholderPage("设置平面图", "保留原平面图上传、拖拽布点能力；此处为 PyQt 页面骨架。")
        self.settings = PlaceholderPage("系统设定", "保留设备管理、用户管理、参数配置入口；此处为 PyQt 页面骨架。")
        self.site = PlaceholderPage("切换站点", "保留多站点配置与切换逻辑；此处为 PyQt 页面骨架。")
        self.logs = PlaceholderPage("日志查询", "保留原日志时间范围筛选与表格展示能力；此处为 PyQt 页面骨架。")

        pages = [
            ("实时监控", self.dashboard),
            ("数据查询", self.data_query),
            ("系统报警", self.alarm),
            ("设置平面图", self.floor_plan),
            ("系统设定", self.settings),
            ("切换站点", self.site),
            ("日志查询", self.logs),
        ]

        for i, (name, page) in enumerate(pages):
            self.stack.addWidget(page)
            btn = QPushButton(name)
            btn.setCheckable(True)
            if i == 0:
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, idx=i: self._switch_page(idx))
            side_layout.addWidget(btn)

        side_layout.addStretch(1)

        logout = QPushButton("退出登录")
        logout.clicked.connect(self.close)
        side_layout.addWidget(logout)

        container = QFrame()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(18, 18, 18, 18)

        header = QLabel("鸿软温湿度监测系统 · PyQt UI 优化演示")
        header.setObjectName("headerTitle")
        header.setFont(QFont("Microsoft YaHei", 13, QFont.Weight.DemiBold))
        container_layout.addWidget(header)
        container_layout.addWidget(self.stack, 1)

        status = QLabel("状态：演示页面已加载，支持后续接入数据库与串口采集。")
        status.setObjectName("statusText")
        container_layout.addWidget(status)

        outer.addWidget(self.sidebar)
        outer.addWidget(container, 1)

    def _switch_page(self, index: int):
        self.stack.setCurrentIndex(index)
        for i in range(self.sidebar.layout().count()):
            item = self.sidebar.layout().itemAt(i)
            widget = item.widget()
            if isinstance(widget, QPushButton) and widget.isCheckable():
                widget.setChecked(i - 1 == index)

    def _build_dashboard_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(8, 8, 8, 8)

        tabs = QTabWidget()
        tabs.setDocumentMode(True)

        all_areas = sorted({d.area for d in SAMPLE_DATA})
        area_names = ["全部"] + all_areas

        for area in area_names:
            area_widget = QWidget()
            grid = QGridLayout(area_widget)
            grid.setContentsMargins(8, 8, 8, 8)
            grid.setHorizontalSpacing(12)
            grid.setVerticalSpacing(12)

            filtered = SAMPLE_DATA if area == "全部" else [d for d in SAMPLE_DATA if d.area == area]
            for idx, sample in enumerate(filtered):
                card = SensorCard(sample)
                card.setMinimumWidth(230)
                grid.addWidget(card, idx // 3, idx % 3)

            grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            tabs.addTab(area_widget, area)

        layout.addWidget(tabs)
        return page


def apply_theme(app: QApplication):
    app.setStyleSheet(
        """
        QWidget {
            background: #f5f7fb;
            color: #1b2230;
            font-family: "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
            font-size: 13px;
        }
        QFrame#sidebar {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #1f3c88, stop:1 #285a9c);
            min-width: 190px;
            max-width: 210px;
            border-right: 1px solid rgba(255,255,255,0.08);
        }
        QLabel#brandTitle {
            color: #ffffff;
            font-size: 20px;
            font-weight: 700;
            margin: 0 0 10px 2px;
        }
        QLabel#headerTitle {
            color: #234274;
            font-size: 20px;
            padding: 6px 2px 12px 2px;
        }
        QPushButton {
            border: 0;
            border-radius: 10px;
            padding: 8px 12px;
            text-align: left;
            background: rgba(255, 255, 255, 0.12);
            color: #ffffff;
            font-weight: 500;
        }
        QFrame QPushButton:hover {
            background: rgba(255, 255, 255, 0.2);
        }
        QFrame QPushButton:checked {
            background: #ffffff;
            color: #1f3c88;
        }
        QLabel#statusText {
            color: #5f6f87;
            background: #ffffff;
            border: 1px solid #dce3ef;
            border-radius: 10px;
            padding: 10px 12px;
        }
        QFrame#sensorCard {
            background: #ffffff;
            border-radius: 12px;
            border: 1px solid #d8e2f0;
        }
        QLabel#sensorName {
            color: #2a3f66;
            font-size: 15px;
            font-weight: 700;
        }
        QLabel#normalValue {
            color: #2e7d32;
            font-size: 14px;
            font-weight: 600;
        }
        QLabel#alarmValue {
            color: #d63031;
            font-size: 14px;
            font-weight: 700;
        }
        QTabWidget::pane {
            border: 0;
            top: -2px;
        }
        QTabBar::tab {
            background: #e7edf8;
            border-radius: 8px;
            padding: 8px 14px;
            margin-right: 8px;
            color: #325289;
            font-weight: 600;
        }
        QTabBar::tab:selected {
            background: #325289;
            color: #ffffff;
        }
        QLineEdit {
            background: #ffffff;
            border: 1px solid #d5dfef;
            border-radius: 8px;
            padding: 8px 10px;
            color: #22314b;
        }
        QLabel#loginTitle {
            font-size: 16px;
            font-weight: 700;
            color: #234274;
        }
        QLabel#pageTitle {
            font-size: 22px;
            font-weight: 700;
            color: #2a3f66;
        }
        QLabel#pageDesc {
            font-size: 14px;
            color: #556b8a;
            line-height: 1.5;
        }
        """
    )
    pal = app.palette()
    pal.setColor(pal.ColorRole.Window, QColor("#f5f7fb"))
    app.setPalette(pal)


def run_app(save_screenshot: str | None = None) -> int:
    app = QApplication(sys.argv)
    apply_theme(app)

    if not save_screenshot:
        login = LoginDialog()
        if login.exec() != QDialog.DialogCode.Accepted:
            return 0

    window = MainWindow()
    window.show()

    if save_screenshot:
        app.processEvents()
        window.grab().save(save_screenshot)
        return 0

    return app.exec()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="鸿软温湿度监测系统 PyQt UI 演示")
    parser.add_argument("--screenshot", help="可选：保存主界面截图到指定路径")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    raise SystemExit(run_app(args.screenshot))
