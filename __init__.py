from pathlib import Path

import pcbnew, wx

from .arrange_in_grid import GridArrangeDialog

class ArrangeInGridAction(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Grid Arrange Footprints"
        self.category = "Modify PCB"
        self.description = "Arrange selected footprints in a grid with configurable spacing"
        self.show_toolbar_button = True
        self.icon_file_name = (
            Path(__file__).parent / "images" / "grid.png").as_posix()

    def Run(self):
        # Ensure a wx App exists (KiCAD may have one already running)
        app = wx.GetApp()
        if not app:
            app = wx.App(False)
        dlg = GridArrangeDialog(None)
        dlg.ShowModal()
        dlg.Destroy()

ArrangeInGridAction().register()

# For testing the plugin outside of KiCAD, you can run it directly:
if __name__ == '__main__':
    ArrangeInGridAction().Run()
