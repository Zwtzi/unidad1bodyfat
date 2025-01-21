import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QRadioButton, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QGroupBox, QGridLayout)

class BodyFatCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Body Fat Calculator")
        self.setGeometry(100, 100, 600, 400)

        # Main layout
        main_layout = QVBoxLayout()

        # Input group box
        input_group = QGroupBox("Input Details")
        input_layout = QGridLayout()

        # Gender
        self.male_radio = QRadioButton("Male")
        self.male_radio.setChecked(True)
        self.female_radio = QRadioButton("Female")

        input_layout.addWidget(QLabel("Gender:"), 0, 0)
        input_layout.addWidget(self.male_radio, 0, 1)
        input_layout.addWidget(self.female_radio, 0, 2)

        # Age
        input_layout.addWidget(QLabel("Age:"), 1, 0)
        self.age_input = QLineEdit()
        input_layout.addWidget(self.age_input, 1, 1)

        # Weight
        input_layout.addWidget(QLabel("Weight (kg):"), 2, 0)
        self.weight_input = QLineEdit()
        input_layout.addWidget(self.weight_input, 2, 1)

        # Height
        input_layout.addWidget(QLabel("Height (cm):"), 3, 0)
        self.height_input = QLineEdit()
        input_layout.addWidget(self.height_input, 3, 1)

        # Neck
        input_layout.addWidget(QLabel("Neck (cm):"), 4, 0)
        self.neck_input = QLineEdit()
        input_layout.addWidget(self.neck_input, 4, 1)

        # Waist
        input_layout.addWidget(QLabel("Waist (cm):"), 5, 0)
        self.waist_input = QLineEdit()
        input_layout.addWidget(self.waist_input, 5, 1)

        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)

        # Calculate button
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_body_fat)
        main_layout.addWidget(self.calculate_button)

        # Result display
        self.result_label = QLabel("Results will be displayed here.")
        main_layout.addWidget(self.result_label)

        # Central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def calculate_body_fat(self):
        try:
            gender = "male" if self.male_radio.isChecked() else "female"
            age = int(self.age_input.text())
            weight = float(self.weight_input.text())
            height = float(self.height_input.text())
            neck = float(self.neck_input.text())
            waist = float(self.waist_input.text())

            if gender == "male":
                # U.S. Navy Method for males
                body_fat = 495 / (1.0324 - 0.19077 * (waist - neck) / height + 0.15456 * height / 100) - 450
            else:
                # U.S. Navy Method for females (not considering hip for simplicity)
                body_fat = 495 / (1.29579 - 0.35004 * (waist - neck) / height + 0.221 * height / 100) - 450

            body_fat = round(body_fat, 1)
            self.result_label.setText(f"Body Fat: {body_fat}%")
        except Exception as e:
            self.result_label.setText(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BodyFatCalculator()
    window.show()
    sys.exit(app.exec())
