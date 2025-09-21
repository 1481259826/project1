import os
import argparse
from datetime import datetime
from .exif_reader import get_exif_date, add_watermark

def main():
    parser = argparse.ArgumentParser(description="批量为图片添加拍摄日期水印")
    parser.add_argument("input_path", help="图片所在文件夹路径")
    parser.add_argument("--font-size", type=int, default=30, help="字体大小，默认30")
    parser.add_argument("--font-color", type=str, default="white", help="字体颜色，例如 white 或 #FF0000")
    parser.add_argument("--position", type=str, default="right_bottom",
                        choices=["left_top", "center", "right_bottom"],
                        help="水印位置，默认 right_bottom")

    args = parser.parse_args()

    if not os.path.isdir(args.input_path):
        print("❌ 路径不存在或不是文件夹")
        return

    # 输出目录加时间戳避免覆盖
    output_dir = os.path.join(
        args.input_path,
        f"{os.path.basename(args.input_path)}_watermark_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(args.input_path):
        file_path = os.path.join(args.input_path, file)
        if not os.path.isfile(file_path):
            continue
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            date_str = get_exif_date(file_path)
            output_path = os.path.join(output_dir, file)
            add_watermark(file_path, date_str, args.font_size, args.font_color, args.position, output_path)
            print(f"✅ 已处理：{file}，水印：{date_str}")

if __name__ == "__main__":
    main()
