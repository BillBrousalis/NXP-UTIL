# [ NXP CUP Util ]

**Debugging the NXP Cup Car, and visualizing data.**

**Avoid fiddling with embedded code and have `Python3` aid you in your algorithm development.**

**The Trifecta**:

![](assets/trifecta.png)

## **TL;DR: Setup**
Install required `Python3` packages:

```
pip install -r requirements.txt
```

Set up your configuration by editing `config/config.yaml`.

**Raspberry-PI:**

```
./rpi-run
```

for setting the some config options on-the-fly, check out
```
./rpi-run -h
```

**Client(s):**

```
.\CarDbgGUI.exe
```
or run the `Python3` script
```
python3 CarDbgGUI.py
```

## **Basic Idea**

### Generic Debugging

* Car --> Raspberry-PI: `UART` Connection
* Raspberry-PI --> Client(s): `WIFI` Connection

Transmit your car's **crucial data**, such as:
  * Linescan Camera Output
  * Steering Angle and
  * Vehicle Speed

over to your machine for viewing and proccessing, all in `real-time`.

### Development

Receive the LineScan's data and let your `RPI` take the wheel!

Use the `Commands` Mode to control the car with the RPI!

Develop and experiment with algorithms in `Python3` for quick prototyping,
see they work, and ***then*** write them in `C`!

## **Building**

If modifications are needed, you can rebuild your `.exe` / `binary` executable:

```
pyinstaller --onefile --nowindowed --icon="assets/rpi.ico" --distpath="bin/" --name="CarDbgGUI.exe" src/client/CarDbgGUI.py
```

## **The Raspberry-PI**

The Raspberry-PI allows `multiple clients` to view and visualize the transmitted data
simultaneously.

Basic `dnsmasq` / `hostapd` setup for WIFI access.

**Optional**: Use `systemd` to run on startup.

## **Graphical User Interface**

Makes the `ip:port` connection to the server.

Visualizing linescan output in real-time using `Matplotlib` graphing.

Steering Angle and Vehicle Speed available for viewing.

## **COMMANDS mode:**

The car can be controlled using the Raspberry-PI by setting speed and steering - Run the car in commands mode.

Develop your algorithm in `Python3` before writting large amounts of C code.

Runs `server-side` for speed.

Not super fast, but useful nontheless.

**Recommended (if not debugging):** 0 Clients

## **LOGGING mode:**

[TODO]: Logging option (None / "PI" / "CLIENT") to keep logs in selected device.
