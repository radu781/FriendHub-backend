import os
import random
import uuid
from dataclasses import dataclass, field

import qrcode
from PIL import Image
from PIL.ImageColor import colormap


@dataclass
class QRCodeBuilder:
    data: str
    logo: Image.Image = field(init=False)
    qr_img: Image.Image = field(init=False)
    LOGO_WIDTH = 50

    def __post_init__(self) -> None:
        self.logo = Image.open("friendhub/static/logo.png")

    def make(self, fill_color: str | None = None, back_color: str | None = None) -> None:
        if not fill_color or not back_color:
            fill_color, back_color = self.__random_color()

        w_percent = QRCodeBuilder.LOGO_WIDTH / float(self.logo.size[0])
        h_size = int((float(self.logo.size[1]) * float(w_percent)))
        logo = self.logo.resize((QRCodeBuilder.LOGO_WIDTH, h_size), Image.ANTIALIAS)

        qr_code = qrcode.QRCode(error_correction=qrcode.ERROR_CORRECT_H)
        qr_code.add_data(self.data)
        qr_code.make()

        self.qr_img = qr_code.make_image(fill_color=fill_color, back_color=back_color).convert(
            "RGB"
        )

        pos = ((self.qr_img.size[0] - logo.size[0]) // 2, (self.qr_img.size[1] - logo.size[1]) // 2)
        self.qr_img.paste(logo, pos)

    def save(self, author_id: uuid.UUID) -> None:
        dir_name = f"friendhub/static/uploads/{author_id}"
        try:
            os.mkdir(dir_name)
        except FileExistsError:
            pass
        self.qr_img.save(f"{dir_name}/qr.png")

    def __random_color(self) -> tuple[str, str]:
        fill_color = random.choice(list(colormap.keys()))
        back_color = fill_color
        while back_color == fill_color:
            back_color = random.choice(list(colormap.keys()))
        return (fill_color, back_color)
