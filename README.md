# 🧪 Worrell Lab

## **Project: Plate Reader Automation**

This Python project automates data collection for an M1000 plate reader and Peltier system combo.

🔗 [Lab Website](https://www.bradyworrell.com/)

---

## 📦 Modules Overview

### `GUI.py`

> A graphical user interface for controlling the Meerstetter TEC device, enabling temperature ramps, monitoring, and control.

#### ✅ Features
- Real-time temperature display
- Input for target temperature and number of scans
- Start/stop controls for ramping
- GUI polling for live updates

#### 📚 Dependencies
- `tkinter` (standard library)  
- `threading`, `time` (standard libraries)  
- `MeerstetterTEC` (local module)  
- `threading.Event` for thread communication

#### 🧪 Usage

```python
import tkinter as tk
from MeerstetterTEC import MeerstetterTEC
from GUI import GUI
import threading

root = tk.Tk()
tec = MeerstetterTEC(...)
start_event = threading.Event()
end_event = threading.Event()

app = GUI(root, tec, end_event, start_event)
root.mainloop()
```
---
### `MeerstetterTEC.py`

> Provides a class-based interface to communicate with a Meerstetter TEC controller over a serial connection. It includes functionality for setting temperatures, monitoring status, and executing temperature ramps over time.

#### ✅ Features
- Serial connection setup and management.
- Methods to read temperature and setpoints from the device.
- Smooth temperature ramping using time-based interpolation.
- Logging output for command execution and device feedback.

#### 📚 Dependencies
- `serial` (PySerial)
- `time`, `threading`, `os`, `sys` (standard libraries)
- `mecom.py` (inherited communication class)

#### ✍️ Key Methods
- `get_temp()`: Returns the current temperature from the TEC.
- `set_temp(temp)`: Sets the temperature setpoint on the TEC.
- `ramp_to(target_temp, ramp_time_s, end_event, start_event)`: Gradually ramps the TEC temperature to a target value over a defined period, using threading events to manage the process.

#### 🧪 Usage 
Typically used in conjunction with the GUI interface:
```python
tec = MeerstetterTEC(port='COM3')
print(tec.get_temp())
tec.set_temp(25.0)
```
---
### `automate_GUI.py`

> This module defines the automateGUI class, which provides an automation workaround for initiating scans via the Tecan software interface. Rather than communicating directly with the Tecan device, this script relies on simulating user interaction to trigger scans at specified temperature intervals.

⚠️ Note: This method is a placeholder and can be replaced by direct serial communication with the Tecan device in the future. We decided it would be too time intensive to reverse engineer the tecan's communication protocol at this point. 

#### ✅ Features
- Detects and stores the mouse position over the Tecan scan button via a guided confirmation process.
- Simulates mouse movement and clicking to trigger scans automatically.
- Integrates a temperature stabilization delay before each scan.

#### 📚 Dependencies
- pyautogui for GUI automation
- tkinter for pop-up messages and confirmation windows
- time (standard library)

#### ✍️ Key Methods
- `getButtonLocation()`: Guides the user to hover over the Tecan scan button and confirms its location after a period of  mouse inactivity.
- `scan(current_temp, hold_rate, end_ramp_event)`: Waits for the system to stabilize at the set temperature, then simulates a scan trigger.
- `clickButton()`: Moves the cursor to the confirmed location and performs a click.

#### 🧪 Usage 
- Use getButtonLocation() once during setup to define the scan button position.
- Use `clickButton()` to repeatedly trigger the Tecan to run
- This class is compatible with threaded workflows using threading.Event to synchronize with the temperature ramping process.
---

### 🧩 `data_collection.py`

> This module contains the dataCollection class and its nested graphTemp class, responsible for real-time data acquisition from the Meerstetter TEC device and live temperature visualization.

#### ✅ Features
- Fetches and logs temperature and output data from the TEC controller in real time.
- Writes collected data to a CSV file at 1-second intervals.
- Plots a live-updating temperature graph using `matplotlib`, embedded in the GUI via `tkinter`.

#### 📚 Dependencies

- `matplotlib` — for graphing and animation  
- `csv`, `time` — for data logging  
- `threading` — for concurrency and thread-safe access  
- `tkinter` — for GUI embedding (`FigureCanvasTkAgg`)

##### 🛠️ Method: `writeToCSV(end_ramp_event, tec_output_file)`
- Continuously fetches output data from the TEC device.
- Logs:
  - Timestamp
  - Object temperature
  - Output current
  - Output voltage
- Writes to a user-defined CSV file.
- Terminates when `end_ramp_event` is set.

---
#### 📊 `graphTemp` Class (Nested)

A nested class within `dataCollection` for generating a live temperature graph embedded in the GUI.

##### 🔑 Features
- Tracks time from initialization to keep the x-axis in sync with real elapsed time.
- Updates the plot every 2 seconds with new temperature data.
- Shares the data object with `dataCollection` using thread-safe access.
- Uses `matplotlib.animation.FuncAnimation` to render a smooth real-time graph.

##### 🛠️ Method: `run_animation()`
- Starts the animation loop.
- Should be called after data collection has started.

#### 💡 Usage Notes

- Instantiate `dataCollection` with a `MeerstetterTEC` object:
  
  ```python
  from data_collection import dataCollection
  tec_logger = dataCollection(tec_instance)
  ```

- Call `writeToCSV()` in a thread alongside temperature ramping:

  ```python
  threading.Thread(target=tec_logger.writeToCSV, args=(end_event, "output.csv")).start()
  ```

- After dataCollection is initialized, create a graphTemp instance and embed it in your Tkinter layout:

   ```python
  graph = tec_logger.graphTemp(parent_tk_frame)
  graph.run_animation()
  ```
---
#### 📽️ `main.py`

> This is the primary entry point for running the TEC temperature control and data collection application. It coordinates the GUI, temperature ramping logic, data logging, and thread management.

#### ⏳ Flow 
Launches the GUI and waits for user interaction to begin the ramping procedure. Once started, it manages threading for data logging and temperature control, handles real-time graphing, and safely shuts down all components when finished.

#### ✅ Features
- Initializes the TEC controller and GUI
- Uses `threading.Event` for synchronization between GUI and backend processes
- Coordinates data logging, ramping, and graphing using `ThreadManager`
- Ensures a clean shutdown of threads and GUI when the ramping is complete or the GUI is closed

**Workflow**
- TEC Initialization: Creates a MeerstetterTEC object from Temp_Ramping.
- GUI Setup: Instantiates the TECGUI.GUI with start and stop events.
- Thread Management: Uses a custom ThreadManager to manage background threads.
- Event Polling:
    - Monitors start_ramp_event to trigger ramping and data collection.
    - Monitors end_ramp_event to handle clean shutdown.

#### ✍️ Key Methods
- `main()` : Starts the GUI loop and checks for ramping initiation via start_ramp_event.
- `start_ramp_procedure(gui, MeerstetterTEC, end_ramp_event, thread_manager)`
  - Extracts user-inputted ramp parameters from the GUI.
  - Launches threads for temperature ramping and CSV logging.
  - Initializes and runs the live temperature graph.
- `handle_shutdown(gui, end_ramp_event, thread_manager)`:
  - Continuously checks for ramp termination or user shutdown.
  - Cancels all threads and gracefully closes the GUI.

#### 📚 Dependencies
- tkinter for the graphical interface
- Custom modules: `TECGUI`, `Temp_Ramping`, `dataCollection`, `thread_manager`
- threading for concurrency control

#### 💡 Usage Notes
- Run the script directly to start the application:
```bash
python main.py
```
Make sure all custom modules are accessible in the same directory or properly installed.

---

### `thread_manager.py`

>This module defines the ThreadManager class, which simplifies the creation, starting, and clean shutdown of multiple threads used throughout the TEC temperature control application.

#### 🫦 Purpose
Provides centralized management for background threads to improve code modularity and reduce redundancy. It also handles safe termination of threads using shared threading events.

#### ✅ Features
- Create and store threads for later use
- Start all threads at once
- Join threads when needed
- Terminate threads gracefully using an Event flag
- Clear the thread list for reuse

#### Class: ThreadManager
`__init__()`
- Initializes an empty list to hold thread objects.

`create_thread(target, args=())`
- Creates a thread for a given target function with arguments and adds it to the manager's list.

`start_all()`
- Starts all threads that have been created.

`join_all()`
- Waits for all threads to complete execution.

`terminate_all(end_event)`
- Signals all threads to terminate by setting a shared threading.Event. Joins any active threads to ensure clean shutdown.

`clear()`
- Removes all stored thread references to reset the manager.

#### 💡 Usage
The ThreadManager is typically used in conjunction with GUI and temperature ramping logic to start and manage:

- Data logging threads
- Temperature control threads

```python
thread_manager = ThreadManager()
thread_manager.create_thread(target_function, args=(...))
thread_manager.start_all()
...
thread_manager.terminate_all(end_event)
```

### 📁 File Structure

```
plate_reader/
│
├── main.py                  # Main script that launches the GUI and manages the temperature ramping workflow
├── TECGUI.py                # GUI layout and interaction logic using Tkinter
├── Temp_Ramping.py          # TEC temperature ramping control logic
├── dataCollection.py        # Data logging to CSV and live temperature graphing
├── automate_GUI.py          # Automates GUI-based Tecan software interactions using PyAutoGUI
├── thread_manager.py        # Utility for managing thread lifecycle
├── README.md                # Project documentation
└── requirements.txt         # List of Python dependencies
```

---

## 🔧 Installation

1. **Clone the repository**:
 ```bash
 git clone https://github.com/your-username/plate_reader.git
 cd plate_reader
 ```
2. **Create and activate a virtual environment (recommended)**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
3. **Install dependencies**:
  ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
  ```
4. **run the program**
  ```bash
  python main.py
  ```

# Contextual References

Cold Plates & Peltier Contextual videos
https://www.youtube.com/watch?v=FPFE7i7bz9Y

Glass-Transistion Thermomechanical Dye Papers 
https://pubs.rsc.org/en/content/articlelanding/2015/PY/C5PY00308C
https://www.nature.com/articles/s41467-019-11144-6

TEC (Thermo-Electric-Cooler) & Tecan Software
https://www.meerstetter.ch/customer-center/downloads/category/7-tec-family-firmware-and-service-software
https://lifesciences.tecan.com/software-overview?utm_term=tecan%20reader&utm_campaign=SO-Brand&utm_source=adwords&utm_medium=ppc&gad_source=1

Tecan Infinite M1000 User Guide
https://med.stanford.edu/content/dam/sm/htbc/documents/eq/30036266_IFU_InfiniteM1000_V1_6_English.pdf

Tecan to Python xml output code
https://github.com/choderalab/assaytools/blob/master/scripts/xml2png.py

https://www.youtube.com/watch?v=XPZUfntiyNU
https://www.youtube.com/watch?v=8l-SAYPHo9M

# Basic Functionality Illustration
![Drawing](https://github.com/zac-abero/worrell-pr/assets/109258998/2f69e544-a255-4971-b41f-86a42289b29d)

# 19-well Peltier Prototype
![ZAC01716](https://github.com/zac-abero/worrell-pr/assets/109258998/f83389a3-767a-49ca-a062-983b0e1ddbe0)
# Enclosure 
![ZAC01731](https://github.com/zac-abero/worrell-pr/assets/109258998/cd69b52c-e12f-434b-88ed-7e2234cb9df6)
# Full System
![ZAC01725](https://github.com/zac-abero/worrell-pr/assets/109258998/7ab231f6-3157-42fa-9f80-c9da2e02d09f)


# Physical Prototype Specs:

Thermoelectric-Cooling Temperature Control Board
(https://www.meerstetter.ch/products/tec-controllers/tec-1123-hv)

TEC-1163 Display (DPY-1114)
(https://www.meerstetter.ch/products/systems-software-accessories/displays/dpy-1114)

TECs (VT-127-1.4-1.5-72, POTTED)
https://tetech.com/product/vt-127-1-4-1-5-72/

PT100 Temperature Sensor
(https://www.omega.com/en-us/temperature-measurement/temperature-sensing-elements/p/PRTDCAP)

Power Supply (MeanWell)
(https://www.meanwell-web.com/en-gb/ac-dc-slim-single-output-enclosed-power-supply-uhp--1000--48)

Water Pump
(https://www.walmart.com/ip/Decdeal-Decdeal-USB-DC5V-4-8W-Ultra-quiet-Mini-Brushless-Water-Pump-Waterproof-Submersible-Fountain-Aquarium-Circulating-300L-H-Lift-300cm/801761697)

1/4" Tubing
(https://www.amazon.com/Raindrip-016010T-4-Inch-100-Feet-Tubing/dp/B0007WJIJU/ref=sr_1_3?dib=eyJ2IjoiMSJ9.YbvTkmVdmLVPed2bYIcP5rONqqpXZdJgVM41H5w5dfFWTVTs9NzhO-LmEez8_kuVXNk8cPo7TgSmFjtcl-kAl0ffjn-9RQvfCLX3lHnHb30V9h22C7vM5gtcs-CharsZV1Bmu3RruHNMVBUwPOdrypNqsfFI0UDieRJu28-PzvTgRyslPJ6KfoYIDMFteNzZswyWtU2QNP1lpVcU0R3eDoua9xoXd3hr2WVlzUWleyw.XrBf77P2imwRQ1gGlZIKsfX56glmgKf3Hb1oCdRm4V0&dib_tag=se&keywords=1%2F4+inch+black+tubing&qid=1715214868&sr=8-3)

1/8" Tubing
(https://www.amazon.com/ANPTGHT-Silicone-High-temperature-Transfer-19-68FT/dp/B0BM4KQ6RT/ref=sr_1_5?crid=1V44OIJEN3HSZ&dib=eyJ2IjoiMSJ9.dmWCpeimyMifqkekY7Tp3lztxJZqItxkqCdW-PSV825bEzymY2tQnk_CJbczmhGnD_Uf4H3s0ic_LnT9MuM08BkeZqdn6ziVE_P8zPPsqtElHv4bhZkWLAiG5yuLIpv5gC6Sv7wCMq4qQiT7F_AF-rQz9NORcXgsnJ4bx8_m6c7C5Y-nJE_7Vq6U5mbFqu18YAg7YQTSNOollNi7aoWarJlTxBDGamXvqq7JHLJeo10.tnLY4M0W1_RlApuvfaybPVCgOn74y1RO0usjSlK_YDk&dib_tag=se&keywords=1%2F8+inch+black+tubing&qid=1715214903&sprefix=1%2F8+inch+black+tubing%2Caps%2C141&sr=8-5)

1/4" to 1/8" Adapters
(https://www.amazon.com/JoyTube-Plastic-Fittings-Connectors-Aquarium/dp/B08JCCP63D?th=1)

Blue Anodized Aluminum Cooling Block
(https://www.amazon.com/Cooling-Aluminum-Computer-Industrial-Inverter/dp/B07K8LHP77/ref=sr_1_11?crid=2X5MMCKP5ENOT&dib=eyJ2IjoiMSJ9.RcXUsapNNljIWaO3aEN2YLkH6TvquXdkSBnHENVGDlGgjrXd-G-Xjyyfv_6XbJpA14g_vWqWvJJgHbWzoiLRwEXvqbF1njoFbHpIfw5KNjLMaWJYMmqrBpyJX6_Ozn73zEo8XPbUqQOYu5alZsuOztM9T8_9cF3CEJvsEFeS-hJRowQhRV-Np5Em7TJAznreOItpUwPW0UgXHj2THi8Rh2AD-hEzsYhFgrws4wnmsY_H62CZaSjmdqjnJL4QmvJBdRXK7T4lWkxW4v_PnQwdD8aMePTvVA3bQu5wYEkgSmw.9mYZEvXF67HnTI-dL8EO8x-J89_uCYIuI07CEUk86kg&dib_tag=se&keywords=aluminum+water+cooling+block+40mm+x+120mm+black&qid=1726505926&s=industrial&sprefix=aluminum+water+cooling+block+40mm+x+120mm+blac%2Cindustrial%2C130&sr=1-11)


# Print/milling files

Custom plate reader drop plate and clip for wires
https://www.printables.com/model/1009608-custom-plate-reader-tray-and-clip

19-well top plate (meant to be made from aluminum)
https://www.printables.com/model/1009621-19-well-top-plate

