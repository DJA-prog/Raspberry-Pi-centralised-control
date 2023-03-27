import tkinter as tk
from tkinter import *
from tkinter import ttk
from views.View import View


"""
    View associated with HomeController. It will be responsible for program's 
    main screen view.

    extends / copy tk.Tk as its own, essentially making the current class a 
    Tk on its own and therefor no extra instance needs to be initialized
"""


class HomeView(tk.Tk):

    # variables
    window_width = 800
    window_height = 600
    window_dim = str(window_width) + "x" + str(window_height)
    welcomed = False

    devices_data = [
        # [1, "Student01", "unknown"],
        # [2, "Student02", "unknown"],
        # [3, "Student03", "unknown"],
        # [4, "Student04", "unknown"],
        # [5, "Student05", "unknown"],
        # [6, "Student06", "unknown"]
    ]

    device_info = []

    application_data = [
        # ["Remmina", "inactive"],
        # ["TypeSpeed", "inactive"],
        # ["Chrome", "inactive"],
        # ["Firefox", "inactive"],
        # ["LibreOffice", "inactive"]
    ]

    global_controls = [
        ["EXIT", "exit"],
        ["REFRESH", "refresh"],
        ["RESTART ALL", "restart_all"],
        ["SHUTDOWN ALL", "shutdown_all"],
        ["DEFAULT", "default"]
    ]

    device_control = [
        ["SHUTDOWN", "shutdown"],
        ["RESTART", "restart"],
        ["DEFAULT", "default"]
    ]

    current_device_id = 1

    current_device_info = None

    current_appication_info = None

    def __init__(self, controller):
        super().__init__()
        self.homeController = controller

        # get data
        self.current_device_id = self.homeController.getCurrentDeviceId()
        self.devices_data[:] = self.homeController.getDevices()
        self.application_data = self.homeController.getDeviceAplications(self.current_device_id)
        self.current_appication_info = self.application_data[0]

        # build gui
        self._make_root()

        self._make_panel_devices_list()
        self._make_panel_devices_list_content()

        self._make_panel_controls()
        self._make_panel_controls_global_controls()

        if self.welcomed:
            self.display_device_info()

    # BUILD GUI

    def _make_root(self):
        self.title("Home")
        self.geometry(self.window_dim)
        self.config(bg="#1ECBE1")

    # left devices panel in root
    def _make_panel_devices_list(self):
        self.panel_devices_list_width = self.window_width * 0.2
        self.panel_devices_list_height = int(self.window_height * 1.0)
        self.panel_devices_list = tk.Frame(self,
                                           border=4,
                                           width=self.panel_devices_list_width,
                                           height=self.panel_devices_list_height,
                                           relief="raised",
                                           borderwidth=2)
        self.panel_devices_list.pack(side="left", fill='y')

        panel_devices_list_label = tk.Label(self.panel_devices_list,
                                            text="DEVICES",
                                            font=["Arial", 14],
                                            relief="raised",
                                            borderwidth=2,
                                            padx=5,
                                            pady=5)
        panel_devices_list_label.config(anchor="center")
        panel_devices_list_label.pack(side="top", fill='x')

    # devices list in panel devices list (Updatable)
    def _make_panel_devices_list_content(self):
        self.panel_devices_list_inner_frame = tk.Frame(self.panel_devices_list,
                                                       width=self.panel_devices_list_width,
                                                       height=self.panel_devices_list_height)
        self.panel_devices_list_inner_frame.pack(fill='y', expand=True)

        self.panel_devices_list_canvas = tk.Canvas(self.panel_devices_list_inner_frame,
                                                   width=self.panel_devices_list_width,
                                                   height=self.panel_devices_list_height)
        self.panel_devices_list_canvas.pack(
            side="left", fill="both", expand=True)

        yscrollbar = ttk.Scrollbar(self.panel_devices_list_inner_frame,
                                   orient="vertical",
                                   command=self.panel_devices_list_canvas.yview)
        yscrollbar.pack(side="right", fill='y')

        self.panel_devices_list_canvas.configure(yscrollcommand=yscrollbar.set)

        self.panel_devices_list_canvas.bind("<Configure>",
                                            lambda e: self.panel_devices_list_canvas.configure(
                                                scrollregion=self.panel_devices_list_canvas.bbox(
                                                    "all")
                                            ))

        devices_list = tk.Frame(self.panel_devices_list_canvas,
                                width=self.panel_devices_list_width,
                                height=self.panel_devices_list_height)

        self.panel_devices_list_canvas.create_window((0, 0),
                                                     window=devices_list,
                                                     anchor="nw")

        for device in self.devices_data:
            device_btn = tk.Button(devices_list,
                                   cursor="hand2",
                                   text=device[1],
                                   width=15,
                                   command=lambda id=device[0]: self.setDeviceId(id))
            # print(f"Device: {device[1]}; Status: {device[2]}")
            if device[2].lower() == "online":
                device_btn.config(bg="green")
            elif device[2].lower() == "offline":
                device_btn.config(bg="red")
            else:
                device_btn.config(bg="blue")

            device_btn.config(fg="white", font=["Arial", 12])

            device_btn.pack(side="top", fill="both", expand=True)

    # right control panel in root
    def _make_panel_controls(self):
        self.panel_controls_width = int(self.window_width * 0.8)
        self.panel_controls_height = int(self.window_height * 1.0)
        self.panel_controls = tk.Frame(self,
                                       border=0,
                                       width=self.panel_controls_width,
                                       height=self.panel_controls_height)
        self.panel_controls.pack(side="right", fill='both', expand=True)

    # global controls in control panel at the bottom
    def _make_panel_controls_global_controls(self):
        self.panel_controls_global_controls_width = int(
            self.panel_controls_width * 0.1)
        self.panel_controls_global_controls_height = int(
            self.panel_controls_height * 0.1)
        self.panel_controls_global_controls = tk.Frame(self.panel_controls,
                                                       width=self.panel_controls_global_controls_width,
                                                       height=self.panel_controls_global_controls_height,
                                                       relief="raised",
                                                       borderwidth=2,
                                                       pady=1)
        self.panel_controls_global_controls.pack(side="bottom", fill='x')

        for control in self.global_controls:
            control_button = tk.Button(self.panel_controls_global_controls,
                                       cursor="hand2",
                                       text=control[0],
                                       width=10,
                                       padx=1,
                                       command=lambda x=control[0]: self.homeController.ribbonControl(x))
            if control[0] == "EXIT":
                control_button.config(bg="red")

            control_button.pack(side="right", fill="both", expand=True)

    # applications list in control panel
    def _make_panel_controls_applications(self):
        self.panel_controls_applications_width = self.panel_controls_width * 0.25
        self.panel_controls_applications_height = int(
            self.panel_controls_height * 1.0)
        self.panel_controls_applications_controls = tk.Frame(self.panel_controls,
                                                             border=0,
                                                             width=self.panel_controls_applications_width,
                                                             height=self.panel_controls_applications_height,
                                                             relief="raised",
                                                             borderwidth=2)
        self.panel_controls_applications_controls.pack(side="right", fill='y')

        panel_controls_applications_controls_label = tk.Label(self.panel_controls_applications_controls,
                                                              text="Applications",
                                                              font=[
                                                                  "Arial", 14],
                                                              relief="raised",
                                                              borderwidth=2,
                                                              padx=5,
                                                              pady=5)
        panel_controls_applications_controls_label.config(anchor="center")
        panel_controls_applications_controls_label.pack(side="top", fill='x')

    # applications list in controls applications (Updatable)
    def _make_panel_controls_applications_content(self):
        self.panel_controls_applications_inner_frame = tk.Frame(self.panel_controls_applications_controls,
                                                                width=self.panel_controls_applications_width,
                                                                height=self.panel_controls_applications_height)

        self.panel_controls_applications_inner_frame.pack(
            fill='y', expand=True)

        self.panel_controls_applications_canvas = tk.Canvas(self.panel_controls_applications_inner_frame,
                                                            width=self.panel_controls_applications_width,
                                                            height=self.panel_controls_applications_height)
        self.panel_controls_applications_canvas.pack(
            side="left", fill="both", expand=True)

        yscrollbar = ttk.Scrollbar(self.panel_controls_applications_inner_frame,
                                   orient="vertical",
                                   command=self.panel_controls_applications_canvas.yview)
        yscrollbar.pack(side="right", fill='y')

        self.panel_controls_applications_canvas.configure(
            yscrollcommand=yscrollbar.set)

        self.panel_controls_applications_canvas.bind("<Configure>",
                                                     lambda e: self.panel_controls_applications_canvas.configure(
                                                         scrollregion=self.panel_controls_applications_canvas.bbox(
                                                             "all")
                                                     ))

        applications_list = tk.Frame(self.panel_controls_applications_canvas,
                                     width=self.panel_controls_applications_width,
                                     height=self.panel_controls_applications_height)

        self.panel_controls_applications_canvas.create_window((0, 0),
                                                              window=applications_list,
                                                              anchor="nw")

        for application in self.application_data:
            device_btn = tk.Button(applications_list,
                                   cursor="hand2",
                                   text=application["name"],
                                   width=15,
                                   command=lambda x=application["name"]: self.update_appication_info(x))

            if application["status"] == "active":
                device_btn.config(bg="green")
            elif application["status"] == "inactive":
                device_btn.config(bg="grey")
            else:
                device_btn.config(bg="blue")

            device_btn.config(fg="white", font=["Arial", 12])

            device_btn.pack(side="top", fill="both", expand=True)

    # device and application info in controls panel
    def _make_panel_controls_device(self):
        self.panel_controls_device_width = self.panel_controls_width * 0.75
        self.panel_controls_device_height = int(
            self.panel_controls_height * 1.0)
        self.panel_controls_device = tk.Frame(self.panel_controls,
                                              border=4,
                                              width=self.panel_controls_device_width,
                                              height=self.panel_controls_device_height,
                                              relief="flat",
                                              borderwidth=0)
        self.panel_controls_device.pack(side="top", fill="both", expand=True)

        self.panel_controls_device_label = tk.Label(self.panel_controls_device,
                                                    text="DEVICE",
                                                    font=["Arial", 14],
                                                    relief="raised",
                                                    borderwidth=2,
                                                    padx=5,
                                                    pady=5)
        self.panel_controls_device_label.config(anchor="center")
        self.panel_controls_device_label.pack(side="top", fill='x')

    # device info panel in controls device panel
    def _make_panel_controls_device_info_panel(self):
        self.panel_controls_device_info_panel_width = self.panel_controls_device_width * 1.0
        self.panel_controls_device_info_panel_height = int(
            self.panel_controls_device_height * 0.5)
        self.panel_controls_device_info_panel = tk.Frame(self.panel_controls_device,
                                                         border=4,
                                                         width=self.panel_controls_device_info_panel_width,
                                                         height=self.panel_controls_device_info_panel_height,
                                                         relief="flat",
                                                         borderwidth=0)
        self.panel_controls_device_info_panel.pack(side="top")
        panel_controls_device_info_panel_label = tk.Label(self.panel_controls_device_info_panel,
                                                          text="Info",
                                                          font=["Arial", 14],
                                                          relief="raised",
                                                          borderwidth=2,
                                                          padx=5,
                                                          pady=5)
        panel_controls_device_info_panel_label.config(anchor="center")
        panel_controls_device_info_panel_label.pack(side="top", fill='x')

    # device info in device info panel (Updatable)
    def _make_panel_controls_device_info_panel_content(self):
        self.panel_controls_device_info_panel_content_width = self.panel_controls_device_info_panel_width
        self.panel_controls_device_info_panel_content_height = int(
            self.panel_controls_device_info_panel_height * 1.0)
        self.panel_controls_device_info_panel_content = tk.Frame(self.panel_controls_device_info_panel,
                                                                 border=4,
                                                                 width=self.panel_controls_device_info_panel_content_width,
                                                                 height=self.panel_controls_device_info_panel_content_height,
                                                                 relief="flat",
                                                                 borderwidth=0)
        self.panel_controls_device_info_panel_content.pack(
            side="top", fill="both", expand=True)

        # create table
        panel_controls_device_info_panel_content_table = ttk.Treeview(self.panel_controls_device_info_panel_content,
                                                                      columns=("option", "value"),
                                                                      show="headings")
        panel_controls_device_info_panel_content_table.heading("option",text="Option")
        panel_controls_device_info_panel_content_table.heading("value",text="Value")
        panel_controls_device_info_panel_content_table.column("option", stretch=YES)
        panel_controls_device_info_panel_content_table.column("value", stretch=YES)
        panel_controls_device_info_panel_content_table.pack(side="top", fill="both", expand=True)
        # insert data
        info_index = 0
        for info in self.device_info:
            panel_controls_device_info_panel_content_table.insert(parent = '', index=info_index, values=info)
            info_index += 1
        
        # device control
        panel_controls_device_info_panel_content_control = tk.Frame(self.panel_controls_device_info_panel_content,
                                                                    border=4,
                                                                    width=self.panel_controls_device_info_panel_content_width,
                                                                    relief="flat",
                                                                    borderwidth=0)
        panel_controls_device_info_panel_content_control.pack(
            side="top", fill='x', expand=True)

        for control in self.device_control:
            button = tk.Button(panel_controls_device_info_panel_content_control,
                               cursor="hand2",
                               text=control[0],
                               width=10,
                               padx=1,
                               command=lambda x=control[0]: self.homeController.deviceControl(x))
            button.pack(side="right", fill="both", expand=True)

    # application info panel in controls device panel
    def _make_panel_controls_application_info_panel(self):
        self.panel_controls_application_info_panel_width = self.panel_controls_device_width
        self.panel_controls_application_info_panel_height = int(
            self.panel_controls_device_height * 0.5)
        self.panel_controls_application_info_panel = tk.Frame(self.panel_controls_device,
                                                              border=4,
                                                              width=self.panel_controls_application_info_panel_width,
                                                              height=self.panel_controls_application_info_panel_height,
                                                              relief="flat",
                                                              borderwidth=0)
        self.panel_controls_application_info_panel.pack(side="top")
        panel_controls_application_info_panel_label = tk.Label(self.panel_controls_application_info_panel,
                                                               text="APP INFO",
                                                               font=[
                                                                   "Arial", 14],
                                                               relief="raised",
                                                               borderwidth=2,
                                                               padx=5,
                                                               pady=5)
        panel_controls_application_info_panel_label.config(anchor="center")
        panel_controls_application_info_panel_label.pack(side="top", fill='x')

    # application info in device info panel (Updatable)
    def _make_panel_controls_application_info_panel_content(self):
        self.panel_controls_application_info_panel_content_width = self.panel_controls_application_info_panel_width
        self.panel_controls_application_info_panel_content_height = int(
            self.panel_controls_application_info_panel_height * 1.0)
        self.panel_controls_application_info_panel_content = tk.Frame(self.panel_controls_application_info_panel,
                                                                      border=4,
                                                                      width=self.panel_controls_application_info_panel_content_width,
                                                                      height=self.panel_controls_application_info_panel_content_height,
                                                                      relief="flat",
                                                                      borderwidth=0)
        self.panel_controls_application_info_panel_content.pack(
            side="top", fill="both", expand=True)
        # create table
        panel_controls_application_info_panel_content_table = ttk.Treeview(self.panel_controls_application_info_panel_content,
                                                                      columns=("option", "value"),
                                                                      show="headings")
        panel_controls_application_info_panel_content_table.heading("option",text="Option")
        panel_controls_application_info_panel_content_table.heading("value",text="Value")
        panel_controls_application_info_panel_content_table.column("option", stretch=YES)
        panel_controls_application_info_panel_content_table.column("value", stretch=YES)
        panel_controls_application_info_panel_content_table.pack(side="top", fill="both", expand=True)
        # insert data
        info_index = 0
        for info_key, info_value in self.current_appication_info.items():
            panel_controls_application_info_panel_content_table.insert(parent = '', index=info_index, values=(info_key, info_value))
            info_index += 1


    # UPDATE GUI
    def display_device_info(self): # self.display_device_info()
        if self.welcomed == False:
            self._make_panel_controls_applications()
            self._make_panel_controls_applications_content()
            self._make_panel_controls_device()
            # self._make_panel_controls_device_label()
            self._make_panel_controls_device_info_panel()
            self._make_panel_controls_device_info_panel_content()
            self._make_panel_controls_application_info_panel()
            self._make_panel_controls_application_info_panel_content()
            self.welcomed = True

    def update_devices_list(self, new_devices_list=None):
        self.display_device_info()
        if new_devices_list is not None:
            # self.devices_data.clear()
            self.devices_data = new_devices_list
        self.panel_devices_list_inner_frame.destroy()
        self._make_panel_devices_list_content()

    def update_applications_list(self, new_applications_list=None):
        self.display_device_info()
        if new_applications_list is not None:
            self.application_data = new_applications_list
        self.panel_controls_applications_inner_frame.destroy()
        self._make_panel_controls_applications_content()

    def update_device_label(self, new_device_id=None):
        self.display_device_info()
        if int(self.current_device_id) < 10:
            label_text = "STUDENT: 0" + str(self.current_device_id)
        else:
            label_text = "STUDENT: " + str(self.current_device_id)
        self.panel_controls_device_label.configure(text=label_text)

    def update_device_info(self, new_device_info=None):
        self.display_device_info()
        if new_device_info is not None:
            self.current_device_info = new_device_info
        self.panel_controls_device_info_panel_content.destroy()
        self._make_panel_controls_device_info_panel_content()

    def update_appication_info(self, application_name = None, new_appication_info=None):
        self.display_device_info()
        if new_appication_info is not None:
            self.current_appication_info = new_appication_info
        if application_name is not None:
            app_pos = 0
            for app in self.application_data:
                if app["name"] == application_name:
                    self.current_appication_info = self.application_data[app_pos]
                    break
                app_pos += 1
        else:
            self.current_appication_info = self.application_data[0]
        self.panel_controls_application_info_panel_content.destroy()
        self._make_panel_controls_application_info_panel_content()

    def setDeviceId(self, device_id):
        self.current_device_id = device_id
        self.homeController.setCurrentDeviceId(device_id)
        # get applications
        self.application_data = self.homeController.getDeviceAplications(self.current_device_id)
        # print(f"Set current device id: {self.current_device_id}")
        # print(self.application_data)
        #get device information
        self.device_info = self.homeController.getDeviceInfo(self.current_device_id)

        self.update_appication_info()
        self.update_applications_list()
        self.update_device_label()
        self.update_device_info()

    def main(self):
        self.mainloop()
