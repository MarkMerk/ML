from keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab, Image
import numpy as np
import matplotlib.pyplot as plt

model = load_model('bestmodel.h5')

def predict_digit(img):
    # изменение рзмера изобржений на 28x28
    img = img.resize((28,28))
    # конвертируем rgb в grayscale
    img = img.convert('L')
    img.save('temp.jpeg')
    img = np.array(img)
    # изменение размерности для поддержки модели ввода и нормализации
    img = img.reshape(1,28,28,1)
    img = -1*(img/255.0)+1
    # предстказание цифры
    res = model.predict([img])[0]
    plt.imshow(img[0])
    return np.argmax(res), max(res)
    
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.x = self.y = 0
        self.start_pos = 0
        
        # Создание элементов
        self.canvas = tk.Canvas(self, width=300, height=300, bg = "white", cursor="cross")
        self.label = tk.Label(self, text="Думаю..", font=("Helvetica", 48))
        self.classify_btn = tk.Button(self, text = "Распознать", command = self.classify_handwriting) 
        self.button_clear = tk.Button(self, text = "Очистить", command = self.clear_all)
        
        # Сетка окна
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=0, column=1,pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)
        
        self.canvas.bind('<Button-1>', self.start_pos)
        self.canvas.bind('<B1-Motion>', self.draw_lines)
        self.canvas.bind('<ButtonRelease-1>', self.save)
        # window_width = 300
        # window_height = 200

        # # get the screen dimension
        # screen_width = self.winfo_screenwidth()
        # screen_height = self.winfo_screenheight()

        # # find the center point
        # center_x = int(screen_width/2 - window_width / 2)
        # center_y = int(screen_height/2 - window_height / 2)

        # # set the position of the window to the center of the screen
        # self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
    def clear_all(self):
        self.canvas.delete("all")
        
    def classify_handwriting(self):
        # HND = self.canvas.winfo_id() 
        # rect = win32gui.GetWindowRect(HND) # получаем координату холста
        # im = ImageGrab.grab(rect)
        # im = Image.open('one.png')
        # newsize = (2483, 2483)
        # im1 = im.resize(newsize)
        digit, acc = predict_digit(self.im)
        self.label.configure(text= str(digit)+', '+ str(int(acc*100))+'%')

    def show_img(self, event):
        self.canvas.to_file('my.img')
        
    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r=8
        self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill='black')

    def save(self,event):
        self.update()
        print(self.winfo_x(),self.winfo_y(),self.winfo_rootx(),self.winfo_rooty())
        x=self.winfo_rootx()+self.winfo_x()+self.winfo_x()+20
        y=self.winfo_rooty()+self.winfo_y()+self.winfo_y()+40
        x1=x+self.winfo_width()+300
        y1=y+self.winfo_height()+630
        self.im = ImageGrab.grab().crop((x,y,x1,y1))
        self.im.save('st.jpeg')

app = App()

mainloop()