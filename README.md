# Rocket Simulation GUI

A graphical application built using PyQt6 and Matplotlib to simulate a rocket's trajectory and energy dynamics in a 2D space. The simulation can include the effects of Earth's and Moon's gravity, with adjustable parameters for mass, velocity, and time.

---

## Features
- **User Input Panel:** Configure initial rocket parameters such as mass, position, and velocity.
- **Simulation Modes:** Choose between:
  - Earth only
  - Earth and Moon
- **Graphical Views:**
  - **Trajectory View:** Visualizes the rocket's path around celestial bodies.
  - **Energy View:** Plots kinetic, potential, and total energy over time.
- **Crash Detection:** Alerts if the rocket crashes into the Earth or Moon.

---

## Installation

To get started, clone the repository and install the required dependencies.

### Prerequisites
- Python 3.8 or later
- Virtual environment (recommended)

### Steps
1. **Clone the Repository**  
   First, clone the repository from GitHub:
   ```bash
   git clone https://github.com/jasperaeschlimann/Rocket-orbital-simulator.git
   cd Rocket-orbital-simulator
   ```

2. **Set Up a Virtual Environment**  
   It is highly recommended to use a virtual environment to keep dependencies isolated from your global Python installation.

   - Create a virtual environment:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On **Linux/Mac**:
       ```bash
       source venv/bin/activate
       ```
     - On **Windows**:
       ```bash
       venv\Scripts\activate
       ```

3. **Install Project Dependencies**  
   With the virtual environment activated, install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**  
   Start the Rocket Simulation GUI:
   ```bash
   python main.py
   ```

5. **Optional: Deactivate the Virtual Environment**  
   When you're done using the application, you can deactivate the virtual environment with:
   ```bash
   deactivate
   ```

---

### Notes
- If you encounter any issues with missing dependencies, make sure `pip` is up-to-date:
  ```bash
  python -m pip install --upgrade pip
  ```
- To ensure the application runs correctly, verify that the `Resources/earth_texture.png` and `Resources/moon_texture.png` files are present in the project directory.

---

## Usage

Run the application using:
```bash
python main.py
```

### Simulation Controls:
- **Rocket Parameters:**
  - Configure initial mass, x/y position, and velocity.
- **Simulation Modes:**
  - Select "Earth Only" or "Earth and Moon."
- **Buttons:**
  - `Run Simulation`: Start the simulation based on the provided inputs.
  - `Switch to Energy View`: Toggle between trajectory and energy plots.

### Outputs:
- **Graphical View:**
  - Trajectory or energy plots based on the current view mode.
- **Crash Messages:**
  - If the rocket crashes into the Earth or Moon, an alert will be displayed below the buttons.

---

## Project Structure

```
Rocket-orbital-simulator/
├── main.py               # Entry point of the application
├── gui/
│   ├── main_window.py    # GUI layout and logic
├── simulation/
│   ├── rocket.py         # Rocket dynamics and physics calculations
│   ├── planet_constants.py  # Gravitational constants and celestial parameters
├── Resources/
│   ├── earth_texture.png # Image texture for Earth
│   ├── moon_texture.png  # Image texture for Moon
├── requirements.txt      # Project dependencies
├── .gitignore            # Specifies files and folders to ignore in version control
├── README.md             # Project documentation
```

---

## Acknowledgments

- **PyQt6** for GUI components.
- **Matplotlib** for 2D plotting.

---

## Author

**Jasper Aeschlimann**  
- GitHub: [jasperaeschlimann](https://github.com/jasperaeschlimann)
- Email: jasper.aeschlimann@outlook.com

