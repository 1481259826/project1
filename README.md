# 图片 EXIF 水印工具

本项目可以批量读取图片 EXIF 信息中的拍摄时间信息，选取年月日，并将其作为水印添加到图片上。

## 使用方法

安装依赖：
```bash
pip install -r requirements.txt
```
使用示例：
```bash
python -m project1.cli ./images --font-size 30 --font-color "#FF0000" --position right_bottom
```

