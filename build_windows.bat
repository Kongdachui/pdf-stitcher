@echo off
echo Installing dependencies...
pip install pillow pyinstaller
echo Building EXE...
pyinstaller --onefile --name PDFStitcher pdf_stitcher.py
echo.
echo Done! The executable is in the "dist" folder.
pause
