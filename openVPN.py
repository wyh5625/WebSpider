import subprocess
import time
import signal
import psutil

vpn_process = None

def run_vpn(config_path):
    global vpn_process
    if vpn_process is not None:
        terminate_vpn()  # Gracefully terminate the existing VPN process

    command = [
        "sudo", "openvpn",
        "--config", config_path,
        "--auth-user-pass", "credentials.txt"
    ]

    vpn_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def add_default_route():
    # Command to add the default route
    command = ["sudo", "route", "add", "default", "192.168.0.1"]

    try:
        # Execute the command
        subprocess.run(command, check=True)
        print("Default route added successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error adding default route: {e}")

def terminate_vpn():
    global vpn_process
    if vpn_process is not None:
        try:
            # Gracefully terminate the OpenVPN process
            vpn_process.terminate()
            vpn_process.wait()  # Wait for the process to terminate
            print("VPN process terminated gracefully.")
            add_default_route()
            print("Add default route.")
        except psutil.NoSuchProcess:
            print("VPN process not found.")
        except psutil.AccessDenied:
            print("Permission denied to terminate VPN process.")

# Example usage
run_vpn("US-ovpn-tcp.ovpn")
time.sleep(10)  # Simulate some operations
terminate_vpn()  # Terminate the VPN process gracefully