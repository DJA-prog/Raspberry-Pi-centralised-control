from config import APP_PATH
import threading


class FileWatchdog(threading.Thread):
    def __init__(self, model):
        threading.Thread.__init__(self)
        self.model = model
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            self.check_files()
            self.stop_event.wait(60)  # Check files every 60 seconds

    def check_files(self):
        for file in self.model.files:
            # Check for file size, file type, and file permissions
            if file.size > 1000000:
                self.model.remove_file(file)
                self.notify_controller("File size too large")
            elif file.type != "pdf":
                self.model.remove_file(file)
                self.notify_controller("Invalid file type")
            elif not file.is_accessible():
                self.model.remove_file(file)
                self.notify_controller("File permission denied")

    def notify_controller(self, message):
        self.model.controller.notify(message)
