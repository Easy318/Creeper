# 配置
from pathlib import Path

# 项目文件夹
SRC_DIR = Path(__file__).parent.parent

# Download文件夹
DOWNLOAD_DIR = SRC_DIR / "download"


if __name__ == "__main__":
    print(SRC_DIR)
