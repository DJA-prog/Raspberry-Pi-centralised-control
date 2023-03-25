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
class explore(tk.Tk):

    # variables
    window_width = 800
    window_height = 600
    window_dim = str(window_width) + "x" + str(window_height)

    devices_data = [
        ["Student01", "unknown"],
        ["Student02", "unknown"],
        ["Student03", "unknown"],
        ["Student04", "unknown"],
        ["Student05", "unknown"],
        ["Student06", "unknown"]
    ]

    application_data = [
        ["Remmina", "inactive"],
        ["TypeSpeed", "inactive"],
        ["Chrome", "inactive"],
        ["Firefox", "inactive"],
        ["LibreOffice", "inactive"]
    ]

    global_controls = [
        ["EXIT", "exit"],
        ["REFRESH", "refresh"],
        ["RESTART ALL", "restart_all"],
        ["SHUTDOWN ALL", "shutdown_all"],
        ["DEFAULT", "default"]
    ]

    current_device_id = 1

    current_device_info = None

    current_appication_info = None

    def __init__(self):
        super().__init__()

        # build gui
        self._make_root()

        self._make_panel_devices_list()
        self._make_panel_devices_list_content()

        self._make_panel_controls()
        self._make_panel_controls_global_controls()
        self._make_panel_controls_applications()
        self._make_panel_controls_applications_content()

        self._make_panel_controls_device()
        self._make_panel_controls_device_label()
        self._make_panel_controls_device_info_panel()
        self._make_panel_controls_device_info_panel_content()
        self._make_panel_controls_application_info_panel()
        self._make_panel_controls_application_info_panel_content()

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
                                           relief="flat",
                                           borderwidth=0)
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
                                   text=device[0],
                                   width=15)

            if device[1].lower == "online":
                device_btn.config(bg="green")
            elif device[1].lower == "offline":
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
                                                       relief="flat",
                                                       borderwidth=0,
                                                       pady=4)
        self.panel_controls_global_controls.pack(side="bottom", fill='x')

        for control in self.global_controls:
            control_button = tk.Button(self.panel_controls_global_controls,
                                       cursor="hand2",
                                       #    command= lambda x=control[1]: self
                                       text=control[0],
                                       width=10,
                                       padx=1)
            control_button.pack(side="right", fill="both", expand=True)

    # applications list in control panel
    def _make_panel_controls_applications(self):
        self.panel_controls_applications_width = self.panel_controls_width * 0.25
        self.panel_controls_applications_height = int(
            self.panel_controls_height * 1.0)
        self.panel_controls_applications_controls = tk.Frame(self.panel_controls,
                                                             border=4,
                                                             width=self.panel_controls_applications_width,
                                                             height=self.panel_controls_applications_height,
                                                             relief="flat",
                                                             borderwidth=0)
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

        for application in self.devices_data:
            device_btn = tk.Button(applications_list,
                                   cursor="hand2",
                                   text=application[0],
                                   width=15)

            if application[1].lower == "active":
                device_btn.config(bg="green")
            elif application[1].lower == "inactive":
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

    # label for device and application info in controls device panel (Updatable)
    def _make_panel_controls_device_label(self):
        if self.current_device_id < 10:
            label_text = "DEVICE: 0" + str(self.current_device_id)
        else:
            label_text = "DEVICE: " + str(self.current_device_id)
        self.panel_controls_device_label = tk.Label(self.panel_controls_device,
                                                    text=label_text,
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

    # UPDATE GUI

    def update_devices_list(self, new_devices_list=None):
        if new_devices_list is not None:
            self.devices_data = new_devices_list
        self.panel_devices_list_inner_frame.destroy()
        self._make_panel_devices_list_content()

    def update_applications_list(self, new_applications_list=None):
        if new_applications_list is not None:
            self.application_data = new_applications_list
        self.panel_controls_applications_inner_frame.destroy()
        self._make_panel_controls_applications_content()

    def update_device_label(self, new_device_id=None):
        if new_device_id is not None:
            self.current_device_id = int(new_device_id)
        self.panel_controls_device_label.destroy()
        self._make_panel_controls_device_label()

    def update_device_info(self, new_device_info=None):
        if new_device_info is not None:
            self.current_device_info = new_device_info
        self.panel_controls_device_info_panel_content.destroy()
        self._make_panel_controls_device_info_panel_content()

    def update_appication_info(self, new_appication_info=None):
        if new_appication_info is not None:
            self.current_appication_info = new_appication_info
        self.panel_controls_application_info_panel_content.destroy()
        self._make_panel_controls_application_info_panel_content()

    def show(self):
        self.mainloop()
