from config import APP_PATH
import csv


"""
    Model description
"""
class Devices:

    devices_csv = APP_PATH+"/storage/devices.csv"
    devices_data = []
    device_info_data = []

    device_application_json = APP_PATH+"/storage/devices_application_data.json"
    device_application_data = []


    def __init__(self):
        # self.devices_list =
        pass


    def get_devices_status_list(self):
        with open(self.devices_csv, 'r') as csvfile:
            devices_list = csv.DictReader(
                csvfile, delimiter=',', quotechar='|')
        
            for line in devices_list:
                self.devices_data.append([line["id"], line["referred_name"], line["status"]])

        return self.devices_data
    
    def get_first_device_id(self):
        with open(self.devices_csv, 'r') as csvfile:
            devices_list = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(devices_list)

            for line in devices_list:
                self.device_info_data = line[0]
                break

        return self.device_info_data
    
    def get_device_info(self, device_id):
        with open(self.devices_csv, 'r') as csvfile:
            devices_list = csv.DictReader(
                csvfile, delimiter=',', quotechar='|')
            
            for line in devices_list:
                # print(f"Line: {line['id']} : Device_id: {device_id}")
                if int(line["id"]) == int(device_id):
                    self.device_info_data = [
                        ["Hostname", line["hostname"]],
                        ["IP", line["ip"]],
                        ["Username", line["username"]],
                        ["Status", line["status"]]
                    ]
                    return self.device_info_data
            
            self.device_info_data = [
                ["Hostname", "N/A"],
                ["IP", "N/A"],
                ["Username", "N/A"],
                ["Status", "N/A"]
            ]

        return self.device_info_data

    # ["Hostname", "wordpropi01"],
    # ["IP", "192.168.1.1"],
    # ["Username", "pi"],
    # ["Status", "Offline"]
