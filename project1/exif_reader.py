import os
import piexif
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def get_exif_date(image_path):
    """读取图片的EXIF拍摄日期，优先顺序：DateTimeOriginal > DateTimeDigitized > DateTime"""
    try:
        exif_dict = piexif.load(image_path)
        date_bytes = (
            exif_dict["Exif"].get(piexif.ExifIFD.DateTimeOriginal)
            or exif_dict["Exif"].get(piexif.ExifIFD.DateTimeDigitized)
            or exif_dict["0th"].get(piexif.ImageIFD.DateTime)
        )
        if date_bytes:
            date = datetime.strptime(date_bytes.decode("utf-8"), "%Y:%m:%d %H:%M:%S")
            return date.strftime("%Y-%m-%d")
    except Exception:
        pass
    # 如果没有EXIF时间，就用文件修改时间
    file_stat = os.stat(image_path)
    date = datetime.fromtimestamp(file_stat.st_mtime)
    return date.strftime("%Y-%m-%d")

def get_text_size(draw, text, font):
    """兼容不同 Pillow 版本，计算文字宽高"""
    if hasattr(draw, "textbbox"):
        bbox = draw.textbbox((0, 0), text, font=font)
        width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    else:
        width, height = draw.textsize(text, font=font)
    return width, height

def add_watermark(image_path, text, font_size, font_color, position, output_path):
    """在图片上添加文字水印"""
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # 字体兼容 Windows / Linux / 默认
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", font_size)
        except:
            font = ImageFont.load_default()

    text_w, text_h = get_text_size(draw, text, font)
    img_w, img_h = image.size

    if position == "left_top":
        x, y = 10, 10
    elif position == "center":
        x, y = (img_w - text_w) / 2, (img_h - text_h) / 2
    elif position == "right_bottom":
        x, y = img_w - text_w - 10, img_h - text_h - 10
    else:
        x, y = 10, 10  # 默认左上角

    draw.text((x, y), text, font=font, fill=font_color)
    # 保存时保留原图格式和 EXIF 信息
    image.save(output_path, format=image.format, exif=image.info.get("exif"))
