from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QRadioButton,
    QPushButton, QVBoxLayout, QWidget, QComboBox, QGridLayout
)
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
import math

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
            is_metric = self.units_combo.currentText() == "Metric"

            # Convertir a unidades métricas si es necesario
            if not is_metric:
                weight *= 0.453592  # lb a kg
                height *= 2.54  # in a cm
                neck *= 2.54
                waist *= 2.54
                if hip:
                    hip *= 2.54

            # Calcular porcentaje de grasa corporal (Método US Navy)
            if self.male_radio.isChecked():
                body_fat = 495 / (1.0324 - 0.19077 * math.log10(waist - neck) + 0.15456 * math.log10(height)) - 450
            else:
                body_fat = 495 / (1.29579 - 0.35004 * math.log10(waist + hip - neck) + 0.221 * math.log10(height)) - 450

            body_fat_mass = weight * (body_fat / 100)
            lean_body_mass = weight - body_fat_mass

            # Body Fat (BMI method)
            bmi = weight / ((height / 100) ** 2)
            if self.male_radio.isChecked():
                bmi_body_fat = 1.20 * bmi + 0.23 * int(self.age_input.text()) - 16.2
            else:
                bmi_body_fat = 1.20 * bmi + 0.23 * int(self.age_input.text()) - 5.4

            # Ideal Body Fat y cantidad a perder (Jackson & Pollock)
            ideal_body_fat = 10.5 if self.male_radio.isChecked() else 18.4
            fat_to_lose = (body_fat - ideal_body_fat) / 100 * weight

            # Categoría de grasa corporal
            category = self.get_category(body_fat, self.male_radio.isChecked())

            # Mostrar resultados
            self.result_output.setText(
                f"Body Fat (U.S. Navy Method): {body_fat:.1f}%\n"
                f"Body Fat Category: {category}\n"
                f"Body Fat Mass: {body_fat_mass:.1f} kg\n"
                f"Lean Body Mass: {lean_body_mass:.1f} kg\n"
                f"Ideal Body Fat for Given Age (Jackson & Pollock): {ideal_body_fat:.1f}%\n"
                f"Body Fat to Lose to Reach Ideal: {fat_to_lose:.1f} kg\n"
                f"Body Fat (BMI method): {bmi_body_fat:.1f}%"
            )

            # Generar gráfica
            self.show_graph(body_fat)

        except ValueError:
            self.result_output.setText("Invalid input. Please enter valid numbers.")

    def show_graph(self, body_fat):
        categories = ["Essential", "Athletes", "Fitness", "Average", "Obese"]
        male_limits = [6, 14, 18, 25, 30]
        female_limits = [13, 20, 24, 31, 36]
        limits = male_limits if self.male_radio.isChecked() else female_limits

        plt.figure(figsize=(6, 2))
        plt.bar(categories, limits, color=['blue', 'green', 'yellow', 'orange', 'red'], alpha=0.5)
        plt.axhline(y=body_fat, color='black', linestyle='--')
        plt.text(2, body_fat + 1, f"{body_fat:.1f}%", color='black', ha='center')
        plt.title("Body Fat Distribution")
        plt.ylabel("% Body Fat")
        plt.show()

    def clear_inputs(self):
        # Limpiar campos de entrada y resultado
        self.age_input.clear()
        self.weight_input.clear()
        self.height_input.clear()
        self.neck_input.clear()
        self.waist_input.clear()
        self.hip_input.clear()
        self.result_output.clear()

    def get_category(self, body_fat, is_male):
        if is_male:
            if body_fat < 6:
                return "Essential Fat"
            elif body_fat < 14:
                return "Athletes"
            elif body_fat < 18:
                return "Fitness"
            elif body_fat < 25:
                return "Average"
            else:
                return "Obese"
        else:
            if body_fat < 13:
                return "Essential Fat"
            elif body_fat < 20:
                return "Athletes"
            elif body_fat < 24:
                return "Fitness"
            elif body_fat < 31:
                return "Average"
            else:
                return "Obese"

app = QApplication([])
window = BodyFatCalculator()
window.show()
app.exec()

