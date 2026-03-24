@echo off
echo [Step 1] Installing Python libraries...
pip install PyMuPDF Pillow pyinstaller
echo [Step 2] Packaging PDFStitcher.exe...
pyinstaller --onefile --windowed --name PDFStitcherV2 pdf_stitcher_gui.py
echo.
echo Success! Your EXE is ready in the "dist" folder.
echo You can copy this EXE to ANY Windows PC and it will work.
pause
