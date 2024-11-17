from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QRadioButton, QButtonGroup, QFormLayout
)
from PyQt6.QtCore import Qt, pyqtSlot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from simulation.planet_constants import G_CONSTANT, EARTH_MASS, EARTH_RADIUS, MOON_MASS, MOON_RADIUS, MOON_DISTANCE
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from simulation.rocket import Rocket


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Intialise window
        self.setWindowTitle("Rocket Simulation")
        self.setGeometry(100, 100, 1200, 800)

        # Current view mode which can change between 'trajectory' or 'energy'
        self.current_view = "trajectory"

        # User inputs with some starting parameters that give a circular orbit
        self.mass_label = QLabel("Rocket Mass (kg):")
        self.mass_input = QLineEdit("100")

        self.x_label = QLabel("Starting x-coordinate (m):")
        self.x_input = QLineEdit("0")

        self.y_label = QLabel("Starting y-coordinate (m):")
        self.y_input = QLineEdit("7E6")  

        self.vx_label = QLabel("Initial x-velocity (m/s):")
        self.vx_input = QLineEdit("7543")  

        self.vy_label = QLabel("Initial y-velocity (m/s):")
        self.vy_input = QLineEdit("0")

        self.time_step_label = QLabel("Time Step (s):")
        self.time_step_input = QLineEdit("10")

        self.simulation_time_label = QLabel("Total Simulation Time (s):")
        self.simulation_time_input = QLineEdit("10000")

        # Selection for the simulation, to include either only the Earth, or the Earth and Moon
        self.simulation_label = QLabel("Choose Simulation:")
        self.earth_button = QRadioButton("Earth Only")
        self.earth_moon_button = QRadioButton("Earth and Moon")
        self.earth_button.setChecked(True)

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.earth_button)
        self.button_group.addButton(self.earth_moon_button)

        # Buttons for performing the simulation and switching current view between 'trajectory' and 'energy'
        self.run_button = QPushButton("Run Simulation")
        self.toggle_view_button = QPushButton("Switch to Energy View")

        # Matplotlib plot
        self.canvas = FigureCanvas(plt.figure(figsize=(8, 6)))
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Adjust form layout for inputs and simulation selection
        form_layout = QFormLayout()
        form_layout.addRow(self.mass_label, self.mass_input)
        form_layout.addRow(self.x_label, self.x_input)
        form_layout.addRow(self.y_label, self.y_input)
        form_layout.addRow(self.vx_label, self.vx_input)
        form_layout.addRow(self.vy_label, self.vy_input)
        form_layout.addRow(self.time_step_label, self.time_step_input)
        form_layout.addRow(self.simulation_time_label, self.simulation_time_input)
        
        # Add a spacer (two empty lines) before "Choose Simulation"
        # Add simulation selection directly to form layout
        form_layout.addRow(QLabel())  
        form_layout.addRow(QLabel())  
        simulation_layout = QHBoxLayout()
        simulation_layout.addWidget(self.simulation_label)
        simulation_layout.addWidget(self.earth_button)
        simulation_layout.addWidget(self.earth_moon_button)
        simulation_layout.setSpacing(5)  
        form_layout.addRow(simulation_layout)

        # Add a spacer (two empty lines) before the buttons
        # Add buttons for running the simulation and switching current view
        form_layout.addRow(QLabel())  
        form_layout.addRow(QLabel())  
        form_layout.addRow(self.run_button)
        form_layout.addRow(self.toggle_view_button)

        # Add crash message below the buttons with two-line spacing
        form_layout.addRow(QLabel())  
        form_layout.addRow(QLabel())  
        self.crash_message_label = QLabel("")
        self.crash_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addRow(self.crash_message_label)

        # Plot layout for simulations
        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)

        # Main layout with form layout for inputs on the left and plotting layout on the right
        main_layout = QHBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(plot_layout)

        # Central widget set with the main layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Connect buttons for running simulation and switching current view
        self.run_button.clicked.connect(self.run_simulation)
        self.toggle_view_button.clicked.connect(self.toggle_view)

    @pyqtSlot()
    def run_simulation(self):
        """Reads inputs, runs the simulation, and updates the plot."""
        try:
            # Clear the crash message before starting a new simulation
            self.crash_message_label.setText("")

            # Extract user inputs
            mass = float(self.mass_input.text())
            x = float(self.x_input.text())
            y = float(self.y_input.text())
            vx = float(self.vx_input.text())
            vy = float(self.vy_input.text())
            h = float(self.time_step_input.text())
            time_target = float(self.simulation_time_input.text())

            # Set celestial parameters based on user selected simulation type
            if self.earth_button.isChecked():
                planet_mass = EARTH_MASS
                moon_mass = 0
                moon_distance = 0
            else:
                planet_mass = EARTH_MASS
                moon_mass = MOON_MASS
                moon_distance = MOON_DISTANCE

            # Initialize rocket
            self.rocket = Rocket(mass, x, y, vx, vy, 0)
            self.rocket.initialize_energies(G_CONSTANT, planet_mass, moon_mass, moon_distance)

            # Run the simulation up until the user defined end time, unless rocket's update position and velocity method detects crash
            while self.rocket.time_log[-1] < time_target:
                try:
                    self.rocket.update_position_and_velocity(
                        G = G_CONSTANT,
                        h = h,
                        Mass_Earth = planet_mass,
                        Mass_Moon = moon_mass,
                        Moon_Distance = moon_distance,
                        Earth_Radius = EARTH_RADIUS,
                        Moon_Radius = MOON_RADIUS
                    )
                except ValueError as e:
                    # Display the crash message and stop the simulation
                    self.crash_message_label.setText(str(e))
                    break

            # Plot results
            self.plot_simulation()

        except ValueError as e:
            # Display invalid input message in the status bar
            self.statusBar().showMessage("Invalid input. Please enter valid numerical values.")

    def toggle_view(self):
        """Toggles between trajectory view and energy view."""
        if self.current_view == "trajectory":
            self.current_view = "energy"
            self.toggle_view_button.setText("Switch to Trajectory View")
        else:
            self.current_view = "trajectory"
            self.toggle_view_button.setText("Switch to Energy View")
        self.plot_simulation()

    def plot_simulation(self):
        """Plots the simulation based on the current view."""
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)

        if self.current_view == "trajectory":
            # Plot the Earth
            earth_texture_path = "Resources/earth_texture.png"
            earth_img = mpimg.imread(earth_texture_path)
            ax.imshow(
                earth_img,
                extent=[-EARTH_RADIUS, EARTH_RADIUS, -EARTH_RADIUS, EARTH_RADIUS],
                zorder=1,
            )

            # Plot the Moon if applicable
            if self.earth_moon_button.isChecked():
                moon_texture_path = "Resources/moon_texture.png"
                moon_img = mpimg.imread(moon_texture_path)
                ax.imshow(
                    moon_img,
                    extent=[
                        MOON_DISTANCE - MOON_RADIUS,
                        MOON_DISTANCE + MOON_RADIUS,
                        -MOON_RADIUS,
                        MOON_RADIUS,
                    ],
                    zorder=1,
                )

            # Plot the rocket's trajectory
            ax.plot(self.rocket.x_log, self.rocket.y_log, color="red", label="Rocket Trajectory", zorder=2)
            ax.set_title("Rocket Trajectory")
            ax.set_xlabel("x-coordinate (m)")
            ax.set_ylabel("y-coordinate (m)")
            ax.legend()

            x_min, x_max = min(self.rocket.x_log), max(self.rocket.x_log)
            y_min, y_max = min(self.rocket.y_log), max(self.rocket.y_log)

            x_padding = 0.1 * (x_max - x_min)
            y_padding = 0.1 * (y_max - y_min)

            ax.set_xlim(x_min - x_padding, x_max + x_padding)
            ax.set_ylim(y_min - y_padding, y_max + y_padding)
            ax.set_aspect("equal", adjustable="datalim")

        elif self.current_view == "energy":
            # Plot the rocket's energies
            ax.plot(self.rocket.time_log, self.rocket.ke_log, color="blue", label="Kinetic Energy")
            ax.plot(self.rocket.time_log, self.rocket.gpe_log, color="green", label="Potential Energy")
            ax.plot(self.rocket.time_log, self.rocket.total_energy_log, color="purple", label="Total Energy")
            ax.set_title("Energy vs Time")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Energy (J)")
            ax.legend()

        self.canvas.draw()
