# backup code----

# if yoke == yoke222:
#             self.currentCountEntry.configure(text=self.yoke_current_cnt["Yoke222"])
#             #  check for the current count of layer and the total count and update the status and check the mixup of yokes
#             if self.yoke_current_cnt["Yoke222"] == yoke_layer_count[yoke222] and self.layer_buffer != yoke_layer_count[yoke222]:
#                 self.layer_buffer = yoke_layer_count[yoke222]
#             elif self.yoke_current_cnt["Yoke222"] == 0 and self.layer_buffer == yoke_layer_count[yoke222]:
#                 self.layer_fill[self.i] = True  # layer is filled successfully
#                 customtkinter.CTkLabel(master=self.frame_left,
#                                        text=f"Layer {self.i} Filled", text_font=("Roboto Medium", -14)).grid(row=5 + self.i, column=0, pady=5, padx=1)
#                 # if i is equal to the total number of layers then stop the iteration and set the value of i to 0
#                 if self.i == yoke_total_layers[yoke222] - 1:
#                     self.i = 0
#                     # register the package of the yoke 222 in the file
#                     self.save_data(yoke222)
#                     # show the message that the yoke is filled successfully
#                     self.customtkinter.CTkLabel(text=f"Yoke {yoke222} Filled", text_font=(
#                         "Roboto Medium", -14)).grid(row=4 + self.i, column=0, pady=5, padx=1)

#                     # reset the self.layer_fill list
#                     self.layer_fill = [False for i in range(yoke_total_layers[yoke222])]
#                 else:
#                     self.i += 1
#                 self.layer_buffer = -1
#             # check the mixup of yokes
#             if self.yoke_current_cnt["Yoke231"] > 0 or self.yoke_current_cnt["Yoke238"] > 0:
#                 self.YOKE_MIX = True
#                 if self.YOKE_MIX == True:
#                     customtkinter.CTkLabel(master=self.frame_left, text="MESSAGE: NOT OKAY \n(MIXUP OF OTHER PARTS)", text_color="#E55F5F", text_font=(
#                         "Roboto Medium", -14)).grid(row=4 + self.i + 1, column=0, pady=5, padx=1)
#                 # if self.YOKE_MIX == False:
#                 #     self.YOKE_MIX = False
#                 #     customtkinter.CTkLabel(master=self.frame_left, text="").grid(row=4 + self.i + 1, column=0, pady=5, padx=1)
#             if self.yoke_current_cnt["Yoke231"] == 0 and self.yoke_current_cnt["Yoke238"] == 0:
#                 self.YOKE_MIX = False
#                 if self.YOKE_MIX == False:
#                     customtkinter.CTkLabel(master=self.frame_left, text="").grid(row=4 + self.i + 1, column=0, pady=5, padx=1)
#             # if the layer is not filled completely then show the message
#             elif self.yoke_current_cnt["Yoke222"] < yoke_layer_count[yoke222]:
#                 customtkinter.CTkLabel(master=self.frame_left, text=f"LAYER {self.i+1} NOT FILLED", text_color="#E55F5F", text_font=(
#                     "Roboto Medium", -14)).grid(row=4 + self.i + 2, column=0, pady=5, padx=1)
#         elif yoke == yoke231:
#             self.currentCountEntry.configure(text=self.yoke_current_cnt["Yoke231"])
#             #  check for the current count of layer and the total count and update the status and check the mixup of yokes
#             if self.yoke_current_cnt["Yoke231"] == yoke_layer_count[yoke231] and self.layer_buffer != yoke_layer_count[yoke231]:
#                 self.layer_buffer = yoke_layer_count[yoke231]
#             elif self.yoke_current_cnt["Yoke231"] == 0 and self.layer_buffer == yoke_layer_count[yoke231]:
#                 self.layer_fill[self.i] = True
#                 customtkinter.CTkLabel(self.frame_left,
#                                        text=f"Layer {self.i+1} Filled", text_font=("Roboto Medium", -14)).grid(row=4 + self.i, column=0, pady=5, padx=1)
#                 # if i is equal to the total number of layers then stop the iteration and set the value to i to 0
#                 if self.i == yoke_total_layers[yoke231] - 1:
#                     self.i = 0
#                     # register the package of the yoke 231 in the file
#                     self.save_data(yoke231)
#                     # reset the self.layer_fill list
#                     self.layer_fill = [False for i in range(yoke_total_layers[yoke231])]
#                 else:
#                     self.i += 1
#                 self.layer_buffer = -1
#             # check the mixup of yokes
#             if self.yoke_current_cnt["Yoke222"] > 0 or self.yoke_current_cnt["Yoke238"] > 0:
#                 customtkinter.CTkLabel(master=self.frame_left, text="MESSAGE: NOT OKAY\n(MIXUP OF OTHER PARTS)", text_color="#E55F5F", text_font=(
#                     "Roboto Medium", -14)).grid(row=4 + self.i + 1, column=0, pady=5, padx=1)
#             # if the layer is not filled completely then show the message
#             elif self.yoke_current_cnt["Yoke231"] < yoke_layer_count[yoke231]:
#                 customtkinter.CTkLabel(master=self.frame_left, text=f"LAYER {self.i+1} NOT FILLED", text_color="#E55F5F", text_font=(
#                     "Roboto Medium", -14)).grid(row=4 + self.i + 2, column=0, pady=5, padx=1)
#         elif yoke == yoke238:
#             self.currentCountEntry.configure(text=self.yoke_current_cnt["Yoke238"])
#             #  check for the current count of layer and the total count and update the status and check the mixup of yokes
#             if self.yoke_current_cnt["Yoke238"] == yoke_layer_count[yoke238] and self.layer_buffer != yoke_layer_count[yoke238]:
#                 self.layer_buffer = yoke_layer_count[yoke238]
#             elif self.yoke_current_cnt["Yoke238"] == 0 and self.layer_buffer == yoke_layer_count[yoke238]:
#                 self.layer_fill[self.i] = True
#                 customtkinter.CTkLabel(master=self.frame_left,
#                                        text=f"Layer {self.i+1} Filled", text_font=("Roboto Medium", -14)).grid(row=4 + self.i, column=0, pady=5, padx=1)
#                 # if i is equal to the total number of layers then stop the iteration and set the value to i to 0
#                 if self.i == yoke_total_layers[yoke238] - 1:
#                     self.i = 0
#                     # register the package of the yoke 238 in the file
#                     self.save_data(yoke238)
#                     # reset the self.layer_fill list
#                     self.layer_fill = [False for i in range(yoke_total_layers[yoke238])]
#                 else:
#                     self.i += 1
#                 self.layer_buffer = -1
#             # check the mixup of yokes
#             if self.yoke_current_cnt["Yoke222"] > 0 or self.yoke_current_cnt["Yoke231"] > 0:
#                 customtkinter.CTkLabel(master=self.frame_left, text="NOT OKAY \n(MIXUP OF OTHER PARTS)", text_color="#E55F5F", text_font=(
#                     "Roboto Medium", -14)).grid(row=4 + self.i + 1, column=0, pady=5, padx=1)
#             # if the layer is not filled completely then show the message
#             elif self.yoke_current_cnt["Yoke238"] < yoke_layer_count[yoke238]:
#                 customtkinter.CTkLabel(master=self.frame_left, text=f"LAYER {self.i+1} NOT FILLED", text_color="#E55F5F", text_font=(
#                     "Roboto Medium", -14)).grid(row=4 + self.i + 2, column=0, pady=5, padx=1)


dic = {1: 5,
       2: 6,
       3: 7,
       4: 8,
       }

for i in dic:
    print(dic[i])