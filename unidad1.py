from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QRadioButton,
    QPushButton, QVBoxLayout, QWidget, QComboBox, QGridLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QColor
from PIL.ImageQt import ImageQt

import math
import matplotlib.pyplot as plt
import numpy as np
import io
from PIL import Image


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

        # Gráfica
        self.graph_label = QLabel()

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
        layout.addWidget(self.graph_label, 10, 0, 1, 3)

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

            # Calcular porcentaje de grasa corporal (Método de la Marina de EE.UU.)
            if self.male_radio.isChecked():
                body_fat = 495 / (1.0324 - 0.19077 * math.log10(waist - neck) + 0.15456 * math.log10(height)) - 450
            else:
                body_fat = 495 / (1.29579 - 0.35004 * math.log10(waist + hip - neck) + 0.221 * math.log10(height)) - 450

            # Masa de grasa corporal y masa magra
            body_fat_mass = weight * (body_fat / 100)
            lean_body_mass = weight - body_fat_mass

            # Grasa ideal según la edad (Jackson & Pollock)
            age = int(self.age_input.text())
            ideal_body_fat = 10.5 if self.male_radio.isChecked() else 18.4  # Valores ajustados según la imagen

            # Grasa a perder para alcanzar el ideal
            fat_to_lose = weight * ((body_fat - ideal_body_fat) / 100)

            # Grasa corporal según el método del IMC
            bmi = weight / ((height / 100) ** 2)
            bmi_body_fat = 1.2 * bmi + (0.23 * age) - (10.8 if self.male_radio.isChecked() else 0) - 5.4

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
            self.generate_graph(body_fat)

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
        self.graph_label.clear()

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

    def generate_graph(self, body_fat):
    # Configurar categorías y rangos según el género
        if self.male_radio.isChecked():
            categories = ["Essential", "Athletes", "Fitness", "Average", "Obese"]
            ranges = [6, 14, 18, 25, 40]  # Rango máximo como referencia para hombres
            colors = ["#00ccff", "#33ff99", "#ffff66", "#ff9966", "#ff3300"]
        else:
            categories = ["Essential", "Athletes", "Fitness", "Average", "Obese"]
            ranges = [14, 21, 25, 32, 50]  # Rango máximo como referencia para mujeres
            colors = ["#00ccff", "#33ff99", "#ffff66", "#ff9966", "#ff3300"]

        # Crear la gráfica horizontal
        fig, ax = plt.subplots(figsize=(6, 1))
        start = 0

        # Dibujar las barras con los rangos de grasa corporal
        for i, range_val in enumerate(ranges):
            ax.barh(0, range_val - start, left=start, color=colors[i], edgecolor="black")
            start = range_val

        # Línea para el porcentaje de grasa corporal calculado
        ax.axvline(body_fat, color="black", linestyle="--", label=f"{body_fat:.1f}%")
        ax.set_yticks([])
        ax.set_xticks(ranges)
        ax.set_xticklabels(categories)
        ax.legend()

        # Convertir la gráfica en una imagen y mostrarla en la interfaz
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        img = Image.open(buf)

        qt_img = QPixmap.fromImage(ImageQt(img))
        self.graph_label.setPixmap(qt_img)
        buf.close()



app = QApplication([])
window = BodyFatCalculator()
window.show()
app.exec()

