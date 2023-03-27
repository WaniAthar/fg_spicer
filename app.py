'''
Code Author: Athar Mujtaba Wani
email: 01fe20bcs054@kletech.ac.in
KLE Technological University
'''
import datetime
import os
import time
# import tkinter
import tkinter.filedialog
import tkinter.messagebox
import warnings
import customtkinter
import cv2
import pandas as pd
import PIL.Image
import PIL.ImageTk
import torch
from PIL import Image, ImageTk


# import yolov5    #for production use the package
warnings.filterwarnings("ignore") 

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


YOKE_LIST = ['Yoke231', 'Yoke238', 'Yoke222']
YOKE_COUNT = [48, 48, 63]
YOKE_TOTAL_LAYERS = [3, 3, 3]
YOKE_LAYER_COUNT = [16, 16, 21]

yoke231, yoke238, yoke222 = YOKE_LIST[0], YOKE_LIST[1], YOKE_LIST[2]

# yoke_count_dict = {yoke222: 63, yoke231: 64, yoke238: 48}
# yoke_layer_count = {yoke222: 21, yoke231: 16, yoke238: 16}
# yoke_total_layers = {yoke222: 3, yoke231: 4, yoke238: 3}

yoke_count_dict = dict(zip(YOKE_LIST, YOKE_COUNT))
yoke_layer_count = dict(zip(YOKE_LIST, YOKE_LAYER_COUNT))
yoke_total_layers = dict(zip(YOKE_LIST, YOKE_TOTAL_LAYERS))
# The intermediate buffer to store the current layer count
# max count of layers is 4

CANVAS_WIDTH, CANVAS_HEIGHT = 1100, 825
# CANVAS_WIDTH, CANVAS_HEIGHT = 1080, 1920


