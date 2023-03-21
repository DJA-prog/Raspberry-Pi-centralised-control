import os
from config import APP_PATH
from models.Scan import Scan
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
        self.scanModel = Scan()
        pass

    def update_devices_csv(self):
        print("Updating devices csv")

        # Create a temporary file for writing the updated CSV data
        temp_file = self.devices_csv + ".tmp"

        # Open the input CSV file for reading
        with open(self.devices_csv, 'r') as csv_in_file:
            # Open the temporary file for writing
            with open(temp_file, 'w', newline='') as csv_out_file:
                # Create a CSV reader object
                csv_reader = csv.reader(csv_in_file, delimiter=',', quotechar='|')

                # Create a CSV writer object
                csv_writer = csv.writer(csv_out_file, delimiter=',', quotechar='|')

                # Loop through each row in the CSV file
                for row in csv_reader:
                    print(row[0])

                    # Update the row as needed
                    if row[0] != "id":
                        host_check = self.scanModel.check_host(row[2])
                        row[3] = host_check[1]  # set ip
                        if host_check[0]:
                            row[7] = "online"
                        elif not host_check[0]:
                            row[7] = "offline"
                        else:
                            row[7] = "unknown"

                    # Write the updated row to the temporary file
                    csv_writer.writerow(row)

        # Replace the input CSV file with the temporary file
        os.replace(temp_file, self.devices_csv)

        print("Updated devices csv")

    def restart_all(self):
        with open(self.devices_csv, 'r') as csvfile:
            devices_list = csv.DictReader(csvfile, delimiter=',', quotechar='|')

            for line in devices_list:
                if line["exempted"] == "false" and self.scanModel.is_device_online(line["hostname"]):
                    self.scanModel.execute_remote_command(line["hostname"], line["username"], line["password"], "sudo reboot & exit")

    def shutdown_all(self):
        with open(self.devices_csv, 'r') as csvfile:
            devices_list = csv.DictReader(csvfile, delimiter=',', quotechar='|')

            for line in devices_list:
                if line["exempted"] == "false" and self.scanModel.is_device_online(line["hostname"]):
                    self.scanModel.execute_remote_command(line["hostname"], line["username"], line["password"], "sudo shutdown now & exit")
                

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

    def notify_exit(self):
        # Perform any necessary cleanup tasks here
        # ...

        # Exit the program
        import sys
        sys.exit()
