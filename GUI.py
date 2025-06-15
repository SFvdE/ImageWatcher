import ttkbootstrap as ttk
import subprocess

window = ttk.Window()

window.title("ImageWatcher")
window.configure(background="white")
window.minsize(200, 200)
window.maxsize(500, 500)
window.geometry("300x300+50+50")

label = ttk.Label(window)
label.pack(pady=30) 
label.config(font=("Arial", 20, "bold"))

def ImageWatcher():
    subprocess.Popen(["python", "ImageWatcher.py"])

btn = ttk.Button(window, text="run", command=ImageWatcher, bootstyle="outline")
btn.pack(pady=20)

window.mainloop()