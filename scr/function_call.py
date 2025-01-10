from datetime import datetime
import json
import re
from scr.utils import data_path
def get_weather(location: str, start_time: str, stop_time: str, view_mode: str):
    """
    Simulates fetching weather data for a given location within a specified time range and view mode.

    Parameters:
        location (str): The name of the location.
        start_time (str): The start time in the format 'YYYY-MM-DD HH:MM:SS'.
        stop_time (str): The stop time in the format 'YYYY-MM-DD HH:MM:SS'.
        view_mode (str): The view mode, e.g., 'summary', 'detailed'.

    Returns:
        dict: Simulated weather data or an error message.
    """
    try:
        start = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        stop = datetime.strptime(stop_time, '%Y-%m-%d %H:%M:%S')
        if stop < start:
            return {"status": "error", "error": "Stop time must be after start time."}
    except ValueError:
        return {"status": "error", "error": "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'."}

    # Simulate different responses based on location and `view_mode`.
    if location == "Hanoi":
        if view_mode == "summary":
            data = {
                "status": "success",
                "location": location,
                "start_time": start_time,
                "stop_time": stop_time,
                "summary": {
                    "average_temperature": "25°C",
                    "rainfall": "15mm",
                    "humidity": "70%"
                }
            }
        elif view_mode == "detailed":
            data = {
                "status": "success",
                "location": location,
                "start_time": start_time,
                "stop_time": stop_time,
                "hourly_forecast": [
                    {"time": "2024-12-16 08:00:00", "temperature": "24°C", "condition": "Cloudy"},
                    {"time": "2024-12-16 09:00:00", "temperature": "25°C", "condition": "Rainy"},
                    {"time": "2024-12-16 10:00:00", "temperature": "26°C", "condition": "Partly Cloudy"}
                ]
            }
    elif location == "New York":
        if view_mode == "summary":
            data = {
                "status": "success",
                "location": location,
                "start_time": start_time,
                "stop_time": stop_time,
                "summary": {
                    "average_temperature": "10°C",
                    "rainfall": "5mm",
                    "humidity": "50%"
                }
            }
        elif view_mode == "detailed":
            data = {
                "status": "success",
                "location": location,
                "start_time": start_time,
                "stop_time": stop_time,
                "hourly_forecast": [
                    {"time": "2024-12-16 08:00:00", "temperature": "8°C", "condition": "Sunny"},
                    {"time": "2024-12-16 09:00:00", "temperature": "9°C", "condition": "Windy"},
                    {"time": "2024-12-16 10:00:00", "temperature": "10°C", "condition": "Cloudy"}
                ]
            }
    elif location == "Tokyo":
        if view_mode == "summary":
            data = {
                "status": "success",
                "location": location,
                "start_time": start_time,
                "stop_time": stop_time,
                "summary": {
                    "average_temperature": "18°C",
                    "rainfall": "0mm",
                    "humidity": "65%"
                }
            }
        elif view_mode == "detailed":
            data = {
                "status": "success",
                "location": location,
                "start_time": start_time,
                "stop_time": stop_time,
                "hourly_forecast": [
                    {"time": "2024-12-16 08:00:00", "temperature": "17°C", "condition": "Sunny"},
                    {"time": "2024-12-16 09:00:00", "temperature": "18°C", "condition": "Clear"},
                    {"time": "2024-12-16 10:00:00", "temperature": "19°C", "condition": "Sunny"}
                ]
            }
    else:
        data = {"status": "error", "error": f"Unknown location: {location}. Supported locations are 'Hanoi', 'New York', 'Tokyo'."}

    return data

def setup_server(server_name: str, ip_address: str, port: str, os_type: str, cpu_cores: str, memory_gb: str, storage_gb: str):
    """
    Simulates setting up a server with multiple independent parameters.

    Parameters:
        server_name (str): The name of the server.
        ip_address (str): The IP address of the server.
        port (str): The port number for the server.
        os_type (str): The operating system type (e.g., 'Linux', 'Windows').
        cpu_cores (str): The number of CPU cores.
        memory_gb (str): The amount of memory in GB.
        storage_gb (str): The amount of storage in GB.

    Returns:
        dict: Simulated result of the server setup process.
    """
    # Convert parameters to appropriate types
    try:
        port = int(port)
        cpu_cores = int(cpu_cores)
        memory_gb = int(memory_gb)
        storage_gb = int(storage_gb)
    except ValueError:
        return {"status": "error", "error": "Invalid parameter type. Ensure port, cpu_cores, memory_gb, and storage_gb are integers."}

    # Validate parameters
    if not (0 < port < 65536):
        return {"status": "error", "error": "Invalid port number. Must be between 1 and 65535."}
    if cpu_cores <= 0:
        return {"status": "error", "error": "CPU cores must be greater than 0."}
    if memory_gb <= 0:
        return {"status": "error", "error": "Memory must be greater than 0 GB."}
    if storage_gb <= 0:
        return {"status": "error", "error": "Storage must be greater than 0 GB."}
    if os_type not in ["Linux", "Windows"]:
        return {"status": "error", "error": "Unsupported OS type. Must be 'Linux' or 'Windows'."}

    # Simulate server setup process
    result = {
        "status": "success",
        "server_name": server_name,
        "ip_address": ip_address,
        "port": port,
        "os_type": os_type,
        "cpu_cores": cpu_cores,
        "memory_gb": memory_gb,
        "storage_gb": storage_gb,
        "message": "Server setup completed successfully."
    }
    return result



