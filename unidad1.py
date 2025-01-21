import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QRadioButton, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QGroupBox, QGridLayout, QTextEdit)

class BodyFatCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Body Fat Calculator")
        self.setGeometry(100, 100, 600, 600)

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

        # Hip (only for females)
        self.hip_label = QLabel("Hip (cm):")
        self.hip_input = QLineEdit()
        input_layout.addWidget(self.hip_label, 6, 0)
        input_layout.addWidget(self.hip_input, 6, 1)
        self.hip_label.setVisible(False)
        self.hip_input.setVisible(False)

        # Toggle hip visibility based on gender
        self.female_radio.toggled.connect(self.toggle_hip_input)

        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)

        # Calculate button
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_body_fat)
        main_layout.addWidget(self.calculate_button)

        # Result display
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        main_layout.addWidget(self.result_text)

        # Central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def toggle_hip_input(self):
        is_female = self.female_radio.isChecked()
        self.hip_label.setVisible(is_female)
        self.hip_input.setVisible(is_female)

    def calculate_body_fat(self):
        try:
            gender = "male" if self.male_radio.isChecked() else "female"
            age = int(self.age_input.text())
            weight = float(self.weight_input.text())
            height = float(self.height_input.text())
            neck = float(self.neck_input.text())
            waist = float(self.waist_input.text())
            hip = float(self.hip_input.text()) if gender == "female" else 0

            if gender == "male":
                # U.S. Navy Method for males
                body_fat = 495 / (1.0324 - 0.19077 * (waist - neck) / height + 0.15456 * height / 100) - 450
            else:
                # U.S. Navy Method for females
                body_fat = 495 / (1.29579 - 0.35004 * (waist + hip - neck) / height + 0.221 * height / 100) - 450

            body_fat = round(body_fat, 1)

            # Additional calculations
            fat_mass = round(weight * body_fat / 100, 1)
            lean_mass = round(weight - fat_mass, 1)
            ideal_body_fat = 10.5 if gender == "male" else 18.0
            fat_to_lose = round(weight * (body_fat - ideal_body_fat) / 100, 1) if body_fat > ideal_body_fat else 0

            # Display results
            results = f"""
Body Fat: {body_fat}%
Body Fat Category: {'Essential' if body_fat <= 5 else 'Athletes' if body_fat <= 13 else 'Fitness' if body_fat <= 17 else 'Average' if body_fat <= 25 else 'Obese'}
Body Fat Mass: {fat_mass} kg
Lean Body Mass: {lean_mass} kg
Ideal Body Fat for Given Age: {ideal_body_fat}%
Body Fat to Lose to Reach Ideal: {fat_to_lose} kg
"""
            self.result_text.setText(results)
        except Exception as e:
            self.result_text.setText(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BodyFatCalculator()
    window.show()
    sys.exit(app.exec())
