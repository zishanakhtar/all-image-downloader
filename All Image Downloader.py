import time
import customtkinter as ctk
import requests
import pathlib
import os
from bs4 import BeautifulSoup
from PIL import Image
from datetime import datetime
import sys
import webbrowser
from CTkMessagebox import CTkMessagebox
import threading
import io
import random

"""
customtkinter, requests, bs4, PIL, CTkMessagebox
"""

downloads_folder_path = str(pathlib.Path.home()/"Downloads/Website Images/")


def create_download_folder(time):
    # Create a folder in Downloads folder names YouTubeDownloads if it does not exist.
    pathlib.Path(pathlib.Path.home() / f"Downloads/Website Images/{time}").mkdir(parents=True, exist_ok=True)


extensions = ("jpg", "jpeg", "png", "gif", "svg")
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

pics_downloaded = 0
def download():
    current_time = str(datetime.now()).replace(":", "-").replace(".", "-")
    create_download_folder(current_time)
    download_progress.configure(text="Starting download...")
    link = var_url.get()
    print("Link:", link)
    try:
        r = requests.get(url=link, headers=headers)
    except Exception as e:
        CTkMessagebox(title="Warning", message="Unable to process the link.", icon="warning")
        download_progress.configure(text="")
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    with open("index.html", encoding="utf8") as f:
        html_content = f.read()
        soup = BeautifulSoup(html_content, "html.parser")
        images = soup.select('img')
        print("Images:", images)
        print("Number of img:", len(images))
        for img_index, img in enumerate(images):
            img_link = requests.compat.urljoin(link, img.get('src'))
            if img_link is not None:
                print("Image link:", img_link)
                link_split = img_link.split('.')
                img_extension = str(link_split[len(link_split)-1])
                print(img_extension)
                # for extension in extensions:

                # if img_extension.startswith(extensions):
                try:
                    if str(link).startswith("https://"):
                        # Random interval between requests
                        req_interval = random.choice(list(range(1, 16)))
                        print("Request interval:", req_interval, "Sec")
                        time.sleep(req_interval)

                    get_img = requests.get(img_link, stream=True, headers=headers)

                    i = Image.open(io.BytesIO(get_img.content)).convert("RGB")
                    if img_extension not in extensions:
                        img_extension = "png"
                    with open(f"{downloads_folder_path}/{current_time}/{img_index}.{img_extension}", "wb") as fp:
                        # fp.write(r.content)
                        i.save(fp)
                        global pics_downloaded
                        pics_downloaded += 1
                        if pics_downloaded == 1:
                            download_progress.configure(text=f"1/{len(images)} photo downloaded")
                        else:
                            download_progress.configure(text=f"{pics_downloaded}/{len(images)} photos downloaded")
                except Exception as e:
                    print(e)
                    # if str(e).startswith("No connection adapters were found"):
                    #     download_progress.configure(text="Resetting connection...")
                    #     time.sleep(20)
    CTkMessagebox(title="Info", message=f"Download complete.\n{pics_downloaded} images downloaded.", icon="check")
    download_progress.configure(text="")
    pics_downloaded = 0
    images.clear()


def download_in_separate_thread():
    """Downloading task in parallel thread to prevent app from Not Responding"""
    threading.Thread(target=download).start()


def open_download_dir():
    os.startfile(downloads_folder_path)


def open_buymeacoffee():
    webbrowser.open("https://www.buymeacoffee.com/zishanakhtar")


def change_theme():
    if ctk.get_appearance_mode() == "Light":
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("light")


def close_app():
    sys.exit()


window = ctk.CTk()
current_theme = ctk.set_appearance_mode("dark")
window.title("All Image Downloader")
window.wm_iconbitmap("All Image Downloader Icon.ico")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
app_width = 550
app_height = 500
# print(screen_width, screen_height)
x = int((screen_width-app_width)/2)
y = int((screen_height-app_height)/3)
# print(x, y)
window.geometry(f"{app_width}x{app_height}+{x}+{y}")
window.resizable(False, False)

light_img = Image.open("All Image Downloader 3.png")
dark_img = Image.open("All Image Downloader.png")
img_main = ctk.CTkImage(light_image=light_img, dark_image=dark_img, size=(450, 150))
lbl_img_main = ctk.CTkLabel(window, text="", image=img_main)
lbl_img_main.pack(pady=(20, 0))

lbl = ctk.CTkLabel(window, text="Enter Website Link Below", font=("", 18, "bold"))
lbl.pack(pady=(10, 0))

lbl2 = ctk.CTkLabel(window, text="(Only publicly available links)", font=("", 12))
lbl2.pack(pady=(0, 0))

var_url = ctk.StringVar()
input_url = ctk.CTkEntry(window, textvariable=var_url, width=350)
input_url.pack(pady=(0, 0))

input_url.insert("0", "- - - Follow on Instagram: @akhtarreviews - - -")

download_progress = ctk.CTkLabel(window, text="", font=("", 18))
download_progress.pack(pady=(10, 0))

f1 = ctk.CTkFrame(window, fg_color="transparent")
f1.pack()

btn_download = ctk.CTkButton(f1, text="Download Images", command=download_in_separate_thread)
btn_download.pack(side="left", pady=15)

btn_open_download_folder = ctk.CTkButton(f1, text="Download Location", command=open_download_dir)
btn_open_download_folder.pack(side="left", padx=(15, 0), pady=15)

f2 = ctk.CTkFrame(window, fg_color="transparent")
f2.pack()

btn_support = ctk.CTkButton(f2, text="Support", command=open_buymeacoffee)
btn_support.pack(side="left", pady=(5, 0))

btn_theme = ctk.CTkButton(f2, text="Change Theme", command=change_theme)
btn_theme.pack(side="left", padx=(15, 0), pady=(5, 0))

btn_exit = ctk.CTkButton(window, text="Exit", command=close_app, hover_color="red")
btn_exit.pack(pady=(20, 0))

window.mainloop()
