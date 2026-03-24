import os, sys, tkinter as tk
from tkinter import filedialog, messagebox, ttk
import fitz
from PIL import Image, ImageChops
import threading

def trim_white(im):
    bg = Image.new(im.mode, im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    return im.crop(bbox) if bbox else im

class PDFStitcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF 视觉无缝拼接工具 v2.0")
        self.root.geometry("500x320")
        tk.Label(root, text="PDF 垂直无缝拼接工具 (自适应留白版)", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Button(root, text="第一步：选择待处理 PDF", command=self.select_file).pack(pady=5)
        self.lbl_file = tk.Label(root, text="未选择文件", fg="gray")
        self.lbl_file.pack()
        tk.Button(root, text="第二步：选择输出目录", command=self.select_output).pack(pady=5)
        self.lbl_out = tk.Label(root, text="未选择输出目录", fg="gray")
        self.lbl_out.pack()
        self.btn_run = tk.Button(root, text="开始执行合并", state="disabled", bg="green", fg="white", command=self.start_process)
        self.btn_run.pack(pady=15)
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=5)
        self.input_path = ""; self.output_dir = ""

    def select_file(self):
        self.input_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.input_path: self.lbl_file.config(text=os.path.basename(self.input_path), fg="black"); self.check_ready()

    def select_output(self):
        self.output_dir = filedialog.askdirectory()
        if self.output_dir: self.lbl_out.config(text=self.output_dir, fg="black"); self.check_ready()

    def check_ready(self):
        if self.input_path and self.output_dir: self.btn_run.config(state="normal")

    def start_process(self):
        self.btn_run.config(state="disabled")
        threading.Thread(target=self.process_logic, daemon=True).start()

    def process_logic(self):
        try:
            doc = fitz.open(self.input_path); total = len(doc); margin = 60; stitched = []
            self.progress["maximum"] = total // 2
            for i in range(0, total, 2):
                if i+1 >= total: break
                pix1 = doc[i].get_pixmap(dpi=300); pix2 = doc[i+1].get_pixmap(dpi=300)
                im1 = trim_white(Image.frombytes("RGB", [pix1.width, pix1.height], pix1.samples))
                im2 = trim_white(Image.open(Image.frombytes("RGB", [pix2.width, pix2.height], pix2.samples).save("t.png") or "t.png").convert("RGB")) if not i==0 else trim_white(Image.frombytes("RGB", [pix2.width, pix2.height], pix2.samples))
                im2 = trim_white(Image.frombytes("RGB", [pix2.width, pix2.height], pix2.samples))
                cw, ch = max(im1.width, im2.width), im1.height + im2.height
                canvas = Image.new("RGB", (cw + 2*margin, ch + 2*margin), (255, 255, 255))
                canvas.paste(im1, (margin + (cw - im1.width)//2, margin))
                canvas.paste(im2, (margin + (cw - im2.width)//2, margin + im1.height))
                stitched.append(canvas); self.progress["value"] = (i // 2) + 1; self.root.update_idletasks()
            if stitched:
                out = os.path.join(self.output_dir, "Stitched_" + os.path.basename(self.input_path))
                stitched[0].save(out, save_all=True, append_images=stitched[1:], resolution=300.0)
                messagebox.showinfo("成功", f"合并完成！\n保存至: {out}")
        except Exception as e: messagebox.showerror("错误", f"发生错误: {e}")
        finally: self.btn_run.config(state="normal"); self.progress["value"] = 0

if __name__ == "__main__":
    root = tk.Tk(); app = PDFStitcherApp(root); root.mainloop()
