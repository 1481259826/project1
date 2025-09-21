from my_project.exif_reader import get_exif_date

def test_get_exif_date_with_file(tmp_path):
    # 创建一个假文件模拟测试
    f = tmp_path / "test.jpg"
    f.write_text("fake image")
    date = get_exif_date(str(f))
    assert isinstance(date, str)
