import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

# variabel global
img_asli = None
img_proses = None
img_tk = None

# fungsi menampilkan gambar ke canvas
def tampilkan_gambar(img):
    global img_tk

    canvas.update()
    cw = canvas.winfo_width()
    ch = canvas.winfo_height()

    h, w = img.shape[:2]
    scale = min(cw / w, ch / h)

    nw = int(w * scale)
    nh = int(h * scale)

    img_resize = cv2.resize(img, (nw, nh))
    img_rgb = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)

    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)

    canvas.delete("all")
    canvas.create_image(cw // 2, ch // 2, image=img_tk, anchor="center")

# fungsi update informasi
def update_info(operasi):
    if img_proses is None:
        return

    h, w = img_proses.shape[:2]

    info_text.set(
        f"Nama File  : {nama_file}\n"
        f"Ukuran     : {w} x {h}\n"
        f"Mode Warna : {mode_warna}\n"
        f"Operasi    : {operasi}\n"
        f"Keterangan : {keterangan}"
    )

# fungsi upload gambar
def upload_gambar():
    global img_asli, img_proses, nama_file, mode_warna, keterangan

    path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
    )

    if path:
        img_asli = cv2.imread(path)
        img_proses = img_asli.copy()

        nama_file = path.split("/")[-1]
        mode_warna = "RGB"
        keterangan = "Gambar asli dimuat"

        tampilkan_gambar(img_proses)
        update_info("Belum ada")

# fungsi grayscale
def grayscale():
    global img_proses, mode_warna, keterangan

    if img_asli is None:
        return

    img_proses = cv2.cvtColor(img_asli, cv2.COLOR_BGR2GRAY)
    img_proses = cv2.cvtColor(img_proses, cv2.COLOR_GRAY2BGR)

    mode_warna = "Grayscale"
    keterangan = "Konversi RGB ke Grayscale"

    tampilkan_gambar(img_proses)
    update_info("Grayscale")

# fungsi smoothing
def smoothing():
    global img_proses, mode_warna, keterangan

    if img_asli is None:
        return

    kernel = np.ones((5, 5), np.float32) / 25
    img_proses = cv2.filter2D(img_asli, -1, kernel)

    mode_warna = "RGB"
    keterangan = "Low-pass filter untuk mengurangi noise"

    tampilkan_gambar(img_proses)
    update_info("Smoothing")

# fungsi sharpening
def sharpening():
    global img_proses, mode_warna, keterangan

    if img_asli is None:
        return

    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    img_proses = cv2.filter2D(img_asli, -1, kernel)

    mode_warna = "RGB"
    keterangan = "High-pass filter untuk menajamkan citra"

    tampilkan_gambar(img_proses)
    update_info("Sharpening")

# fungsi emboss
def emboss():
    global img_proses, mode_warna, keterangan

    if img_asli is None:
        return

    kernel = np.array([
        [-2, -1, 0],
        [-1, 1, 1],
        [0, 1, 2]
    ])

    img_proses = cv2.filter2D(img_asli, -1, kernel)

    mode_warna = "RGB"
    keterangan = "Emboss untuk efek timbul pada citra"

    tampilkan_gambar(img_proses)
    update_info("Emboss")

# window utama
root = tk.Tk()
root.title("Aplikasi Pengolahan Citra Digital")
root.geometry("1000x600")

# frame kiri
frame_kiri = tk.Frame(root, width=700, bg="white")
frame_kiri.pack(side="left", fill="both", expand=True)

canvas = tk.Canvas(frame_kiri, bg="gray")
canvas.pack(fill="both", expand=True, padx=10, pady=10)

# frame kanan
frame_kanan = tk.Frame(root, width=300)
frame_kanan.pack(side="right", fill="y")

tk.Button(frame_kanan, text="Upload Gambar", command=upload_gambar, height=2).pack(fill="x", padx=10, pady=5)
tk.Button(frame_kanan, text="Grayscale", command=grayscale).pack(fill="x", padx=10, pady=5)
tk.Button(frame_kanan, text="Smoothing", command=smoothing).pack(fill="x", padx=10, pady=5)
tk.Button(frame_kanan, text="Sharpening", command=sharpening).pack(fill="x", padx=10, pady=5)
tk.Button(frame_kanan, text="Emboss", command=emboss).pack(fill="x", padx=10, pady=5)

# panel informasi
info_text = tk.StringVar()
info_label = tk.Label(
    frame_kanan,
    textvariable=info_text,
    justify="left",
    anchor="nw",
    bg="#f0f0f0",
    padx=10,
    pady=10
)
info_label.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()
