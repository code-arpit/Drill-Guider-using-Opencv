import tkinter as tk
from tkinter.constants import ANCHOR, CENTER, COMMAND, N, RIGHT, TOP, W, X, Y, YES
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
        self.detect = detect.Drill()
       
        #setting window size
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        # print(self.screen_width, self.screen_height)
        self.root.geometry(f'{self.screen_width}x{self.screen_height}')
        self.root.resizable(width=False, height=False)

        #menu function
        self.top_menu(self.root)
        controller_state(self.root, self.screen_height, self.screen_width)
        toolbox(self.root, self.screen_height, self.screen_width)
        jog_control(self.root, self.screen_height, self.screen_width)
        message = console(self.root, self.screen_height, self.screen_width)
        for i in range(20):
            message.console_message(i)

    def video_stream(self):
        #getting latest frame and convert into image
        video = cv.resize(self.video.read()[1], (int(self.screen_width*0.62), int(self.screen_height*0.6)))      
        cv2image= cv.cvtColor(video,cv.COLOR_BGR2RGB)
        cam_image = self.detect.cam_detected(cv2image)
        img = Image.fromarray(cam_image)
        # Convert image to PhotoImage
        imgtk = ImageTk.PhotoImage(image = img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        # Repeat after an interval to capture continiously
        self.lmain.after(1, self.video_stream)

    def top_menu(self, frame):
        main_menu = tk.Menu(frame)
        root.config(menu=main_menu)

        # File commands to menu
        filemenu = tk.Menu(main_menu)
        filemenu.add_command(label="New File")
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save")
        main_menu.add_cascade(label="File", menu=filemenu)
        main_menu.add_command(label='|')

        # Connect cnc Command in menu
        main_menu.add_command(label='Connect')
        main_menu.add_command(label=':')
        main_menu.add_command(label='CNC', command=self.cnc, foreground='Blue')
        # Connect camera command in menu
        main_menu.add_command(label=':')
        main_menu.add_command(label='Camera', command=self.connect, foreground='Blue')
        main_menu.add_command(label='|')

        # Connect cnc Command in menu
        portmenu = tk.Menu(main_menu)
        portmenu.add_command(label='Port1')
        main_menu.add_cascade(label="Port", menu=portmenu)
        main_menu.add_command(label='|')


        #Exit Command in menu
        main_menu.add_command(label='Quit', command=self.root.quit, foreground='red')
        main_menu.add_command(label='|')
    
    def connect(self):
        print("Connection Established")
        # Getting camera ready
        self.video = cv.VideoCapture(self.cam)
        self.lmain = tk.Label(self.root)
        self.lmain.place(x=self.screen_width*0.35+40,y=20,width=self.screen_width*0.62,height=self.screen_height*0.6)
        if self.video.isOpened():
            self.video_stream()
        else:
            print("Please Select a Valid Camera")
    
    def cnc(self):
        print("Connection Established")

class controller_state():
    def __init__(self, frame, height, width):
        box = tk.LabelFrame(frame, text='Controller State', labelanchor=N, pady=10, font=16)
        box.place(x=20, y=10, width=width*0.35, height=height*0.3)
        self.x_frame = tk.Frame(box)
        self.x_frame.pack(side=TOP, anchor=W, fill=X)

        tk.Label(self.x_frame, 
                text='    CNC    ',
                font='Arial 20 bold',
                background='red',
                foreground='Black'
        ).grid(row=0, column=1, padx=40)
        
        tk.Label(self.x_frame, 
                text='   Camera   ',
                font='Arial 20 bold',
                background='red',
                foreground='Black'
        ).grid(row=0, column=2, padx=10)

        check = tk.Label(self.x_frame, 
                    text='CHECK',
                    font='Verdana 30 bold'
        ).grid(row=0, column=0)
                
        x_axis = tk.Label(self.x_frame, 
                    text='X-Axis',
                    font=('Arial', 20)
        ).grid(row=2, column=0, pady=10)
        
        y_axis = tk.Label(self.x_frame, 
                    text='Y-Axis',
                    font=('Arial', 20)
        ).grid(row=3, column=0, pady=10)
        
        z_axis = tk.Label(self.x_frame, 
                    text='Z-Axis',
                    font=('Arial', 20)
        ).grid(row=4, column=0, pady=10)

        feed_rate = tk.Label(self.x_frame, 
                    text='FEED RATE',
                    justify=CENTER
        ).grid(row=5, column=0)

        spindle = tk.Label(self.x_frame, 
                    text='SPINDLE',
                    justify=CENTER
        ).grid(row=6, column=0)
      
    
class toolbox():
    def __init__(self, frame, height, width):
        tools = tk.LabelFrame(frame, text='Tool Box', labelanchor=N, padx=10, pady=10, font=16)
        tools.place(x=20, y=height*0.3+20, width=width*0.35, height=height*0.125)
        home_box = tk.Button(tools, text='Home Machine', width=15, height=2).grid(row=0, column=0)
        reset_zero_box = tk.Button(tools, text='Reset Zero', width=15, height=2).grid(row=1, column=0)
        return_zero_box = tk.Button(tools, text='Return To Zero', width=15, height=2).grid(row=0, column=1)
        soft_reset_box = tk.Button(tools, text='Soft Reset', width=15, height=2).grid(row=1, column=1)
        unlock_box = tk.Button(tools, text='Unlock', width=15, height=2).grid(row=0, column=2)
        get_state_box = tk.Button(tools, text='Check Mode', width=15, height=2).grid(row=1, column=2)
        check_mode_box = tk.Button(tools, text='Get State', width=15, height=2).grid(row=0, column=3)

class jog_control():
    def __init__(self, frame, height, width):
        control = tk.LabelFrame(frame, text='Jog Controller', labelanchor=N, padx=10, pady=10, font=16)
        control.place(x=20, y=height*0.45, width=width*0.35, height=height*0.44)
        n_w = tk.Button(control, text='n_w', width=15, height=3).grid(row=0, column=0)
        up = tk.Button(control, text='UP', width=15, height=3).grid(row=0, column=1)
        n_e = tk.Button(control, text='n_e', width=15, height=3).grid(row=0, column=2)
        z = tk.Button(control, text='Z+', width=15, height=3).grid(row=0, column=3)

        left = tk.Button(control, text='LEFT', width=15, height=3).grid(row=1, column=0)
        middle = tk.Button(control, text='__', width=15, height=3).grid(row=1, column=1)
        right = tk.Button(control, text='RIGHT', width=15, height=3).grid(row=1, column=2)
        blank = tk.Button(control, text='__', width=15, height=3).grid(row=1, column=3)

        s_w = tk.Button(control, text='s_w', width=15, height=3).grid(row=2, column=0)
        down = tk.Button(control, text='DOWN', width=15, height=3).grid(row=2, column=1)
        s_e = tk.Button(control, text='s_e', width=15, height=3).grid(row=2, column=2)
        z_ = tk.Button(control, text='Z-', width=15, height=3).grid(row=2, column=3)

        size_frame = tk.Frame(control)
        size_frame.grid(row=3, column=0, columnspan=3, pady=20)
        size_dimension = tk.Frame(control)
        size_dimension.grid(row=3, column=3, pady=20)

        step_size_xy = tk.Label(size_frame, text='Step Size XY', width=15, height=3).grid(row=0, column=0)
        step_size_xy_input = tk.Spinbox(size_frame, from_=0, to=10, width=25).grid(row=0, column=1)

        step_size_z = tk.Label(size_frame, text='Step Size Z', width=15, height=3).grid(row=1, column=0)
        step_size_z_input = tk.Spinbox(size_frame, from_=0, to=10, width=25).grid(row=1, column=1)

        step_size_abc = tk.Label(size_frame, text='Step Size ABC', width=15, height=3).grid(row=2, column=0)
        step_size_abc_input = tk.Spinbox(size_frame, from_=0, to=10, width=25).grid(row=2, column=1)

        feed_rate = tk.Label(size_frame, text='Feed Rate', width=15, height=3).grid(row=3, column=0)
        feed_rate_input = tk.Spinbox(size_frame, from_=0, to=10, width=25).grid(row=3, column=1)

        mm_label = tk.Button(size_dimension, text='Millimeters', width=15, height=3).grid(row=0, column=0)
        sm_label = tk.Button(size_dimension, text='Smaller', width=15, height=3).grid(row=1, column=0)
        lg_label = tk.Button(size_dimension, text='Larger', width=15, height=3).grid(row=2, column=0)

class console():
    def __init__(self, frame, height, width):
        box = tk.LabelFrame(frame, text='Console', labelanchor=N, padx=10, pady=10, font=16)
        box.place(x=width*0.35+40, y=height*0.6+20, width=width*0.6+40, height=height*0.27)

        scroll = tk.Scrollbar(box)
        scroll.pack(side=RIGHT, fill=Y)
        self.message_frame = tk.Listbox(box, width=int(width*0.6+40), height=int(height*0.27), yscrollcommand=scroll.set)
        self.message_frame.pack(side=tk.LEFT)

    def console_message(self, text):
        text = str(text)
        self.message_frame.insert(tk.END, text)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
