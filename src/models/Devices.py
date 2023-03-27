import os
from config import APP_PATH
from models.Scan import Scan
import csv
import json
import paramiko

"""
    Model description
"""
class Devices:

    devices_csv = APP_PATH+"/storage/devices.csv"
    devices_data = []
    device_info_data = []

    device_application_json = APP_PATH+"/storage/devices_application_data.json"
    device_application_data = None
    device_application_open = False


    def execute_ssh_command(self, hostname, username, password, command):
        # Create a new SSH client
        ssh = paramiko.SSHClient()
        # Automatically add the server's host key
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Connect to the server
        ssh.connect(hostname=hostname, username=username, password=password)
        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(command)
        # Read the output and error streams
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        # Close the SSH connection
        ssh.close()
        # Return the output and error streams
        return output, error

    def __init__(self):
        self.scanModel = Scan()
        pass

    def update_devices_csv(self):
        # print("Updating devices csv")

        # Create a temporary file for writing the updated CSV data
        temp_file = self.devices_csv + ".tmp"

        # Open the input CSV file for reading
        with open(self.devices_csv, 'r') as csv_in_file:
            # Open the temporary file for writing
            with open(temp_file, 'w', newline='') as csv_out_file:
                # print(f"Opened: {temp_file} & {self.devices_csv}")
                # Create a CSV reader object
                csv_reader = csv.reader(csv_in_file, delimiter=',', quotechar='|')

                # Create a CSV writer object
                csv_writer = csv.writer(csv_out_file, delimiter=',', quotechar='|')

                # print("Reading Rows...")
                # Loop through each row in the CSV file
                for row in csv_reader:
                    # print(row[0])

                    # Update the row as needed
                    if row[0] != "id":
                        host_check = self.scanModel.check_host(row[2])
                        print(f"Host status: {host_check}")
                        row[3] = host_check[1]  # set ip
                        if host_check[0] != False :
                            row[8] = "online"
                        elif host_check[0] == False:
                            row[8] = "offline"
                        else:
                            row[8] = "unknown"

                    # print(f"Writing: {row}")
                    # Write the updated row to the temporary file
                    csv_writer.writerow(row)

        # Replace the input CSV file with the temporary file
        os.replace(temp_file, self.devices_csv)

        print("Updated devices csv")
        return True

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

    def get_device_data(self, device_id):
        with open(self.devices_csv, 'r') as csvfile:
            devices_list = csv.DictReader(
                csvfile, delimiter=',', quotechar='|')

            for line in devices_list:
                # print(f"Line: {line['id']} : Device_id: {device_id}")
                if int(line["id"]) == int(device_id):
                    device_data = {
                        "hostname":line["hostname"],
                        "ip":line["ip"],
                        "username": line["username"],
                        "password": line["password"],
                        "use_password": line["use_pass"],
                        "status":line["status"]
                    }
                    return device_data

        return device_data

    def device_shutdown(self, device_id):
        data = self.get_device_data(device_id)
        if data["status"].lower() == "online":
            output = self.scanModel.execute_remote_command(
                data["hostname"], data["username"], data["password"], "sudo shutdown now & exit")
            print(output)

    def device_restart(self, device_id):
        data = self.get_device_data(device_id)
        if data["status"].lower() == "online":
            print(data["hostname"])
            output = self.scanModel.execute_remote_command(
                data["hostname"], data["username"], data["password"], "sudo reboot & exit")
            print(output)

    def device_default(self, device_id):
        data = self.get_device_data(device_id)
        if data["status"].lower() == "online":
            pass

    def readJson(self):
        if self.device_application_open is False:
            self.application_json_file = open(self.device_application_json, 'r')
            self.appication_json_data = self.application_json_file.read()
            #parse
            self.device_application_data = json.loads(self.appication_json_data)
            self.device_appication_open = True

    def get_device_applications(self, device_id):
        self.readJson()
        return self.device_application_data[str(device_id)]

    def get_devices_status_list(self):
        with open(self.devices_csv, 'r') as csvfile:
            devices_list = csv.DictReader(
                csvfile, delimiter=',', quotechar='|')

            self.devices_data.clear()
        
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
