import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtGui import QColor, QPalette, QKeyEvent
from PyQt5.QtCore import Qt
import openai
import time

openai.api_base = "https://api.aiproxy.io/v1"
openai.api_key = 'sk-7Ygy0UKHghtmHl5xh869lPX0O7xkwe84tm568Ij4gXjtalGU'

class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat-Gpt网安智能分析系统 山西警院 昏睡红茶队")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(0.9)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        layout.addWidget(self.chat_history)

        self.user_input = QLineEdit()
        self.user_input.returnPressed.connect(self.send_message)
        layout.addWidget(self.user_input)

        self.minimize_button = QPushButton("最小化")
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setStyleSheet("background-color: rgba(135, 206, 250, 0.7); color: white;")
        layout.addWidget(self.minimize_button)

        self.send_button = QPushButton("发送")
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setStyleSheet("background-color: rgba(135, 206, 250, 0.7); color: white;")
        layout.addWidget(self.send_button)

        self.close_button = QPushButton("关闭")
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("background-color: rgba(135, 206, 250, 0.7); color: white;")
        layout.addWidget(self.close_button)

        self.message_log = []  # 存储对话历史

        self.chat_history.append("智能网安: 你好，请说出您想要的问题。")

        self.draggable = False
        self.offset = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = False
            self.offset = None

    def send_message(self):
        user_message = self.user_input.text()
        self.user_input.clear()
        self.display_message("You: " + user_message)

        self.message_log.append({"role": "system", "content": "You are a cybersecurity expert."})
        self.message_log.append({"role": "user", "content": user_message})  # 记录用户消息

        response = self.get_gpt_response()
        self.display_message_chars("智能网安: " + response)

    def get_gpt_response(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.message_log,
            max_tokens=1000,
            temperature=0.7,
            n=1,
            stop=None,
            timeout=5
        )

        return response.choices[0].message.content.strip()

    def display_message_chars(self, message):
        self.chat_history.setTextColor(QColor(0, 0, 255))
        self.chat_history.insertPlainText("\n")
        for char in message:
            self.chat_history.insertPlainText(char)
            self.chat_history.repaint()
            QApplication.processEvents()
            time.sleep(0.05)
        self.chat_history.insertPlainText("\n")
        self.chat_history.repaint()
        self.chat_history.setTextColor(QColor(0, 0, 0))

    def display_message(self, message):
        self.chat_history.setTextColor(QColor(0, 0, 0))
        self.chat_history.append(message)
        self.chat_history.repaint()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(135, 206, 250))  # 设置背景颜色为天蓝色
    app.setPalette(palette)

    window = ChatApp()
    window.show()

    sys.exit(app.exec_())
