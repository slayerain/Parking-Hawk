import tkinter as tk
from tkinter import ttk


class scroller(tk.Frame):
    def __init__(self, parent, **kwargs):
        try:
            super().__init__(parent, **kwargs)
            self.frame_deploy()
        except Exception as e:
            print(f"Error: {e}")
    def frame_deploy(self):
        self.mainframe = tk.Frame(self, highlightthickness=0)
        self.mainframe.pack(fill=tk.BOTH, side=tk.LEFT, expand=1, anchor=tk.NW)
        self.canvas = tk.Canvas(self.mainframe, highlightthickness=0)
        self.frame = tk.Frame(self.canvas)
        self.scrollbar = ttk.Scrollbar(self.mainframe, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(fill=tk.BOTH, expand=0, side=tk.LEFT)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, anchor=tk.NE)
        self.canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)
        self.frame.bind("<Configure>", lambda event, canvas=self.canvas: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self.update_scroll_region)
        self.frame.bind("<Configure>", self.update_scroll_region)
        self.frame.bind("<Enter>", self.enter_mousewheel, add="+")
        self.frame.bind("<Leave>", self.leave_mousewheel)
    def update_scroll_region(self, *event):
        self.canvas.update_idletasks()
        self.frame.update_idletasks()
        frame_width = self.frame.winfo_width()
        frame_height = self.frame.winfo_height()
        self.canvas.configure(scrollregion=(0,0, frame_width, frame_height))
        self.canvas.configure(width=frame_width, height=frame_height)
        if self.frame.winfo_height() <= self.canvas.winfo_height():
            self.scrollbar.pack_forget()
            self.canvas.configure(yscrollcommand=None)
            self.canvas.unbind("<Enter>")
            self.canvas.unbind_all("<MouseWheel>")
        else:
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.canvas.configure(yscrollcommand=self.scrollbar.set)
            self.canvas.bind("<Enter>", self.enter_mousewheel, add="+")
        self.canvas.configure(scrollregion=(0, 0, self.frame.winfo_width(), self.frame.winfo_height()))
    def top(self):self.canvas.yview_moveto(0.0)
    def refresh(self):
        try:
            self.canvas.update_idletasks()
            self.frame.update_idletasks()
            self.update_scroll_region()
            self.canvas.yview_moveto(0.0)
        except Exception as e:
            print(f"Error: {e}")
    def delete(self):
        try:
            if self.frame.winfo_children():
                for widgets in self.frame.winfo_children(): widgets.destroy()
        except Exception as e:
            print(f"Error: {e}")
    def on_mousewheel(self, event): self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    def enter_mousewheel(self, event): self.canvas.bind_all('<MouseWheel>', self.on_mousewheel, add="+")
    def leave_mousewheel(self, event): self.canvas.unbind_all('<MouseWheel>')
    def grid_config(self, weight_vals):
        for i, weight in enumerate(weight_vals):
            self.frame.grid_columnconfigure(i, weight=weight)




root = tk.Tk()
root.attributes("-fullscreen", True)

test_frame = tk.Frame(root, highlightthickness=0)
test_frame.pack()
# Use the root window as the parent for the scroller
adm_T_C_scroller = scroller(test_frame)
adm_T_C_scroller.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)  # Pack with fill=BOTH and expand=1

for i in range(100):
    label = tk.Label(adm_T_C_scroller.frame, text=f"Label {i + 1}", width=10)
    label.pack(side=tk.TOP, fill=tk.Y)

adm_T_C_scroller.refresh()
adm_T_C_scroller.top()

root.mainloop()
