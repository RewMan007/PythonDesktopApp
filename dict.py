import tkinter
import requests
from tkinter import *
from textblob import TextBlob
from googletrans import Translator
from PIL import ImageTk, Image
from io import BytesIO
import random


root = Tk()
root.title("Spelling Checker")
root.geometry("700x500")
root.config(background="#dae6f6")
thai_word = ""

def translate_word(word):
    translator = Translator()
    translation = translator.translate(word, dest='th')
    if translation is not None:
        return translation.text
    else:
        return "ไม่สามารถแปลคำได้"

def search_image(query):
    print("----------------------------------------------------------------------------")
    # ทำการค้นหาภาพจาก Google Images API
    # ใส่โค้ด API ที่ได้รับจากการลงทะเบียน
    api_key = "AIzaSyDr0aCyAWOx85yKxzV3OkGPNW2uB1WbS5Y"
    search_engine_id = "076d2cd5822d74df8"
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}&searchType=image"
    response = requests.get(url)
    data = response.json()

    # หา URL ของรูปภาพแรกที่ค้นพบ
    if "items" in data and len(data["items"]) > 0:
        image_url = data["items"][0]["link"]
        return image_url

    return None

cs = Label(root, text="ควรแก้เป็น :", font=("Pridi", 20), bg="#dae6f6", fg="#364971")
cs2 = Label(root, text="ความหมาย :", font=("Pridi", 20), bg="#dae6f6", fg="#364971")

def check_spelling():
    word = enter_text.get()
    a = TextBlob(word)
    right = str(a.correct())
    trans.config(text=translate_word(right))

    cs.config(text="ควรแก้เป็น :")  # ใช้ .config() เพื่อเปลี่ยนข้อความใน Label
    cs.place(x=30, y=260)  # ย้าย .place() เข้ามาในฟังก์ชัน check_spelling()
    cs2.place(x=30, y=360)  # ย้าย .place() เข้ามาในฟังก์ชัน check_spelling()

    if word != right:
        cs.config(text="ควรแก้เป็น :")
        spell.config(text=right)
    else:
        cs.config(text="ยินดีด้วย !")
        spell.config(text="ข้อความนี้สะกดถูกต้องแล้ว !")

    image_url = search_image(right)
    if image_url:
        response = requests.get(image_url)
        image_data = response.content

        # สร้างรูปภาพใหม่โดยปรับขนาดเป็น 210x210
        image = Image.open(BytesIO(image_data))
        image = image.resize((210, 210))

        image = ImageTk.PhotoImage(image)
        image_label.configure(image=image)  # ใช้ .configure() แทนการใช้ .config()
        image_label.image = image
        root.update()
        
    else:
        image_label.configure(image=None)  # ใช้ .configure() แทนการใช้ .config()
    image_label.place(x=root.winfo_width() - 240, y=250)
        

heading = Label(root, text="โปรแกรมตรวจคำผิด", font=("Pridi", 30, "bold"), bg="#dae6f6", fg="#364971")
heading.pack(pady=(20, 0))

enter_text = Entry(root, justify="center", width=30, font=("Pridi", 25), bg="white", border=2)
enter_text.pack(pady=10)
enter_text.focus()

button = Button(root, text="      คลิกเพื่อตรวจสอบการสะกด      ", font=("Pridi", 10), fg="white", bg="blue", command=check_spelling)
button.pack()

spell = Label(root, font=("Pridi", 20), bg="#dae6f6", fg="#364971")
spell.place(x=30, y=300)

trans = Label(root, font=("Pridi", 20), bg="#dae6f6", fg="#364971")
trans.place(x=30, y=400)

image_label = Label(root)
image_label.place(x=400, y=260)

root.mainloop()


# Custom Search JSON API มีไว้สําหรับคําค้นหา 100 รายการต่อวันฟรี หากต้องการข้อมูลเพิ่มเติม คุณสามารถลงชื่อสมัครใช้การเรียกเก็บเงินในคอนโซล API คําขอเพิ่มเติมมีค่าใช้จ่าย $5 ต่อการค้นหา 1,000 รายการ ในการค้นหาสูงสุด 10,000 รายการต่อวัน
# หากต้องการมากกว่า 10,000 การค้นหาต่อวันและ Programmable Search Engine ค้นหาเว็บไซต์ไม่เกิน 10 เว็บไซต์ คุณอาจสนใจ Custom Search Site Restricted JSON API ซึ่งไม่จํากัดการค้นหารายวัน