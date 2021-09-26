import tkinter as tk
import tkinter.font as tkFont
import cv2 as cv
from PIL import Image, ImageTk
import detect

class App:
    def __init__(self, root, cam=0):
        #setting title
        self.cam = cam
        self.root = root
        self.root.title("Pcb Drill Guider")
        self.root.background_color='#f0f0f0'
        self.detect = detect.Drill()
       
        #setting window size
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        print(self.screen_width, self.screen_height)
        self.root.geometry(f'{self.screen_width}x{self.screen_height}')
        self.root.resizable(width=False, height=False)
       
        # Getting camera ready
        self.video = cv.VideoCapture(self.cam)
        self.lmain = tk.Label(self.root)
        self.lmain.place(x=20,y=0,width=self.screen_width*0.75,height=self.screen_height)
        if self.video.isOpened():
            self.video_stream()
        else:
            print("Please Select a Valid Camera")

        exit_button=tk.Button(self.root)
        exit_button["bg"] = "red"
        ft = tkFont.Font(family='Times',size=12)
        exit_button["font"] = ft
        exit_button["fg"] = "#000000"
        exit_button["justify"] = "center"
        exit_button["text"] = "Exit"
        exit_button.place(x=self.screen_width-100,y=self.screen_height-120,width=80,height=40)
        exit_button["command"] = self.exit_b

    def video_stream(self):
        #getting latest frame and convert into image
        video = cv.resize(self.video.read()[1], (int(self.screen_width*0.75), int(self.screen_height*0.85)))      
        cv2image= cv.cvtColor(video,cv.COLOR_BGR2RGB)
        cam_image = self.detect.cam_detected(cv2image)
        img = Image.fromarray(cam_image)
        # Convert image to PhotoImage
        imgtk = ImageTk.PhotoImage(image = img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        # Repeat after an interval to capture continiously
        self.lmain.after(1, self.video_stream)

    def exit_b(self):
        # print("command")
        root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
