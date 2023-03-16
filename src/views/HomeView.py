import tkinter as tk
from tkinter import ttk
from views.View import View


"""
    View associated with HomeController. It will be responsible for program's 
    main screen view.
"""
class HomeView(tk.Tk, View):
    #-----------------------------------------------------------------------
    #        Constants
    #-----------------------------------------------------------------------
    PAD = 10
    devices = [
        ["Student 01", "online"],
        ["Student 02", "online"],
        ["Student 03", "offline"]
    ]
    
    #-----------------------------------------------------------------------
    #        Constructor
    #-----------------------------------------------------------------------
    """
        @param controller Controller of this view
    """
    def __init__(self, controller):
        super().__init__()
        self.title("Raspberry Pi Centralised Control") 
        # self.attributes('-fullscreen', True)
        self.homeController = controller
        
        self._make_mainFrame()
        self._make_device_buttons()
        # self._make_title()
        # self._make_options()
        
    
    #-----------------------------------------------------------------------
    #        Methods
    #-----------------------------------------------------------------------
    """
        Creates view's frame.
    """
    def _make_mainFrame(self):
        self.mainFrame = ttk.Frame(self)
        self.mainFrame.pack(padx=self.PAD, pady=self.PAD)
        # self.mainFrame.attributes('-fullscreen', True)

    
    """
        Side Panel
    """
    def _make_side_panel(self):
        pass

    
    def _make_device_buttons(self):
        left_panel = ttk.Frame(self.mainFrame) # hold all buttons
        left_panel.pack() # default append to bottom

        # loop through buttons
        for device in self.devices:
            btn = ttk.Button(
                left_panel, 
                text=device[0],
                # command=(lambda button=caption: self.controller.on_button_click(button)), # command run when the button is clicked
                width = 20
                ) # create the button
            btn.pack() # append to bottom

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
    