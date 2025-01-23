from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QRadioButton,
    QPushButton, QVBoxLayout, QWidget, QComboBox, QGridLayout
)
from PyQt6.QtCore import Qt


class BodyFatCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Body Fat Calculator")

        # Layout principal
        layout = QGridLayout()

        # Inputs básicos
        self.gender_label = QLabel("Gender:")
        self.male_radio = QRadioButton("Male")
        self.female_radio = QRadioButton("Female")
        self.male_radio.setChecked(True)
        self.male_radio.toggled.connect(self.toggle_gender)

        self.age_label = QLabel("Age:")
        self.age_input = QLineEdit()

        self.weight_label = QLabel("Weight (kg):")
        self.weight_input = QLineEdit()

        self.height_label = QLabel("Height (cm):")
        self.height_input = QLineEdit()

        self.neck_label = QLabel("Neck (cm):")
        self.neck_input = QLineEdit()

        self.waist_label = QLabel("Waist (cm):")
        self.waist_input = QLineEdit()

        self.hip_label = QLabel("Hip (cm):")  # Solo para mujeres
        self.hip_input = QLineEdit()
        self.hip_label.setVisible(False)
        self.hip_input.setVisible(False)

        # Sistema de unidades
        self.units_label = QLabel("Units:")
        self.units_combo = QComboBox()
        self.units_combo.addItems(["Metric", "US"])
        self.units_combo.currentIndexChanged.connect(self.update_units)

        # Botones
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_inputs)

        # Resultados
        self.result_label = QLabel("Results:")
        self.result_output = QLabel("")

        # Añadiendo al layout
        layout.addWidget(self.gender_label, 0, 0)
        layout.addWidget(self.male_radio, 0, 1)
        layout.addWidget(self.female_radio, 0, 2)
        layout.addWidget(self.age_label, 1, 0)
        layout.addWidget(self.age_input, 1, 1, 1, 2)
        layout.addWidget(self.weight_label, 2, 0)
        layout.addWidget(self.weight_input, 2, 1, 1, 2)
        layout.addWidget(self.height_label, 3, 0)
        layout.addWidget(self.height_input, 3, 1, 1, 2)
        layout.addWidget(self.neck_label, 4, 0)
        layout.addWidget(self.neck_input, 4, 1, 1, 2)
        layout.addWidget(self.waist_label, 5, 0)
        layout.addWidget(self.waist_input, 5, 1, 1, 2)
        layout.addWidget(self.hip_label, 6, 0)
        layout.addWidget(self.hip_input, 6, 1, 1, 2)
        layout.addWidget(self.units_label, 7, 0)
        layout.addWidget(self.units_combo, 7, 1, 1, 2)
        layout.addWidget(self.calculate_button, 8, 0)
        layout.addWidget(self.clear_button, 8, 1)
        layout.addWidget(self.result_label, 9, 0)
        layout.addWidget(self.result_output, 9, 1, 1, 2)

        # Configuración del widget principal
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def toggle_gender(self):
        # Mostrar o esconder el campo de "Hip" dependiendo del género
        is_female = self.female_radio.isChecked()
        self.hip_label.setVisible(is_female)
        self.hip_input.setVisible(is_female)

    def update_units(self):
        # Cambiar etiquetas según las unidades seleccionadas
        if self.units_combo.currentText() == "Metric":
            self.weight_label.setText("Weight (kg):")
            self.height_label.setText("Height (cm):")
            self.neck_label.setText("Neck (cm):")
            self.waist_label.setText("Waist (cm):")
            self.hip_label.setText("Hip (cm):")
        else:
            self.weight_label.setText("Weight (lb):")
            self.height_label.setText("Height (in):")
            self.neck_label.setText("Neck (in):")
            self.waist_label.setText("Waist (in):")
            self.hip_label.setText("Hip (in):")

    def calculate(self):
        try:
            # Entradas básicas
            weight = float(self.weight_input.text())
            height = float(self.height_input.text())
            neck = float(self.neck_input.text())
            waist = float(self.waist_input.text())
            hip = float(self.hip_input.text()) if self.female_radio.isChecked() else 0
            age = int(self.age_input.text())
            is_metric = self.units_combo.currentText() == "Metric"

            # Convertir a unidades métricas si es necesario
            if not is_metric:
                weight *= 0.453592  # lb a kg
                height *= 2.54  # in a cm
                neck *= 2.54
                waist *= 2.54
                if hip:
                    hip *= 2.54

            # Calcular porcentaje de grasa corporal
            if self.male_radio.isChecked():
                body_fat = 495 / (1.0324 - 0.19077 * (waist - neck) / height + 0.15456 * height) - 450
            else:
                body_fat = 495 / (1.29579 - 0.35004 * (waist + hip - neck) / height + 0.22100 * height) - 450

            # Categoría de grasa corporal
            if body_fat < 6:
                category = "Essential"
            elif body_fat < 14:
                category = "Athletes"
            elif body_fat < 18:
                category = "Fitness"
            elif body_fat < 25:
                category = "Average"
            else:
                category = "Obese"

            # Masa de grasa y masa magra
            body_fat_mass = weight * (body_fat / 100)
            lean_body_mass = weight - body_fat_mass

            # Grasa ideal según edad y género
            if self.male_radio.isChecked():
                ideal_body_fat = 8 + 0.1 * age
            else:
                ideal_body_fat = 20 + 0.1 * age

            fat_to_lose = body_fat_mass - (weight * (ideal_body_fat / 100))
            fat_bmi_method = 1.2 * (weight / ((height / 100) ** 2)) + 0.23 * age - (10.8 if self.male_radio.isChecked() else 0) - 5.4

            # Mostrar resultados
            self.result_output.setText(
                f"Body Fat: {body_fat:.1f}%\n"
                f"Category: {category}\n"
                f"Body Fat Mass: {body_fat_mass:.1f} kg\n"
                f"Lean Body Mass: {lean_body_mass:.1f} kg\n"
                f"Ideal Body Fat: {ideal_body_fat:.1f}%\n"
                f"Fat to Lose: {fat_to_lose:.1f} kg\n"
                f"Body Fat (BMI Method): {fat_bmi_method:.1f}%"
            )
        except ValueError:
            self.result_output.setText("Invalid input. Please enter valid numbers.")

    def clear_inputs(self):
        # Limpiar campos de entrada y resultado
        self.age_input.clear()
        self.weight_input.clear()
        self.height_input.clear()
        self.neck_input.clear()
        self.waist_input.clear()
        self.hip_input.clear()
        self.result_output.clear()


app = QApplication([])
window = BodyFatCalculator()
window.show()
app.exec()