class App(customtkinter.CTk):

    WIDTH = 960
    HEIGHT = 720
    ROOT_DIR = os.getcwd()

    def __init__(self):
        super().__init__()

        self.YOKE_MIX = False

        self.i = 0
        self.layer_buffer = -1
        self.layer_fill = [False, False, False, False]   # max 4 layers
        self.title("FG Packaging")
        # self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        # open window maximized
        self.state("zoomed")
        # call .on_closing() when app gets closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        # ----=-=-=-=-==Model===-=-=-=-=----
        self.model = torch.hub.load(App.ROOT_DIR  # Use backend for yolov5 in this folder
                                    , 'custom'  # to use model in this folder
                                      , path='static\\weights\\best.pt'  # the name of model is this folder
                                      , source='local'  # to use backend from this folder
                                      , force_reload=True  # clear catch
                                      , device=self.device
                                    )
        # self.model = yolov5.load('static\\weights\\best.pt')  # for production
        self.model.conf = 0.50  # NMS confidence threshold
        self.model.iou = 0.20  # IoU threshold
        self.model.multi_label = False  # NMS multiple labels per box
        self.model.max_det = 1000
        self.model.imgsz = 416
        # ----=-=-=-=-==Model End===-=-=-=-=----
        # ============ create three frames ============

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # self.mainframe = customtkinter.CTkFrame(master=self,)
        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 corner_radius=25,)
        self.frame_left.grid(row=0, column=0, padx=20, pady=20, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self,
                                                  corner_radius=25,)
        self.frame_right.grid(row=0, column=1, rowspan=6, padx=20, pady=20, sticky="nswe")

    # #    create a frame in the bottom of the screen
    #     self.frame_bottom = customtkinter.CTkFrame(master=self,
    #                                                 corner_radius=25,)
    #     self.frame_bottom.grid(row=0, column=2,padx=20, pady=20, sticky="nswe")
        self.start_stop = customtkinter.CTkFrame(master=self,
                                                 corner_radius=25,)
        self.start_stop.grid(row=4, column=0, padx=20, pady=20, sticky="nswe")

        # ============ frame_left ============

        # add logo to the top left corner of the left frame
        self.dana_logo = ImageTk.PhotoImage(Image.open("static\\images\\dana_logo_1_100x53.png"))
        self.dana_logo_label = customtkinter.CTkLabel(master=self.frame_left,
                                                      image=self.dana_logo,
                                                      )
        self.dana_logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        # self.dana_logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        # self.dana_logo.grid(row=0, column=0, padx=20, pady=20, sticky="nswe")

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Yoke Details",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=0, column=1, pady=10, padx=5)
        self.label_for_yoke = customtkinter.CTkLabel(master=self.frame_left,
                                                     text="Selected Yoke:",
                                                     text_font=("Roboto Medium", -14))
        self.label_for_yoke.grid(row=1, column=0, pady=5, padx=1)
        self.selectYoke = customtkinter.CTkComboBox(master=self.frame_left,
                                                    values=YOKE_LIST, command=self.changeYoke)

        self.filepathExcelEntry = customtkinter.CTkEntry(master=self.frame_left,
                                                         placeholder_text="Select Excel File",
                                                         text_font=("Roboto Medium", -14))
        self.filepathExcelEntry.grid(row=2, column=0, pady=5, padx=5)
        self.fileButton = customtkinter.CTkButton(master=self.frame_left,
                                                  text="Choose File",
                                                  command=self.button_event)
        self.fileButton.grid(row=2, column=2, pady=10, padx=10)

        self.selectYoke.grid(row=1, column=2, pady=10, padx=10)
        self.finalCount = customtkinter.CTkLabel(master=self.frame_left,
                                                 text="Final Count:",
                                                 text_font=("Roboto Medium", -14))
        self.finalCount.grid(row=3, column=0, pady=5, padx=1)
        self.finalCountEntry = customtkinter.CTkLabel(master=self.frame_left,
                                                      text='64',
                                                      text_font=("Roboto Medium", -14))

        self.finalCountEntry.grid(row=3, column=2, pady=5, padx=5)

        self.currentCount = customtkinter.CTkLabel(master=self.frame_left,
                                                   text="Current Count:",
                                                   text_font=("Roboto Medium", -14))
        self.currentCount.grid(row=4, column=0, pady=5, padx=1)
        self.currentCountEntry = customtkinter.CTkLabel(master=self.frame_left,
                                                        text='--',
                                                        text_font=("Roboto Medium", -14))
        self.currentCountEntry.grid(row=4, column=2, pady=5, padx=5)

        # ========================start stop button==========================

        self.startButton = customtkinter.CTkButton(master=self.start_stop,
                                                   text="Start", width=400, height=50, command=self.startfoo)
        self.startButton.grid(row=0, column=0, pady=10, padx=10)
        self.startButton = customtkinter.CTkButton(master=self.start_stop,
                                                   text="Stop", width=400, height=50, fg_color="#E55F5F", command=self.stopfoo)
        self.startButton.grid(row=1, column=0, pady=10, padx=25)

        # ========================== frame_right ============================
        # open camera in frame_right and show it in the center of the frame
        # canvas
        self.canvas = customtkinter.CTkCanvas(master=self.frame_right,
                                              width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.grid(row=0, column=0, pady=60, padx=60)

        self.frame_right.grid_propagate(False)  #


# ========================== UI methods ============================
    yoke_current_cnt = {i: 0 for i in YOKE_LIST}    # dictionary to store current count of each yoke type --default 0

    def update_frame(self):

        ret, frame = self.camera.read()
    #  resize the frame to fit the canvas
        frame = cv2.resize(frame, (CANVAS_WIDTH, CANVAS_HEIGHT))  # remove comment to resize the frame
        # rgb
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # remove comment to convert the frame to rgb

        if ret:
            self.results = self.model(frame)
            self.results.render()

            self.bboxes = self.results.xyxy[0]
            self.class1 = self.bboxes[self.bboxes[:, 5] == 0]
            self.class2 = self.bboxes[self.bboxes[:, 5] == 1]
            self.class3 = self.bboxes[self.bboxes[:, 5] == 2]

            self.yoke_current_cnt["Yoke222"] = len(self.class1)   # yoke 222
            self.yoke_current_cnt["Yoke231"] = len(self.class2)   # yoke 231
            self.yoke_current_cnt["Yoke238"] = len(self.class3)   # yoke 238
            # add more classes here manually if the model is modified
            # reference = {0:yoke222,1:yoke231,2:yoke238}
            # print(self.results.names[0])
            # print the number of bounding boxes of class 2

            # print the class name along with the count of detections
            for y in self.yoke_current_cnt:
                print(f"{y} :", self.yoke_current_cnt[y], end=" ")
            print()   # print a new line///// alternatively you can use print("\n")

            self.LayerSeperator(self.selectYoke.get())
            # show image to the canvas
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.after(15, self.update_frame)

    def startfoo(self):
        '''Starts the camera and the update_frame function'''
        self.camera = cv2.VideoCapture(0)   
        # read from ip camera in and show it in the center of the frame

        # self.camera = cv2.VideoCapture("C:\\Users\\athar\\Downloads\\Video\\VID20221105113424-compressed.mp4")

        self.update_frame()
        print("start")
        # self.x.start()

    def stopfoo(self):
        ''' Stops the camera and the update_frame function'''
        self.camera.release()
        print("stop")
        # self.x.stop()

        # ============ frame_bottom ============

    def LayerSeperator(self, yoke):
        '''Seperates the layers of the yokes in the box'''
        for each_yoke in YOKE_LIST:
            if each_yoke == yoke:
                self.currentCountEntry.configure(text=f"\t")
                self.currentCountEntry.configure(text=self.yoke_current_cnt[yoke])
                #  check for the current count of layer and the total count and update the status and check the mixup of yokes
                if self.yoke_current_cnt[yoke] == yoke_layer_count[yoke] and self.layer_buffer != yoke_layer_count[yoke]:
                    self.layer_buffer = yoke_layer_count[yoke]
                elif self.yoke_current_cnt[yoke] == 0 and self.layer_buffer == yoke_layer_count[yoke]:
                    self.layer_fill[self.i] = True  # layer is filled successfully
                    customtkinter.CTkLabel(master=self.frame_left,
                                           text=f"Layer {self.i+1} Filled", text_font=("Roboto Medium", -14), text_color="#0AAE2B").grid(row=5 + self.i, column=0, pady=5, padx=1)
                    customtkinter.CTkLabel(master=self.frame_left,
                                           text=f" ", text_font=("Roboto Medium", -14), text_color="#0AAE2B").grid(row=5, column=2, pady=5, padx=1)

                    # if i is equal to the total number of layers then stop the iteration and set the value of i to 0
                    if self.i == yoke_total_layers[yoke] - 1:
                        self.i = 0
                        # register the package of the yoke in the file
                        self.save_data(yoke)
                        # show the message that the yoke is filled successfully
                        customtkinter.CTkLabel(master=self.frame_left,
                                               text=f" ", text_font=("Roboto Medium", -14), text_color="#0AAE2B").grid(row=5, column=2, pady=5, padx=1)
                        customtkinter.CTkLabel(master=self.frame_left,
                                               text=f"{yoke} Filled √", text_font=("Roboto Medium", -14), text_color="#0AAE2B").grid(row=5, column=2, pady=5, padx=1)

                        # reset the self.layer_fill list
                        self.layer_fill = [False for i in range(yoke_total_layers[yoke])]
                    else:
                        self.i += 1
                    self.layer_buffer = -1    # reset/empty the layer buffer
                # check the mixup of yokes
                for y in YOKE_LIST:
                    if self.yoke_current_cnt[y] == 0 and y != yoke:
                        self.YOKE_MIX = False
                        if self.YOKE_MIX == False:
                            customtkinter.CTkLabel(master=self.frame_left, text=f"\t\t").grid(
                                row=4 + self.i + 2, column=0, pady=5, padx=1)
                            break
                    elif self.yoke_current_cnt[y] > 0 and y != yoke:
                        self.YOKE_MIX = True
                        if self.YOKE_MIX == True:
                            customtkinter.CTkLabel(master=self.frame_left, text="(MIXUP OF OTHER PARTS)", text_color="#E55F5F", text_font=(
                                "Roboto Medium", -14)).grid(row=4 + self.i + 2, column=0, pady=5, padx=1)
                            break

                # if the layer is not filled completely then show the message

                if self.yoke_current_cnt[yoke] != yoke_layer_count[yoke]:
                    customtkinter.CTkLabel(master=self.frame_left, text=f"\t\t", text_color="#F2FF00", text_font=(
                        "Roboto Medium", -14)).grid(row=4 + self.i + 1, column=0, pady=5, padx=1)
                    customtkinter.CTkLabel(master=self.frame_left, text=f"LAYER{self.i+1} NOT FILLED", text_color="#F2FF00", text_font=(
                        "Roboto Medium", -14)).grid(row=4 + self.i + 1, column=0, pady=5, padx=1)
                    break
                else:
                    customtkinter.CTkLabel(master=self.frame_left, text=f"\t\t").grid(
                        row=4 + self.i + 1, column=0, pady=5, padx=1)

    def button_event(self, event=None):
        '''Button event to select the output excel file'''
        # choose output file
        self.file = tkinter.filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select file",
            filetypes=(("Excel files", "*.xlsx"), ("csv files", "*.csv")))
        self.filepathExcelEntry.insert(0, self.file)

    def change_appearance_mode(self, new_appearance_mode):
        if customtkinter.get_appearance_mode() == new_appearance_mode:
            customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()

    def changeYoke(self, yokeselected):
        self.countHandler(yokeselected)
        print("Yoke selected: " + yokeselected)

    def countHandler(self, yokeselected):
        for yoke in yoke_count_dict:
            if yoke == yokeselected:
                self.finalCountEntry.configure(text=yoke_count_dict[yoke])

    def save_data(self, yoke):
        '''Save the data to the selected output excel file'''
        df = pd.read_excel(self.filepathExcelEntry.get())
        # get the current date and time
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        # get the current count of the yoke
        current_count = yoke_count_dict[yoke]
        # get the total count of the yoke
        total_count = yoke_count_dict[yoke]
        message = "OKAY"
        # save the data to the excel file
        df = df.append({'Date': dt_string, 'Yoke': yoke, 'Detected Count': current_count,
                       'Total Count': total_count, 'Result': message}, ignore_index=True)
        df.to_excel(self.file, index=False)
        # clear all the messages of the yoke
        for i in range(1, 6):
            customtkinter.CTkLabel(master=self.frame_left, text=f"\t\t").grid(
                row=4 + i, column=0, pady=5, padx=1)
        # clear the entry box
        self.currentCountEntry.configure(text=" -- ")

        

    # save the state of incomplete boxes
    def save_state(self):
        # get the current layer fill and save it to the file locally so that it can be used to resume the process
        with open('layer_fill.txt', 'w') as f:
            for item in self.layer_fill:
                f.write("%s " % item)

    def load_state(self):
        # load the state of the layer fill from the file
        with open('layer_fill.txt', 'r') as f:
            for line in f:
                self.layer_fill = line.split()
                # move the i iterator to the last layer that was filled
                for i in range(len(self.layer_fill)):
                    if self.layer_fill[i] == False:
                        self.i = i
                        break
                    else:
                        self.i = len(self.layer_fill)


if __name__ == "__main__":
    app = App()
    app.mainloop()