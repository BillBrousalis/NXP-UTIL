#!/usr/bin/env python3
def generate_config():
                 
  config_dict = {"VERSION": 0.2,
                 "MAX-DEV": 1,
                 "RPI-IP": "192.168.1.15",
                 "RPI-PORT": 9001,
                 "BYTES-PER-LINE": 130,
                 "COMMANDS": True,  # / True
                 "UART-BAUD": 115200,
                 "DEBUG": True,
                 "LOGGING": None,   # "PI" / "CLIENT"
                 "LOGGING-PATH-RPI": "logs/rpi_logs.csv",
                 "LOGGING-PATH-CLIENT": "logs/client_logs.csv"
  }
  fname = "config.yaml"

  with open(fname, "w") as f:
    import yaml
    yaml.dump(config_dict, f)
    print(f"[*] {fname} has been generated")

if __name__ == "__main__":
  generate_config()