def search_device_by_id(dev_id: str):
    """
    Searches for a device in the JSON database by its ID.

    Parameters:
        devID (str): The ID of the device to search for.

    Returns:
        dict: The device information if found, otherwise an error message.
    """
    # Validate device ID format
    if not re.fullmatch(r'[A-Z]\d{5}', dev_id):
        return {"status": "error", "error": "Invalid device ID format. Must be one uppercase letter followed by five digits."}

    try:
        with open(data_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for key, device in data.items():
            if device.get("devID") == dev_id:
                return {"status": "success", "device": device}

        return {"status": "error", "error": f"Device with ID '{dev_id}' not found."}
    except FileNotFoundError:
        return {"status": "error", "error": f"Database file '{data_path}' not found."}
    except json.JSONDecodeError:
        return {"status": "error", "error": "Error decoding JSON from the database file."}

def search_device_by_name(dev_name: str):
    """
    Searches for a device in the JSON database by its name.

    Parameters:
        dev_name (str): The name of the device to search for.

    Returns:
        dict: The device information if found, otherwise an error message.
    """
    # Validate device name format (example pattern, adjust as necessary)
    if not isinstance(dev_name, str) or len(dev_name.strip()) == 0:
        return {"status": "error", "error": "Invalid device name format. Name must be a non-empty string."}

    try:
        with open(data_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for key, device in data.items():
            if device.get("Name") and dev_name.lower() == device["Name"].lower():
                return {"status": "success", "device": device}

        return {"status": "error", "error": f"Device with name '{dev_name}' not found."}
    except FileNotFoundError:
        return {"status": "error", "error": f"Database file '{data_path}' not found."}
    except json.JSONDecodeError:
        return {"status": "error", "error": "Error decoding JSON from the database file."}


def config_sampling_rate(dev_id: str, sampling_rate: str):
    """
    Configures the sampling rate for a device.

    Parameters:
        dev_id (str): The name of the device.
        sampling_rate (str): The sampling rate to set.

    Returns:
        dict: Result of the configuration.
    """
    # Simulate configuration process
    result = {
        "status": "success",
        "dev_id": dev_id,
        "sampling_rate": sampling_rate,
        "message": "Sampling rate configuration completed successfully."
    }
    return result

def config_sending_rate(dev_id: str, sending_rate: str):
    """
    Configures the sending rate for a device.

    Parameters:
        dev_id (str): The name of the device.
        sending_rate (str): The sending rate to set.

    Returns:
        dict: Result of the configuration.
    """
    # Simulate configuration process
    result = {
        "status": "success",
        "dev_id": dev_id,
        "sending_rate": sending_rate,
        "message": "Sending rate configuration completed successfully."
    }
    return result

def config_reset_device(dev_id: str):
    """
    Resets a device.

    Parameters:
        dev_id (str): The name of the device.

    Returns:
        dict: Result of the reset.
    """
    # Simulate reset process
    result = {
        "status": "success",
        "dev_id": dev_id,
        "message": "Device reset completed successfully."
    }
    return result

def config_update_rtc(dev_id: str):
    """
    Updates the RTC (Real-Time Clock) for a device.

    Parameters:
        dev_id (str): The name of the device.

    Returns:
        dict: Result of the RTC update.
    """
    # Simulate RTC update process
    result = {
        "status": "success",
        "dev_id": dev_id,
        "message": "RTC update completed successfully."
    }
    return result

def config_update_new_firmware(dev_id: str):
    """
    Updates the firmware for a device.

    Parameters:
        dev_id (str): The name of the device.

    Returns:
        dict: Result of the firmware update.
    """
    # Simulate firmware update process
    result = {
        "status": "success",
        "dev_id": dev_id,
        "message": "Firmware update completed successfully."
    }
    return result

def execute_function(function_name: str, args: dict):
    """
    Executes a function based on the function name and arguments provided.

    Parameters:
        function_name (str): The name of the function to execute.
        args (dict): The arguments to pass to the function.

    Returns:
        Any: The result of the function execution.
    """

    if function_name in available_functions:
        return available_functions[function_name](**args)
    else:
        return {"status": "error", "error": f"Function '{function_name}' not recognized."}


# ----------------------------------AVAILABLE FUNCTIONS----------------------------------
available_functions = {
    "get_weather": get_weather,
    "setup_server": setup_server,
    "search_device_by_id": search_device_by_id,
    "search_device_by_name": search_device_by_name,
    "config_sampling_rate": config_sampling_rate,
    "config_sending_rate": config_sending_rate,
    "config_reset_device": config_reset_device,
    "config_update_rtc": config_update_rtc,
    "config_update_new_firmware": config_update_new_firmware,
    "search_device_by_name": search_device_by_name,
}

search_functions = {
    "search_device_by_id": "dev_id", 
    "search_device_by_name": "dev_name"
}

function_descriptions = '''
"get_weather": "Lấy thông tin thời tiết.",
"setup_server": "Thiết lập máy chủ.",
"search_device_by_id": "Tìm kiếm thiết bị theo devID.",
"search_device_by_name": "Tìm kiếm thiết bị theo Name.",
"config_sampling_rate": "Cài đặt tần số lấy mẫu.",
"config_sending_rate": "Cài đặt tần số gởi dữ liệu.",
"config_reset_device": "Khởi động lại thiết bị.",
"config_update_rtc": "Cập nhật thời gian thực (RTC) cho thiết bị.",
"config_update_new_firmware": "Cập nhật firmware mới cho thiết bị.",
'''


