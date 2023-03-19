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
        
    
    #-----------------------------------------------------------------------
    #        Methods
    #-----------------------------------------------------------------------
    """
        Creates view's frame.
    """

    def _make_base(self):
        self.title("Window Title")
        self.geometry(self.window_dim)
        self.config(bg="#e1341e")

    def _make_devices_panel(self):
        # frame in root/self
        self.devices_panel = tk.Frame(self,
                                      border=4,
                                      #   cursor="hand2",
                                      width=self.window_width * 0.25,
                                      height=self.window_height * 1,
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
                                        width=self.window_width * 0.25,
                                        height=self.window_height * 1)
        devices_content.pack()

        # canvas in devices content
        devices_list = tk.Canvas(devices_content,
                                 width=self.window_width * 0.25,
                                 height=self.window_height * 1)
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
                           width=self.window_width * 0.25,
                           height=self.window_height * 1)

        # window in devices
        devices_list.create_window((0, 0),
                                   window=devices,  # where in to create the scrollable window
                                   anchor="nw")  # basically makes the scroll start at the top

        # add buttons in devices in devices list in devices content
        for i in range(24):
            if i < 10:
                button_text = "Student0"+str(i+1)
            else:
                button_text = "Student"+str(i+1)

            device_btn = tk.Button(devices,
                                   text=button_text)
            device_btn.pack(side="top",
                            fill="both",
                            expand="yes")

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
    