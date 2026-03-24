import subprocess
import os
import glob
from PIL import Image, ImageChops
from pathlib import Path
import sys

def trim_white(im):
    bg = Image.new(im.mode, im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    return im.crop(bbox) if bbox else im

def process_file(input_pdf, output_name, margin_px=60):
    if not os.path.exists(input_pdf): return print(f"Error: {input_pdf}")
    try:
        info = subprocess.check_output(["pdfinfo", input_pdf], text=True)
        pages = int([line for line in info.split('\n') if "Pages:" in line][0].split()[1])
        print(f"Processing: {input_pdf}, {pages} pages")
        stitched_pages = []
        temp_dir = Path("temp_work")
        temp_dir.mkdir(exist_ok=True)
        for i in range(1, pages + 1, 2):
            if i + 1 > pages: break
            subprocess.run(["pdftocairo", "-png", "-r", "300", "-f", str(i), "-l", str(i+1), input_pdf, str(temp_dir / "p")], check=True)
            pngs = sorted(glob.glob(str(temp_dir / "p-*.png")))
            if len(pngs) < 2: continue
            im1 = trim_white(Image.open(pngs[0]).convert("RGB"))
            im2 = trim_white(Image.open(pngs[1]).convert("RGB"))
            cw, ch = max(im1.width, im2.width), im1.height + im2.height
            canvas = Image.new("RGB", (cw + 2*margin_px, ch + 2*margin_px), (255, 255, 255))
            canvas.paste(im1, (margin_px + (cw - im1.width)//2, margin_px))
            canvas.paste(im2, (margin_px + (cw - im2.width)//2, margin_px + im1.height))
            tmp = f"tmp_p_{i}.pdf"; canvas.save(tmp, "PDF", resolution=300.0); stitched_pages.append(tmp)
            for f in pngs: os.remove(f)
        if stitched_pages:
            subprocess.run(["qpdf", "--empty", "--pages"] + stitched_pages + ["--", output_name], check=True)
            for p in stitched_pages: os.remove(p)
        if temp_dir.exists(): temp_dir.rmdir()
        print("Done!")
    except Exception as e: print(f"Fail: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3: print("Usage: python3 pdf_stitcher.py <input> <output>")
    else: process_file(sys.argv[1], sys.argv[2])
