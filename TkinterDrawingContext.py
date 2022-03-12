import tkinter
from TimeLinePlot import AbstractDrawingContext, TimeLinePlot

class TkinterWindowDrawingContext(AbstractDrawingContext, tkinter.Tk):

    def __init__(self, window_width, window_height, title='Time line', time_line_width=1000, time_line_height=300):
        super().__init__()

        # window setup
        self.resizable(False, False)
        self.title('TimeLinePlot')
        self.iconbitmap('./stat.ico')

        time_line_width = max(time_line_width, window_width)

        # setup in-frame title
        self.title_label_frame = tkinter.Frame(height=window_height-time_line_height, width=window_width, bg='#0c0c0c')
        self.title_label = tkinter.Label(self.title_label_frame, text=title, font='Arial 28', bg='#0c0c0c', fg='#e5e5e5')
        self.title_label.place(relx=.5, rely=.5,anchor=tkinter.CENTER)
        self.title_label_frame.pack_propagate(0)
        self.title_label_frame.grid(row=0, column=0)

        # setup canvas
        self.canvas_frame = tkinter.Frame(self, width=window_width)
        self.canvas_frame.grid(row=1, column=0)
        self.canvas = tkinter.Canvas(self.canvas_frame, width=window_width, highlightthickness=0)

        # setup horizontal bar for scrolling
        self.h_bar = tkinter.Scrollbar(self.canvas_frame, orient=tkinter.HORIZONTAL)
        self.h_bar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.h_bar.config(command=self.canvas.xview)
        self.h_bar.update()

        self.canvas.pack()

        time_line_height -= self.h_bar.winfo_height()

        self.canvas.config(width=window_width, height=time_line_height, scrollregion=(0, 0, time_line_width, time_line_height), xscrollcommand=self.h_bar.set)

        # setup parameters for the drawing context
        self.line_width = 1
        self.time_line_canvas_width = time_line_width
        self.time_line_canvas_height = time_line_height

    def draw_polygon(self, color, border_color=None, border_width=0, *points):
        self.canvas.create_polygon(points, outline=border_color, width=border_width, fill=color)

    def clear(self):
        self.canvas.delete(tkinter.ALL)

    def get_width(self):
        return self.time_line_canvas_width

    def get_height(self):
        return self.time_line_canvas_height

    def set_line_width(self, w):
        self.line_width = w

    def set_pixel(self, x, y, color):
        self.canvas.create_rectangle(x, y, x+1, y+1, fill=color)

    def draw_line(self, x0, y0, x1, y1, color):
        self.canvas.create_line(x0, y0, x1, y1, fill=color, width=self.line_width)

    def draw_ellipse(self, x, y, r1, r2, color):
        self.canvas.create_oval(x, y, x+r1*2, y+r2*2, fill=color, width=0)

    def draw_rect(self, x0, y0, x1, y1, color):
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=0)

    def draw_text(self, x, y, text, font, color, rotation=0, anchor=''):
        self.canvas.create_text(x, y, text=text, font=font, anchor=anchor, fill=color, angle=rotation)

if __name__ == '__main__':
    # json
    test_data = [
        {'time': '1997-08-02T01:12:00', 'message': 'Switched versions:\nv0.0.1 to v1.0.1', 'title': 'Company A'},
        {'time': '1928-08-14T14:11:00', 'message': 'Switched versions:\nv0.0.1 to v2.0.1', 'title': 'Company B'},
        {'time': '1937-08-14T14:11:00', 'message': 'Switched versions:\nv0.0.1 to v2.0.1', 'title': 'Company C'},
        {'time': '1937-12-30T05:15:00', 'message': 'Switched versions:\nv1.0.1 to v3.0.1', 'title': 'Company D'},
        {'time': '1941-12-30T05:15:00', 'message': 'Switched versions:\nv1.0.1 to v3.0.1', 'title': 'Company E'},
        {'time': '2001-02-28T10:01:00', 'message': 'Switched versions:\nv3.0.1 to v4.0.1', 'title': 'Company F'},
        {'time': '2001-02-28T10:01:00', 'message': 'Switched versions:\nv3.0.1 to v4.0.1', 'title': 'Company G'},
        {'time': '2011-05-10T20:58:00', 'message': 'Switched versions:\nv2.0.1 to v5.0.1', 'title': 'Company H'},
    ]
    TimeLinePlot(
        data=test_data.copy(),
        background_color='#0c0c0c',
        time_line_color='#bb86fc',
        entry_frame_color='#bb86fc',
        entry_text_color='#e5e5e5',
        entry_card_background='#1f1f1f'
    ).draw(TkinterWindowDrawingContext(1000, 400, title='companies switching versions', time_line_width=3000)).mainloop()