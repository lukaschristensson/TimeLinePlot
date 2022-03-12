import datetime


class AbstractDrawingContext:   # quack quack
    def set_pixel(self, x, y, color):
        raise NotImplementedError
    def draw_line(self, x0, y0, x1, y1, color):
        raise NotImplementedError
    def draw_ellipse(self, x, y, r1, r2, color):
        raise NotImplementedError
    def draw_text(self, x, y, text, font, color, rotation=0, anchor=''):
        raise NotImplementedError
    def set_line_width(self, w):
        raise NotImplementedError
    def get_width(self):
        raise NotImplementedError
    def get_height(self):
        raise NotImplementedError
    def draw_rect(self, x0, y0, x1, y1, color):
        raise NotImplementedError
    def draw_polygon(self, color, *points):
        raise NotImplementedError
    def clear(self):
        raise NotImplementedError

class TimeLinePlot:
    def __init__(
            self,
            data=None,
            background_color='black',
            time_line_color='green',
            entry_frame_color='green',
            entry_text_color='white',
            entry_card_background=None,
            title_font='Arial 9',
            message_font='Arial 7',
            time_line_font='Arial 7',
            scrollable=True
    ):
        super().__init__()
        self.entry_card_background = entry_card_background if entry_card_background else background_color
        self.time_line_font = time_line_font
        self.message_font = message_font
        self.title_font = title_font
        self.scrollable = scrollable
        self.entry_text_color = entry_text_color
        self.entry_frame_color = entry_frame_color
        self.time_line_color = time_line_color
        self.background_color = background_color

        first_bad_entry = self.__find_bad_entry__(data)
        if first_bad_entry:
            raise Exception("BAD DATA FORMAT: \n" + str(first_bad_entry))

        # parse time strings into actual datetime, if they're not already datetimes
        for entry_index in range(len(data)):
            if isinstance(data[entry_index]['time'], str):
                try:
                    data[entry_index]['time'] = datetime.datetime.fromisoformat(data[entry_index]['time'])
                except Exception:
                    raise Exception("COULD NOT PARSE TIME STRING AT:\n"+str(data[entry_index]))

        self.data = data

    def draw(self, context: AbstractDrawingContext, far_left_date : datetime.datetime =None, far_right_date : datetime.datetime =None):
        if not self.data:
            raise Exception("NO DATA SET, CANNOT DRAW GRAPH (did you forget to supply the data?)")
        if not far_left_date:
            far_left_date = min(self.data, key=lambda x: x['time'])['time']
            # day has to be set to one because of leap year
            far_left_date = far_left_date.replace(year=far_left_date.year-2, day=1)
        if not far_right_date:
            far_right_date = max(self.data, key=lambda x: x['time'])['time']
            # day has to be set to one because of leap year
            far_right_date = far_right_date.replace(year=far_right_date.year+2, day=1)

        context.draw_rect(0, 0, context.get_width(), context.get_height(), self.background_color)

        context.set_line_width(2)

        y_pos = context.get_height()*0.8

        # draw time line line and endpoints
        context.draw_line(30, y_pos, context.get_width() - 90, y_pos, self.time_line_color)
        context.draw_ellipse(30 - 10, y_pos - 5, 5, 5, self.time_line_color)
        context.draw_ellipse(context.get_width() - 90, y_pos - 5, 5, 5, self.time_line_color)

        # time line params
        left_line_padding = 30
        right_line_padding = 100
        time_line_length = context.get_width() - (right_line_padding+left_line_padding)
        num_days = (far_right_date - far_left_date).days

        # entry params
        entry_width = 100
        entry_height = 55
        entry_padding = 6
        entry_frame_border_width = 2
        entry_frame_corner_size = 10

        # sort by time to make sure they get drawn in the intuitive order as far as y_pos goes
        time_sorted_entries = reversed(sorted(self.data, key=lambda x: x['time']))
        occupied_x = []

        context.set_line_width(entry_frame_border_width)

        for entry in time_sorted_entries:
            if entry['time'] < far_left_date or far_right_date < entry['time']:
                continue

            x_pos = 30 + time_line_length * (entry['time'] - far_left_date).days / num_days
            context.draw_ellipse(x_pos - 2 - 4, y_pos-5, 5, 5, self.background_color)
            context.draw_ellipse(x_pos - 4, y_pos-3, 3, 3, self.entry_frame_color)

            occupied_x += [x_pos]
            overlaps = self.num_overlaps(occupied_x.copy(), x_pos, entry_width)

            card_y_pos = y_pos - entry_height/2 - (entry_height*(1+overlaps) + entry_padding*overlaps)

            context.draw_polygon(
                self.entry_card_background,
                (x_pos, card_y_pos),
                (x_pos + entry_width - entry_frame_corner_size, card_y_pos),
                (x_pos + entry_width, card_y_pos + entry_frame_corner_size),
                (x_pos + entry_width, card_y_pos + entry_height),
                (x_pos, card_y_pos + entry_height)
            )
            context.draw_line(x_pos, y_pos, x_pos, card_y_pos, self.entry_frame_color)

            context.draw_line(
                x_pos, card_y_pos,
                x_pos+entry_width - entry_frame_corner_size,
                card_y_pos,
                self.entry_frame_color
            )
            context.draw_line(
                x_pos+entry_width - entry_frame_corner_size,
                card_y_pos,
                x_pos+entry_width,
                card_y_pos+entry_frame_corner_size,
                self.entry_frame_color
            )
            context.draw_line(
                x_pos+entry_width,
                card_y_pos+entry_frame_corner_size,
                x_pos+entry_width,
                card_y_pos+entry_height,
                self.entry_frame_color
            )
            context.draw_line(
                x_pos,
                card_y_pos+entry_height,
                x_pos+entry_width,
                card_y_pos+entry_height,
                self.entry_frame_color
            )
            context.draw_line(
                x_pos+entry_width - entry_frame_corner_size - entry_frame_border_width*2,
                card_y_pos + entry_frame_border_width*2,
                x_pos+entry_width - entry_frame_border_width*2,
                card_y_pos+entry_frame_corner_size + entry_frame_border_width*2,
                self.entry_frame_color
            )
            context.draw_line(
                x_pos + entry_frame_border_width*4,
                card_y_pos + 20,
                x_pos +entry_width - entry_frame_corner_size - entry_frame_border_width*3,
                card_y_pos + 20,
                self.entry_frame_color
            )

            context.draw_text(
                x_pos + entry_frame_border_width*4 + (entry_width - entry_frame_border_width*4 - entry_frame_corner_size - entry_frame_border_width*3)/2,
                card_y_pos + 20,
                entry['title'], color=self.entry_text_color, font=self.title_font, anchor='s'
            )
            context.draw_text(x_pos+entry_frame_border_width*3, card_y_pos + 24, entry['message'], color=self.entry_text_color, font=self.message_font, anchor='nw')

            context.draw_text(x_pos+entry_frame_border_width*2-4, y_pos+10, entry['time'].strftime('%D'), rotation=45, color=self.entry_text_color, font=self.time_line_font, anchor='ne')

        return context

    @staticmethod
    def num_overlaps(occupied_x_copy, new_x_pos, entry_width):
        occupied_x_copy.remove(new_x_pos)
        for x in occupied_x_copy:
            if x <= new_x_pos+entry_width:
                return 1 + TimeLinePlot.num_overlaps(occupied_x_copy, x, entry_width)
        return 0

    @staticmethod
    def __find_bad_entry__(data):
        for entry in data:
            try:
                if 'time' not in entry or 'message' not in entry or 'title' not in entry:
                    datetime.datetime.fromisoformat(entry['time'])
                    raise
            except:
                return entry
        return None
