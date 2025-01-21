import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QLineEdit, QRadioButton, QPushButton, QButtonGroup, QComboBox, QMessageBox
)

class BodyFatCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Body Fat Calculator")

        # Main layout
        self.main_layout = QVBoxLayout()

        # Unit selection
        self.unit_selector = QComboBox()
        self.unit_selector.addItems(["Metric Units", "US Units"])
        self.unit_selector.currentIndexChanged.connect(self.update_units)
        self.main_layout.addWidget(self.unit_selector)

        # Input fields
        self.input_layout = QVBoxLayout()
        self.gender_group = QButtonGroup()

        self.male_button = QRadioButton("Male")
        self.female_button = QRadioButton("Female")
        self.gender_group.addButton(self.male_button)
        self.gender_group.addButton(self.female_button)

        gender_layout = QHBoxLayout()
        gender_layout.addWidget(QLabel("Gender:"))
        gender_layout.addWidget(self.male_button)
        gender_layout.addWidget(self.female_button)
        self.input_layout.addLayout(gender_layout)

        # Input fields with labels
        self.age_input = self.create_input_field("Age:")
        self.weight_input = self.create_input_field("Weight:")
        self.height_input = self.create_input_field("Height:")
        self.neck_input = self.create_input_field("Neck:")
        self.waist_input = self.create_input_field("Waist:")
        self.hip_input = self.create_input_field("Hip (females only):")
        self.hip_input.setVisible(False)

        self.female_button.toggled.connect(self.toggle_hip_input)

        self.main_layout.addLayout(self.input_layout)

        # Calculate button
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_body_fat)
        self.main_layout.addWidget(self.calculate_button)

        # Results area
        self.results_label = QLabel("")
        self.main_layout.addWidget(self.results_label)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        # Default settings
        self.male_button.setChecked(True)
        self.update_units()

    def create_input_field(self, label_text):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        input_field = QLineEdit()
        layout.addWidget(label)
        layout.addWidget(input_field)
        self.input_layout.addLayout(layout)
        return input_field

    def toggle_hip_input(self):
        self.hip_input.setVisible(self.female_button.isChecked())

    def update_units(self):
        if self.unit_selector.currentText() == "Metric Units":
            self.weight_input.setPlaceholderText("kg")
            self.height_input.setPlaceholderText("cm")
            self.neck_input.setPlaceholderText("cm")
            self.waist_input.setPlaceholderText("cm")
            self.hip_input.setPlaceholderText("cm")

            self.weight_input.setText("")
            self.height_input.setText("")
            self.neck_input.setText("")
            self.waist_input.setText("")
            self.hip_input.setText("")
        else:
            self.weight_input.setPlaceholderText("lbs")
            self.height_input.setPlaceholderText("in")
            self.neck_input.setPlaceholderText("in")
            self.waist_input.setPlaceholderText("in")
            self.hip_input.setPlaceholderText("in")

            self.weight_input.setText("")
            self.height_input.setText("")
            self.neck_input.setText("")
            self.waist_input.setText("")
            self.hip_input.setText("")

    def calculate_body_fat(self):
        try:
            # Get inputs
            gender = "male" if self.male_button.isChecked() else "female"
            age = int(self.age_input.text())
            weight = float(self.weight_input.text())
            height = float(self.height_input.text())
            neck = float(self.neck_input.text())
            waist = float(self.waist_input.text())
            hip = float(self.hip_input.text()) if gender == "female" else 0

            if self.unit_selector.currentText() == "US Units":
                # Convert US to Metric
                weight = weight * 0.453592  # lbs to kg
                height = height * 2.54  # in to cm
                neck = neck * 2.54
                waist = waist * 2.54
                hip = hip * 2.54

            # Body fat calculation (US Navy Method)
            if gender == "male":
                bfp = 86.010 * (waist - neck) / height - 70.041 * (height / 100) + 36.76
            else:
                bfp = 163.205 * (waist + hip - neck) / height - 97.684 * (height / 100) - 78.387

            # Ideal body fat based on age
            if gender == "male":
                if age <= 20:
                    ideal_body_fat = 8.5
                elif age <= 25:
                    ideal_body_fat = 10.5
                elif age <= 30:
                    ideal_body_fat = 12.7
                elif age <= 35:
                    ideal_body_fat = 13.7
                elif age <= 40:
                    ideal_body_fat = 15.3
                elif age <= 45:
                    ideal_body_fat = 16.4
                elif age <= 50:
                    ideal_body_fat = 18.9
                else:
                    ideal_body_fat = 20.9
            else:
                if age <= 20:
                    ideal_body_fat = 17.7
                elif age <= 25:
                    ideal_body_fat = 18.4
                elif age <= 30:
                    ideal_body_fat = 19.3
                elif age <= 35:
                    ideal_body_fat = 21.5
                elif age <= 40:
                    ideal_body_fat = 22.2
                elif age <= 45:
                    ideal_body_fat = 22.9
                elif age <= 50:
                    ideal_body_fat = 25.2
                else:
                    ideal_body_fat = 26.3

            lean_body_mass = weight * (1 - bfp / 100)
            fat_mass = weight * bfp / 100
            fat_to_lose = max(0, (bfp - ideal_body_fat) / 100 * weight)

            # BMI Body Fat Estimate
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            bmi_body_fat = (1.20 * bmi) + (0.23 * age) - (10.8 if gender == "male" else 0) - 5.4

            # Body Fat Category
            if gender == "male":
                if bfp < 6:
                    category = "Essential Fat"
                elif bfp < 14:
                    category = "Athletes"
                elif bfp < 18:
                    category = "Fitness"
                elif bfp < 25:
                    category = "Average"
                else:
                    category = "Obese"
            else:
                if bfp < 14:
                    category = "Essential Fat"
                elif bfp < 21:
                    category = "Athletes"
                elif bfp < 25:
                    category = "Fitness"
                elif bfp < 32:
                    category = "Average"
                else:
                    category = "Obese"

            # Update results
            self.results_label.setText(
                f"Body Fat (U.S. Navy Method): {bfp:.1f}%\n"
                f"Body Fat Category: {category}\n"
                f"Body Fat Mass: {fat_mass:.1f} kg\n"
                f"Lean Body Mass: {lean_body_mass:.1f} kg\n"
                f"Ideal Body Fat for Given Age: {ideal_body_fat}%\n"
                f"Body Fat to Lose to Reach Ideal: {fat_to_lose:.1f} kg\n"
                f"Body Fat (BMI method): {bmi_body_fat:.1f}%"
            )
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for all fields.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BodyFatCalculator()
    window.show()
    sys.exit(app.exec())
