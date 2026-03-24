# PDF Stitcher (Visual Seamless)

基于视觉识别的 PDF 表格垂直无缝拼接工具。专门解决由于设计问题导致的表格被拆分为两页、中间有白边空隙的问题。

## 功能特性
- **视觉识别拼接**：自动剥离 PDF 白边，实现表格内容的物理级接触。
- **边缘留白**：自动在拼接后的页面四周添加留白，提升阅读舒适度。
- **高清输出**：默认 300 DPI 采样。
- **批量处理**：支持超大 PDF 文件。

## 使用方法 (Python)
1. 安装依赖: `pip install -r requirements.txt`
2. 安装系统依赖: `sudo apt install poppler-utils qpdf` (Linux) 或安装 Poppler (Windows)
3. 运行: `python pdf_stitcher.py input.pdf output.pdf`

## 封装为 Windows .exe
1. 在 Windows 下运行 `pip install pyinstaller pillow`
2. 执行: `pyinstaller --onefile pdf_stitcher.py`
