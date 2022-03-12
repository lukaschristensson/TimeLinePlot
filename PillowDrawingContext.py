from PIL import Image, ImageDraw, ImageFont
from TimeLinePlot import AbstractDrawingContext, TimeLinePlot


class PillowDrawingContext(AbstractDrawingContext):

    def save(self):
        self.image.save('plot.png')
    def draw_text(self, x, y, text, font, color, rotation=0, anchor=''):
        if isinstance(font, str):
            # 1.5 size seems to match up with tkinter afaict
            font = ImageFont.truetype(font.split(' ')[0]+'.ttf', int(int(font.split(' ')[1])*1.5))

        text_size = font.getsize(text)

        if '\n' in text:
            lines = text.split('\n')
            for line in lines:
                self.draw_text(x, y + lines.index(line)*text_size[1], line, font, color, rotation, anchor)
            return


        # draw the text on a temporary image, rotate that image and paste it on the main image
        text_image = Image.new(mode='RGBA', size=text_size)
        ImageDraw.Draw(text_image).text((0, 0), text, font=font, fill=color)
        text_image=text_image.rotate(rotation, expand=True)

        image_size = text_image.size

        x -= image_size[0]/2
        y -= image_size[1]/2
        if 'n' in anchor:
            y += image_size[1]/2
        elif 's' in anchor:
            y -= image_size[1]/2
        if 'w' in anchor:
            x += image_size[0]/2
        elif 'e' in anchor:
            x -= image_size[0]/2
        self.image.paste(text_image, (int(x), int(y)), text_image)

    def get_width(self):
        return self.size[0]

    def get_height(self):
        return self.size[1]

    def draw_rect(self, x0, y0, x1, y1, color):
        self.draw.rectangle([x0, y0, x1, y1], fill=color)

    def __init__(self, image=None, size=(3000, 500)):
        self.image = image if image else Image.new(mode='RGBA', size=size)
        self.draw = ImageDraw.Draw(self.image)
        self.size = size
        self.line_width=0

    def set_line_width(self, w):
        self.line_width = w

    def draw_line(self, x0, y0, x1, y1, color):
        self.draw.line([x0, y0, x1, y1], width=self.line_width, fill=color)

    def draw_ellipse(self, x, y, r1, r2, color):
        self.draw.ellipse([x, y, x+r1*2, y+r2*2], fill=color)

    def set_pixel(self, x, y, color):
        self.draw.rectangle([x, y, x+1, y+1], fill=color)

    def clear(self):
        pass

if __name__ == '__main__':
    test_data = [
        {'time': '1997-08-02T01:12:00', 'message': 'Switched versions:\nv0.0.1 to v1.0.1', 'title': 'Company A'},
        {'time': '1928-08-14T14:11:00', 'message': 'Switched versions:\nv0.0.1 to v2.0.1', 'title': 'Company B'},
        {'time': '1937-08-14T14:11:00', 'message': 'Switched versions:\nv0.0.1 to v2.0.1', 'title': 'Company B'},
        {'time': '1937-12-30T05:15:00', 'message': 'Switched versions:\nv1.0.1 to v3.0.1', 'title': 'Company C'},
        {'time': '1941-12-30T05:15:00', 'message': 'Switched versions:\nv1.0.1 to v3.0.1', 'title': 'Company C'},
        {'time': '2001-02-28T10:01:00', 'message': 'Switched versions:\nv3.0.1 to v4.0.1', 'title': 'Company D'},
        {'time': '2001-02-28T10:01:00', 'message': 'Switched versions:\nv3.0.1 to v4.0.1', 'title': 'Company D'},
        {'time': '2011-05-10T20:58:00', 'message': 'Switched versions:\nv2.0.1 to v5.0.1', 'title': 'Company E'},
    ]
    TimeLinePlot(data=test_data.copy()).draw(PillowDrawingContext()).save()
