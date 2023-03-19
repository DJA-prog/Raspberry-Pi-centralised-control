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
class HomeView(tk.Tk, View):
    #-----------------------------------------------------------------------
    #        Constants
    #-----------------------------------------------------------------------
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
    
    applications_data = [
        ["Remmina", "inactive"],
        ["TypeSpeed", "inactive"],
        ["Chrome", "inactive"],
        ["Firefox", "inactive"],
        ["LibreOffice", "inactive"]
    ]

    controls = ["EXIT", "REFRESH", "RESTART ALL",
                "SHUTDOWN ALL", "START DEFAULT"]
    
    device_info_data = [
        ["Hostname", "wordpropi01"],
        ["IP", "192.168.1.1"],
        ["Username", "pi"],
        ["Status", "Offline"]
    ]

    device_controls = [
        ["SHUTDOWN", "active"],
        ["RESTART", "active"],
        ["DEFAULT (remmina)", "inactive"]
    ]
    
    #-----------------------------------------------------------------------
    #        Constructor
    #-----------------------------------------------------------------------
    """
        @param controller Controller of this view
    """
    def __init__(self, controller):
        super().__init__()
        # self.attributes('-fullscreen', True)
        self.homeController = controller
        
        # order of window building
        self._make_base()
        self._make_devices_panel()
        self._make_device_controls()
        self._make_control_ribbon()
        self._make_applications_panel() # update on device change
        self._make_device() # update on device change
        
    
    #-----------------------------------------------------------------------
    #        Methods
    #-----------------------------------------------------------------------
    """
        Creates view's frame.
    """

 # create self / main
    def _make_base(self):
        self.title("Raspberry Pi Centralised Control")
        self.geometry(self.window_dim)
        self.config(bg="#e1341e")

    # inside of self / main
    def _make_devices_panel(self):
        devices_panel_width = self.window_width * 0.2
        devices_panel_height = self.window_height * 1
        # frame in root/self
        self.devices_panel = tk.Frame(self,
                                      border=4,
                                      width=devices_panel_width,
                                      height=devices_panel_height,
                                      relief="flat",  # border type
                                      borderwidth=0)
        self.devices_panel.pack(side="left", fill='y')

        # Label at the top in devices panel
        devices_panel_label = tk.Label(self.devices_panel,
                                       cursor="arrow",
                                       text="DEVICES",
                                       font=["Arial", 14],
                                       relief="raised",
                                       borderwidth=2,
                                       padx=5,
                                       pady=5)
        devices_panel_label.config(anchor="center")  # centers the label text
        devices_panel_label.pack(side="top", fill='x')

        # frame bellow devices label
        devices_content = tk.LabelFrame(self.devices_panel,
                                        width=devices_panel_width,
                                        height=devices_panel_height)
        devices_content.pack(fill='y', expand=True)

        # canvas in devices content
        devices_list = tk.Canvas(devices_content,
                                 width=devices_panel_width,
                                 height=devices_panel_height)
        devices_list.pack(side="left",
                          fill="both",
                          expand="yes")

        # intialize scrollbar
        yscrollbar = ttk.Scrollbar(devices_content,
                                   orient="vertical",
                                   command=devices_list.yview)
        yscrollbar.pack(side="right", fill="y")

        # configure
        devices_list.configure(yscrollcommand=yscrollbar.set)

        # e: pass event
        devices_list.bind("<Configure>",
                          lambda e: devices_list.configure(
                              scrollregion=devices_list.bbox("all")))

        # frame in devices lists
        devices = tk.Frame(devices_list,
                           width=devices_panel_width,
                           height=devices_panel_height)

        # window in devices
        devices_list.create_window((0, 0),
                                   window=devices,  # where in to create the scrollable window
                                   anchor="nw")  # basically makes the scroll start at the top

        # add buttons in devices in devices list in devices content
        for device in self.devices_data:
            device_btn = tk.Button(devices,
                                   cursor="hand2",  # cursor type
                                   text=device[0],
                                   width=15)

            if device[1] == "online":
                device_btn.config(bg="green")
            elif device[1] == "offline":
                device_btn.config(bg="red")
            else:
                device_btn.config(bg="blue")

            device_btn.config(fg="white",
                              font=["Arial", 12])  # font

            device_btn.pack(side="top",
                            fill="both",
                            expand="yes")

    # inside of self / main
    def _make_device_controls(self):
        self.device_controls_width = self.window_width * 0.82
        self.device_controls_height = self.window_height * 1.0
        # frame in root
        self.device_control = tk.Frame(self,
                                       border=0,
                                       width=self.device_controls_width,
                                       height=self.device_controls_height)
        self.device_control.pack(side="right", fill="both", expand=True)

    # inside of device control
    def _make_applications_panel(self):
        applications_panel_width = self.device_controls_width * 0.25
        applications_panel_height = self.device_controls_height * 1
        # frame in device_controls
        self.applications_panel = tk.Frame(self.device_control,  # location
                                           border=4,
                                           #   cursor="hand2", # cursor type
                                           width=applications_panel_width,  # panel width
                                           height=applications_panel_height,  # panel height
                                           relief="flat",  # border type
                                           borderwidth=0)  # border width
        self.applications_panel.pack(side="right", fill='y')

        # Label at the top in applications panel
        applications_panel_label = tk.Label(self.applications_panel,  # location
                                            cursor="arrow",  # cursor type
                                            text="APPLICATIONS",  # label text
                                            font=["Arial", 14],  # font
                                            relief="raised",  # border type
                                            borderwidth=2,  # border width
                                            padx=5,  # x sides padding
                                            pady=5)  # y sides padding
        applications_panel_label.config(
            anchor="center")  # centers the label text
        applications_panel_label.pack(side="top", fill='x')

        # frame bellow applications label
        applications_content = tk.LabelFrame(self.applications_panel,
                                             width=applications_panel_width,
                                             height=applications_panel_height)
        applications_content.pack()

        # canvas in applications content
        applications_list = tk.Canvas(applications_content,
                                      width=applications_panel_width,
                                      height=applications_panel_height)
        applications_list.pack(side="left",
                               fill="both",
                               expand="yes")

        # intialize scrollbar
        yscrollbar = ttk.Scrollbar(applications_content,
                                   orient="vertical",
                                   command=applications_list.yview)
        yscrollbar.pack(side="right", fill="y")

        # configure
        applications_list.configure(yscrollcommand=yscrollbar.set)

        # e: pass event
        applications_list.bind("<Configure>",
                               lambda e: applications_list.configure(
                                   scrollregion=applications_list.bbox("all")))

        # frame in applications lists
        applications = tk.Frame(applications_list,
                                width=applications_panel_width,
                                height=applications_panel_height)

        # window in applications
        applications_list.create_window((0, 0),
                                        window=applications,  # where in to create the scrollable window
                                        anchor="nw")  # basically makes the scroll start at the top

        # add buttons in applications in applications list in applications content
        for application in self.applications_data:
            app_btn = tk.Button(applications,
                                cursor="hand2",  # cursor type
                                text=application[0],
                                width=15)

            app_btn.config(fg="white",
                           font=["Arial", 12])  # font

            if application[1] == "active":
                app_btn.config(bg="green")
            elif application[1] == "inactive":
                app_btn.config(bg="grey", fg="black")
            else:
                app_btn.config(bg="red")

            app_btn.pack(side="top",
                         fill="both",
                         expand="yes")

    # inside of device control
    def _make_control_ribbon(self):
        control_ribbon_width = self.device_controls_width * 1.0
        control_ribbon_height = self.device_controls_height * 0.1
        # frame in device_control
        self.control_ribbon = tk.Frame(self.device_control,  # location
                                       border=4,
                                       #   cursor="hand2", # cursor type
                                       width=control_ribbon_width,  # panel width
                                       height=control_ribbon_height,  # panel height
                                       relief="flat",  # border type
                                       borderwidth=0,  # border width
                                       pady=4)  # padding top and bottom
        self.control_ribbon.pack(side="bottom", fill='x')

        # add buttons in control ribbon
        for control in self.controls:
            control_btn = tk.Button(self.control_ribbon,  # location
                                    cursor="hand2",  # cursor type
                                    text=control,  # button text
                                    width=10,  # width
                                    padx=1)  # padding left and right
            if control == "EXIT":
                control_btn.config(bg="red")

            control_btn.pack(side="right",
                             fill="both",
                             expand="yes")

    # inside of device control
    def _make_device(self):
        device_panel_width = self.device_controls_width * 0.75
        device_panel_height = self.device_controls_height * 0.9
        # frame in device_control
        self.device_panel = tk.Frame(self.device_control,  # location
                                     border=4,
                                     width=device_panel_width,  # panel width
                                     height=device_panel_height,  # panel height
                                     relief="flat",  # border type
                                     borderwidth=0)  # border width
        self.device_panel.pack(side="top", fill='both', expand=True)

        # Label in device_panel
        device_label = tk.Label(self.device_panel,  # location
                                cursor="arrow",
                                text="DEVICE",
                                font=["Arial", 14],
                                relief="raised",
                                borderwidth=2,
                                padx=5,
                                pady=5)
        device_label.config(anchor="center")  # centers the label text
        device_label.pack(side="top", fill='x')

        # frame in device_control under title
        device_info = tk.Frame(self.device_panel,  # location
                               width=device_panel_width)  # panel width
        device_info.pack(side="top", fill='both', expand=True)

        # table in device info
        treeView = ttk.Treeview(device_info,
                                columns=(1, 2),
                                show="headings",
                                height=5)
        treeView.pack(side="top", fill='both')

        treeView.heading(1, text="Field")
        treeView.heading(2, text="Value")

        for info in self.device_info_data:
            treeView.insert('', "end", values=info)

        # frame in device info
        device_control = tk.Frame(device_info, # location
                                relief="flat",  # border type
                                borderwidth=0,  # border width
                                pady=4)  # padding top and bottom
        device_control.pack(side="top", fill='x')

        # add buttons in device control
        for control in self.device_controls:
            control_btn = tk.Button(device_control,  # location
                                    cursor="hand2",  # cursor type
                                    text=control[0],  # button text
                                    width=10,  # width
                                    padx=1)  # padding left and right

            control_btn.pack(side="right",
                             fill="both",
                             expand="yes")
                                  

        # frame in device_control under device info
        app_info = tk.Frame(self.device_panel,  # location
                            width=device_panel_width)  # panel width
        app_info.pack(side="top", fill='both', expand=True)

        # label in app_info
        app_info_title = tk.Label(app_info,  # location
                                  text="APPLICATION INFO",
                                  font=["Arial", 12],
                                  relief="groove",
                                  borderwidth=1,
                                  padx=2,
                                  pady=2)
        app_info_title.pack(side="top", fill='x', expand=True)

    """
    @Overrite
    """
    def main(self):
        self.mainloop()
        
    """
    @Overrite
    """
    def close(self):
        return
    