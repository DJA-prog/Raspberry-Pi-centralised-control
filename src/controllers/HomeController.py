# -*- encoding:utf-8 -*-
from core.Core import Core # opens other controllers
from core.Controller import Controller # opens other views
from models.Devices import Devices


"""
    Main controller. It will be responsible for program's main screen behavior.
"""
class HomeController(Controller):

    current_device_id = 0
    device_info_data = []

    #-----------------------------------------------------------------------
    #        Constructor
    #-----------------------------------------------------------------------
    def __init__(self):
        self.devices = Devices()
        self.core = Core()
        self.current_device_id = self.devices.get_first_device_id()

        # load homeView after
        self.homeView = self.loadView("Home")

        # self.homeView.devices_data = self.devices.get_devices_status_list()

    #-----------------------------------------------------------------------
    #        Methods
    #-----------------------------------------------------------------------
    def getDevices(self):
        return self.devices.get_devices_status_list()
    
    def getDeviceAplications(self, device_id):
        return self.devices.get_device_applications(device_id)
    
    def getCurrentDeviceId(self):
        return self.current_device_id
    
    def setCurrentDeviceId(self, device_id):
        self.current_device_id = device_id

    def getDeviceInfo(self, device_id):
        return self.devices.get_device_info(device_id)
    
    def ribbonControl(self, code):
        if (code == "EXIT"):
            self.exit_application()
        elif (code == "REFRESH"):
            # c = Core.openController("loader")
            # c.refresh()
            if self.devices.update_devices_csv():
                self.homeView.update_devices_list(self.getDevices())
                # pass
        elif (code == "RESTART ALL"):
            self.devices.restart_all()
        elif (code == "SHUTDOWN ALL"):
            self.devices.shutdown_all()
        elif (code == "START DEFAULT"):
            pass
    
    def deviceControl(self, code):
        # print(f"CODE: {code}, DEVICE ID: {self.current_device_id}")
        if (code == "SHUTDOWN"):
            self.devices.device_shutdown(self.current_device_id)
        elif (code == "RESTART"):
            self.devices.device_restart(self.current_device_id)
        elif (code == "DEFAULT"):
            self.devices.device_default(self.current_device_id)

    def exit_application(self):
        self.devices.notify_exit()
        self.homeView.close()

    """
        @Override
    """
    def main(self):
        self.homeView.main()
