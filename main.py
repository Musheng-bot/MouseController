import json
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QSpinBox, QDoubleSpinBox,
                             QFileDialog, QMessageBox, QListWidget, QListWidgetItem, QStyle)

from Player import MacroPlayer
from Recorder import MacroRecorder

class MouseMacroRecorder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.log_list = None
        self.loop_spin = None
        self.speed_spin = None
        self.status_label = None
        self.clear_btn = None
        self.load_btn = None
        self.save_btn = None
        self.play_btn = None
        self.record_btn = None

        self.setWindowTitle("鼠标宏录制软件")
        self.setGeometry(100, 100, 800, 600)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8fafc;
            }
            QLabel {
                color: #1e293b;
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
            QPushButton:disabled {
                background-color: #94a3b8;
                color: #e2e8f0;
            }
            QListWidget {
                border: 1px solid #cbd5e1;
                border-radius: 4px;
                background-color: white;
            }
            QListWidget::item {
                padding: 6px;
                border-bottom: 1px solid #e2e8f0;
            }
            QListWidget::item:selected {
                background-color: #dbeafe;
                color: #1e293b;
            }
            QLabel#status_label {
                font-weight: bold;
                color: #3b82f6;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.create_control_area()

        self.create_settings_area()

        self.create_log_area()

        self.macro_actions = []
        self.recorder = None
        self.player = None

        self.statusBar().showMessage("就绪")

        QMessageBox.information(
            self, "提示",
            "录制时按F8键停止录制\n"
            "播放时按F9键停止播放"
        )

    def create_control_area(self):
        control_widget = QWidget()
        control_layout = QHBoxLayout(control_widget)
        control_layout.setSpacing(10)

        self.record_btn = QPushButton("开始录制")
        self.record_btn.setIcon(QIcon('./Record.png'))
        self.record_btn.clicked.connect(self.toggle_recording)

        self.play_btn = QPushButton("开始播放")
        self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_btn.setEnabled(False)
        self.play_btn.clicked.connect(self.toggle_playback)

        self.save_btn = QPushButton("保存宏")
        self.save_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save_macro)

        self.load_btn = QPushButton("加载宏")
        self.load_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        self.load_btn.clicked.connect(self.load_macro)

        self.clear_btn = QPushButton("清除")
        self.clear_btn.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        self.clear_btn.setEnabled(False)
        self.clear_btn.clicked.connect(self.clear_macro)

        self.status_label = QLabel("状态: 就绪")
        self.status_label.setObjectName("status_label")

        control_layout.addWidget(self.record_btn)
        control_layout.addWidget(self.play_btn)
        control_layout.addWidget(self.save_btn)
        control_layout.addWidget(self.load_btn)
        control_layout.addWidget(self.clear_btn)
        control_layout.addStretch()
        control_layout.addWidget(self.status_label)

        self.main_layout.addWidget(control_widget)

    def create_settings_area(self):
        settings_widget = QWidget()
        settings_layout = QHBoxLayout(settings_widget)
        settings_layout.setSpacing(10)

        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("播放速度:"))

        self.speed_spin = QDoubleSpinBox()
        self.speed_spin.setRange(0.1, 10.0)
        self.speed_spin.setValue(1.0)
        self.speed_spin.setSingleStep(0.1)
        self.speed_spin.setSuffix("x")
        speed_layout.addWidget(self.speed_spin)

        loop_layout = QHBoxLayout()
        loop_layout.addWidget(QLabel("循环次数:"))

        self.loop_spin = QSpinBox()
        self.loop_spin.setRange(1, 1000)
        self.loop_spin.setValue(1)
        loop_layout.addWidget(self.loop_spin)

        settings_layout.addLayout(speed_layout)
        settings_layout.addLayout(loop_layout)
        settings_layout.addStretch()

        self.main_layout.addWidget(settings_widget)

    def create_log_area(self):
        log_widget = QWidget()
        log_layout = QVBoxLayout(log_widget)

        log_label = QLabel("操作记录:")
        log_layout.addWidget(log_label)

        self.log_list = QListWidget()
        log_layout.addWidget(self.log_list)

        self.main_layout.addWidget(log_widget, 1)

    def toggle_recording(self):
        if self.recorder and self.recorder.isRunning():
            self.recorder.stop_recording()
            self.record_btn.setText("开始录制")
            self.record_btn.setIcon(QIcon('./Record.png'))
            self.status_label.setText("状态: 就绪")
            self.statusBar().showMessage("录制已停止")
            self.play_btn.setEnabled(True)
            self.save_btn.setEnabled(True)
            self.clear_btn.setEnabled(True)
        else:
            self.log_list.clear()
            self.macro_actions = []
            self.recorder = MacroRecorder()
            self.recorder.recording_updated.connect(self.update_recording_log)
            self.recorder.recording_stopped.connect(self.on_recording_stopped)
            self.recorder.start()
            self.record_btn.setText("停止录制 (F8)")
            self.record_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
            self.play_btn.setEnabled(False)
            self.save_btn.setEnabled(False)
            self.clear_btn.setEnabled(False)
            self.status_label.setText("状态: 录制中...")
            self.statusBar().showMessage("开始录制，请进行操作...")

    def toggle_playback(self):
        if self.player and self.player.isRunning():
            self.player.stop_playback()
            self.play_btn.setText("开始播放")
            self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.status_label.setText("状态: 就绪")
            self.statusBar().showMessage("播放已停止")
            self.record_btn.setEnabled(True)
            self.save_btn.setEnabled(True)
        else:
            if not self.macro_actions:
                QMessageBox.warning(self, "警告", "没有可播放的宏记录")
                return

            self.log_list.clear()
            speed = self.speed_spin.value()
            loops = self.loop_spin.value()

            self.player = MacroPlayer(self.macro_actions, speed, loops)
            self.player.progress_updated.connect(self.update_playback_log)
            self.player.playback_finished.connect(self.on_playback_finished)
            self.player.start()
            self.play_btn.setText("停止播放 (F9)")
            self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
            self.record_btn.setEnabled(False)
            self.save_btn.setEnabled(False)
            self.status_label.setText(f"状态: 播放中 ({speed}x, {loops}次)")
            self.statusBar().showMessage("开始播放宏...")

    def update_recording_log(self, message):
        self.log_list.addItem(message)
        self.log_list.scrollToBottom()

    def update_playback_log(self, message):
        item = QListWidgetItem(message)
        item.setForeground(QColor("#1e40af"))
        self.log_list.addItem(item)
        self.log_list.scrollToBottom()

    def on_recording_stopped(self, actions):
        self.macro_actions = actions
        self.log_list.addItem(f"录制完成，共记录 {len(actions)} 个操作")
        self.statusBar().showMessage(f"录制完成，共记录 {len(actions)} 个操作")

    def on_playback_finished(self):
        self.play_btn.setText("开始播放")
        self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.status_label.setText("状态: 就绪")
        self.statusBar().showMessage("宏播放完成")
        self.record_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.log_list.addItem("宏播放完成")

    def save_macro(self):
        if not self.macro_actions:
            QMessageBox.warning(self, "警告", "没有可保存的宏记录")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存宏", "", "宏文件 (*.macro);;所有文件 (*)"
        )

        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.macro_actions, f)
                self.statusBar().showMessage(f"宏已保存到: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存宏时出错: {str(e)}")

    def load_macro(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开宏", "", "宏文件 (*.macro);;所有文件 (*)"
        )

        if file_path:
            try:
                with open(file_path, 'r') as f:
                    self.macro_actions = json.load(f)

                self.log_list.clear()
                self.log_list.addItem(f"已加载宏，包含 {len(self.macro_actions)} 个操作")
                self.play_btn.setEnabled(True)
                self.save_btn.setEnabled(True)
                self.clear_btn.setEnabled(True)
                self.statusBar().showMessage(f"已加载宏: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"加载宏时出错: {str(e)}")

    def clear_macro(self):
        reply = QMessageBox.question(
            self, "确认", "确定要清除当前宏记录吗？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.macro_actions = []
            self.log_list.clear()
            self.play_btn.setEnabled(False)
            self.save_btn.setEnabled(False)
            self.clear_btn.setEnabled(False)
            self.statusBar().showMessage("宏记录已清除")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F9 and self.player and self.player.isRunning():
            self.toggle_playback()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    font = app.font()
    font.setFamily("SimHei")
    app.setFont(font)

    window = MouseMacroRecorder()
    window.show()
    sys.exit(app.exec_())