from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QRadioButton, QButtonGroup, QFormLayout
)
from PyQt6.QtCore import pyqtSlot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from simulation.planet_constants import G_CONSTANT, EARTH_MASS, EARTH_RADIUS, MOON_MASS, MOON_RADIUS, MOON_DISTANCE
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from simulation.rocket import Rocket

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rocket Simulation")
        self.setGeometry(100, 100, 1200, 800)

        # Widgets for user inputs
        self.mass_label = QLabel("Rocket Mass (kg):")
        self.mass_input = QLineEdit("100")

        self.x_label = QLabel("Starting x-coordinate (m):")
        self.x_input = QLineEdit("0")

        self.y_label = QLabel("Starting y-coordinate (m):")
        self.y_input = QLineEdit("7E6")  # 7,000 km above Earth's surface

        self.vx_label = QLabel("Initial x-velocity (m/s):")
        self.vx_input = QLineEdit("7543")  # Approx. circular orbit velocity

        self.vy_label = QLabel("Initial y-velocity (m/s):")
        self.vy_input = QLineEdit("0")

        self.time_step_label = QLabel("Time Step (s):")
        self.time_step_input = QLineEdit("10")

        self.simulation_time_label = QLabel("Total Simulation Time (s):")
        self.simulation_time_input = QLineEdit("10000")

        # Simulation selection
        self.simulation_label = QLabel("Choose Simulation:")
        self.earth_button = QRadioButton("Earth Only")
        self.earth_moon_button = QRadioButton("Earth and Moon")
        self.earth_button.setChecked(True)

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.earth_button)
        self.button_group.addButton(self.earth_moon_button)

        # Run Simulation Button
        self.run_button = QPushButton("Run Simulation")

        # Matplotlib plot
        self.canvas = FigureCanvas(plt.figure(figsize=(8, 6)))

        # Navigation toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Layouts
        form_layout = QFormLayout()
        form_layout.addRow(self.mass_label, self.mass_input)
        form_layout.addRow(self.x_label, self.x_input)
        form_layout.addRow(self.y_label, self.y_input)
        form_layout.addRow(self.vx_label, self.vx_input)
        form_layout.addRow(self.vy_label, self.vy_input)
        form_layout.addRow(self.time_step_label, self.time_step_input)
        form_layout.addRow(self.simulation_time_label, self.simulation_time_input)

        input_layout = QVBoxLayout()
        input_layout.addLayout(form_layout)
        input_layout.addWidget(self.simulation_label)
        input_layout.addWidget(self.earth_button)
        input_layout.addWidget(self.earth_moon_button)
        input_layout.addWidget(self.run_button)

        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.toolbar)  # Add the navigation toolbar
        plot_layout.addWidget(self.canvas)

        main_layout = QHBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(plot_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Connect button
        self.run_button.clicked.connect(self.run_simulation)

    @pyqtSlot()
    def run_simulation(self):
        """Reads inputs, runs the simulation, and updates the plot."""
        try:
            # Extract user inputs
            mass = float(self.mass_input.text())
            x = float(self.x_input.text())
            y = float(self.y_input.text())
            vx = float(self.vx_input.text())
            vy = float(self.vy_input.text())
            h = float(self.time_step_input.text())
            time_target = float(self.simulation_time_input.text())

            # Choose simulation type
            if self.earth_button.isChecked():
                planet_mass = EARTH_MASS  # Earth mass
                moon_mass = 0
                moon_distance = 0
                include_moon = False
            else:
                planet_mass = EARTH_MASS
                moon_mass = MOON_MASS
                moon_distance = MOON_DISTANCE  # Moon distance from Earth
                include_moon = True

            # Initialize rocket
            rocket = Rocket(mass, x, y, vx, vy, 0)

            # Run the simulation
            while rocket.time_log[-1] < time_target:
                rocket.update_position_and_velocity(
                    G = G_CONSTANT, h = h, Mass_Earth = planet_mass, Mass_Moon = moon_mass, Moon_Distance = moon_distance
                )

            # Extract logs
            x_log = rocket.x_log
            y_log = rocket.y_log

            # Plot results
            self.plot_simulation(x_log, y_log, include_moon = include_moon, moon_distance = moon_distance)

        except ValueError:
            self.statusBar().showMessage("Invalid input. Please enter valid numerical values.")

    def plot_simulation(self, x_log, y_log, include_moon = False, moon_distance = 0, moon_radius = MOON_RADIUS):
        """Plots the rocket's trajectory and celestial bodies."""
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)

        # Plot the Earth
        earth_radius = 6.371e6  # Earth radius in meters
        earth_texture_path = "Resources/earth_texture.png"
        earth_img = mpimg.imread(earth_texture_path)
        ax.imshow(
            earth_img,
            extent=[
                -earth_radius,
                earth_radius,
                -earth_radius,
                earth_radius,
            ],
            zorder=1,
        )

        # Plot the Moon (if included)
        if include_moon:
            moon_texture_path = "Resources/moon_texture.png"
            moon_img = mpimg.imread(moon_texture_path)
            ax.imshow(
                moon_img,
                extent=[
                    moon_distance - moon_radius,
                    moon_distance + moon_radius,
                    -moon_radius,
                    moon_radius,
                ],
                zorder=1,
            )

        # Plot the Rocket Trajectory
        ax.plot(x_log, y_log, color="red", label="Rocket Trajectory", zorder=2)

        # Set labels, title, and legend
        ax.set_title("Rocket Simulation")
        ax.set_xlabel("x-coordinate (m)")
        ax.set_ylabel("y-coordinate (m)")
        ax.legend()

        # Equal aspect ratio for celestial bodies
        ax.set_aspect('equal', adjustable='datalim')
        self.canvas.draw()