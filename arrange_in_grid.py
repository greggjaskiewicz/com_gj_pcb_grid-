import pcbnew
import wx
import math

def sort_key(fp):
    ref = fp.GetReferenceAsString()
    digits = ''.join(ch for ch in ref if ch.isdigit())
    return int(digits) if digits else 0

class GridArrangeDialog(wx.Dialog):
    def __init__(self, parent):
        super(GridArrangeDialog, self).__init__(parent, title="Grid Arrange Footprints", size=(300, 200))
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Horizontal spacing input
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h_label = wx.StaticText(panel, label="Horizontal Spacing (mm):")
        self.h_text = wx.TextCtrl(panel, value="10")
        h_sizer.Add(h_label, 0, wx.ALL | wx.CENTER, 5)
        h_sizer.Add(self.h_text, 1, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(h_sizer, 0, wx.EXPAND)
        
        # Vertical spacing input
        v_sizer = wx.BoxSizer(wx.HORIZONTAL)
        v_label = wx.StaticText(panel, label="Vertical Spacing (mm):")
        self.v_text = wx.TextCtrl(panel, value="10")
        v_sizer.Add(v_label, 0, wx.ALL | wx.CENTER, 5)
        v_sizer.Add(self.v_text, 1, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(v_sizer, 0, wx.EXPAND)
        
        # Update button to trigger grid re-arrangement
        update_btn = wx.Button(panel, label="Update")
        update_btn.Bind(wx.EVT_BUTTON, self.on_update)
        main_sizer.Add(update_btn, 0, wx.ALL | wx.CENTER, 10)
        
        panel.SetSizer(main_sizer)
        self.Centre()

    def on_update(self, event):
        try:
            h_spacing = float(self.h_text.GetValue())
            v_spacing = float(self.v_text.GetValue())
        except ValueError:
            wx.MessageBox("Please enter valid numeric values for spacing.", "Input Error", wx.OK | wx.ICON_ERROR)
            return

        self.arrange_footprints(h_spacing, v_spacing)

    def arrange_footprints(self, h_spacing_mm, v_spacing_mm):
        board = pcbnew.GetBoard()
        footprints = [fp for fp in board.GetFootprints() if fp.IsSelected()]
        if not footprints:
            wx.MessageBox("No footprints selected.", "Error", wx.OK | wx.ICON_ERROR)
            return

        footprints.sort(key=sort_key)
        count = len(footprints)
        cols = int(math.ceil(math.sqrt(count)))
        base_pos = footprints[0].GetPosition()
        
        for i, fp in enumerate(footprints):
            col = i % cols
            row = i // cols
            new_x = base_pos.x + int(pcbnew.FromMM(h_spacing_mm) * col)
            new_y = base_pos.y + int(pcbnew.FromMM(v_spacing_mm) * row)
            new_pos = pcbnew.VECTOR2I(new_x, new_y)
            fp.SetPosition(new_pos)
        
        pcbnew.Refresh()
#
## For testing the plugin outside of KiCAD, you can run it directly:
#if __name__ == '__main__':
#    GridArrangePlugin().Run()
