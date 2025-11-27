import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QLineEdit,
    QMessageBox,
)

class Calculator(QMainWindow):
    """
    PyQt6를 사용한 기본 계산기 UI 클래스
    """
    def __init__(self):
        """
        생성자: 창의 제목, 크기, 레이아웃 및 위젯을 초기화합니다.
        """
        super().__init__()

        self.setWindowTitle("계산기")
        self.setFixedSize(300, 400)  # 창 크기 고정
        self.setFixedSize(300, 450)  # 창 크기 고정 (버튼 추가로 높이 조절)

        # 모든 위젯을 담을 중앙 위젯과 메인 레이아웃 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 계산 결과를 보여줄 디스플레이 (QLineEdit)
        self.display = QLineEdit()
        self.display.setReadOnly(True)  # 읽기 전용으로 설정
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight) # 텍스트 오른쪽 정렬
        self.display.setStyleSheet("font-size: 24px; padding: 10px;") # 스타일 적용
        main_layout.addWidget(self.display)

        # 버튼들을 담을 그리드 레이아웃
        buttons_layout = QGridLayout()

        # 버튼 텍스트와 그리드 내 위치 정의
        # (텍스트, 행, 열, 행 병합, 열 병합)
        buttons = [
            ('C', 0, 0, 1, 1), ('%', 0, 1, 1, 1), ('<-', 0, 2, 1, 1), ('/', 0, 3, 1, 1),
            ('7', 1, 0, 1, 1), ('8', 1, 1, 1, 1), ('9', 1, 2, 1, 1), ('*', 1, 3, 1, 1),
            ('4', 2, 0, 1, 1), ('5', 2, 1, 1, 1), ('6', 2, 2, 1, 1), ('-', 2, 3, 1, 1),
            ('1', 3, 0, 1, 1), ('2', 3, 1, 1, 1), ('3', 3, 2, 1, 1), ('+', 3, 3, 1, 1),
            ('0', 4, 0, 1, 2), ('.', 4, 2, 1, 1), ('=', 4, 3, 1, 1),
        ]

        # 정의된 버튼 정보에 따라 QPushButton 생성 및 레이아웃에 추가
        for text, row, col, rowspan, colspan in buttons:
            button = QPushButton(text)
            button.setStyleSheet("font-size: 18px; padding: 10px;")
            buttons_layout.addWidget(button, row, col, rowspan, colspan)

        # 메인 레이아웃에 버튼 그리드 추가
        main_layout.addLayout(buttons_layout)

        # 메시지 버튼 추가
        message_button = QPushButton("message")
        message_button.setStyleSheet("font-size: 16px; padding: 8px;")
        message_button.clicked.connect(self.show_message_box)
        main_layout.addWidget(message_button)

    def show_message_box(self):
        """
        메시지 버튼 클릭 시 "Button Clicked" 메시지 박스를 표시합니다.
        """
        QMessageBox.information(self, "알림", "Button Clicked")

def main():
    """
    애플리케이션을 생성하고 메인 창을 실행합니다.
    """
    app = QApplication(sys.argv)
    calculator_window = Calculator()
    calculator_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()