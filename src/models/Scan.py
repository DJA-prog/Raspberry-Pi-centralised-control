import socket
import paramiko
import subprocess

class Scan:
    def __init__(self):
        pass

    # check if hostname is online and if so what is the IP address. return tuple (status, ip)
    def check_host(self, hostname):
        print("Checking hostname: " + hostname)
        try:
            # Use the ping command to check if the hostname is online
            ping_response = subprocess.call(['ping', '-c', '2', hostname])

            # Get the IP address of the hostname
            ip_address = socket.gethostbyname(hostname)

            # Return the results
            if ping_response == 0:
                return (True, ip_address)
            else:
                return (False, ip_address)
        except:
            # If an exception occurs, assume the hostname is offline
            return (False, "")


    # confirm if device is online
    def is_device_online(self, hostname):
        # Ping the hostname and capture the output
        ping_process = subprocess.Popen(
            ["ping", "-c", "3", hostname], stdout=subprocess.PIPE)
        ping_output = ping_process.stdout.read().decode()

        # Check if the output contains the string "3 received"
        if "3 received" in ping_output:
            return True
        else:
            return False

    # execute command with password
    def execute_remote_command(self, hostname, username, password, command):
        # Create an SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote device
        client.connect(hostname=hostname, username=username, password=password)

        # Execute the command and capture the output
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()

        # Close the SSH client
        client.close()

        # Return the output of the command
        return output

    # test if password is needed
    def requires_password(self, hostname, username):
        # Create an SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Try to connect to the remote device without a password
        try:
            client.connect(hostname=hostname, username=username,
                        allow_agent=False, look_for_keys=False)
            # If the connection succeeds, no password is required
            return False
        except paramiko.AuthenticationException:
            # If the connection fails, a password is required
            return True
        finally:
            # Close the SSH client
            client.close()
