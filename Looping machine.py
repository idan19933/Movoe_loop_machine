from tkinter import *
from tkinter.filedialog import askdirectory
import os
import tkinter as tk
import pygame



###################################
# Defining tkinter object
###################################
class MusicPlayer():
    color_list = ['red', 'brown', 'brown', 'green']
    root = None
    MUSIC_END = pygame.USEREVENT+1
    num_of_chanells = 9
    full_path = []
    sound_items = []
    channel_list = []
    set_loop_type_button = None
    uploade_songs_button = None
    is_loop = False
    playBut = None
    previous_is_loop = False
    sound_name_list = []
    mute_button_list = []
    mute_button_state = []
    mute_lists = [0,1,1,1,0,0,1,1,1]

###################################
# Starting app
###################################
    def start(self):
        self.init_ui()
        self.init_pygame()
        self.root.mainloop()

##############################################################
# initialing pygame modules and getting channels ready to play
##############################################################
    def init_pygame(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(self.MUSIC_END)
        pygame.mixer.set_num_channels(self.num_of_chanells)
        for index in range(self.num_of_chanells):
            self.channel_list.append(pygame.mixer.Channel(index))
        pygame.mixer.music.load('C:/Users/97254/PycharmProjects/Execercises/MyMusicPlayer/sound1.mp3')
        pygame.mixer.music.set_volume(0)

##############################################################
# initialing tkinter settings
##############################################################

    def init_ui(self):
        tk_root = tk.Tk()
        self.root = tk_root
        self.ToggelLoop()
        self.uploade_songs_button = Button(tk_root, text="Uploade songs", fg="green", bg="black", command=self.UplodeSounds)
        self.uploade_songs_button.pack(side=BOTTOM)
        tk_root.geometry("480x480")

##############################################################
# Checking when the tracks finish to play
##############################################################
    def check_event(self):
        self.MUSIC_END = pygame.USEREVENT + 1
        inloop  = True
        no_loop = False
        for event in pygame.event.get():
            if event.type == self.MUSIC_END:
                print('music end event')
                if self.previous_is_loop == inloop and self.is_loop == no_loop:
                    pygame.mixer.stop()
                else:
                    index = 0
                    if self.is_loop == True:
                        pygame.mixer.music.play()
                        for sound in self.sound_items:
                            if self.mute_lists[index] == 1:
                                self.channel_list[index].play(pygame.mixer.Sound(sound), -1)
                            index += 1
        self.root.after(1, self.check_event)

##############################################################
# Playing music and detecting if ToggelLoop function is active
##############################################################
    def play(self):
        loopType = 0
        if self.is_loop:
            loopType = -1
        index = 0
        pygame.mixer.music.load(f'{self.full_path[0]}')
        pygame.mixer.music.play()
        for sound in self.sound_items:
            self.channel_list[index].play(pygame.mixer.Sound(sound), loopType)
            index += 1

        self.check_event()

#########################################################################
# Uploading the tracks the user want to user and creating the play button
#########################################################################

    def UplodeSounds(self):
        directory = askdirectory()
        os.chdir(directory)
        sound_file_names = os.listdir()

        index = 0
        for sound_name in sound_file_names:
            self.sound_name_list.append(sound_name)
            full_path = f"{directory}/{sound_name}"


            self.full_path.append(full_path)
            sound = pygame.mixer.Sound(full_path)
            self.sound_items.append(sound)
            index +=1
        if len(self.sound_items) > 0:
            self.uploade_songs_button.destroy()
            self.playBut = Button(self.root, text="Play", fg="green", bg="black", command=self.play)
            self.playBut.pack(side=BOTTOM)
        # self.make_mute_butt()
        self.make_chanels(self.sound_name_list)

############################################
# Creating the looping button functionality
############################################
    def ToggelLoop(self):
        self.previous_is_loop = self.is_loop
        if self.is_loop:
            self.is_loop = False
            button_name = "Not Looping"
        else:
            self.is_loop = True
            button_name = "Looping"

        if self.set_loop_type_button == None:
            self.set_loop_type_button = Button(self.root, text=button_name, fg="green", bg="black",
                                               command=self.ToggelLoop)
            self.set_loop_type_button.pack(side=BOTTOM)
        else:
            self.set_loop_type_button.config(text=button_name)



    def MuteSoundCallbackFactory(self, i):
        return lambda: self.MuteSound(i)

##############################################################
# Making the chanells and mute buttons
##############################################################
    def make_chanels(self,sounds):
        for chanel in range(self.num_of_chanells):
            sound_frame = Frame(self.root)
            sound_frame.grid_columnconfigure(chanel)
            mute_button = Button(sound_frame, bg="green", text='Mute', command=self.MuteSoundCallbackFactory(chanel))
            self.mute_button_list.append(mute_button)
            self.mute_button_state.append(False)
            mute_button.grid(column=0, row=0, sticky='new', padx=3, pady=2)
            lable = Label(sound_frame,text=sounds[chanel], bg="green",width=50)
            lable.grid(column=1, row=0, sticky='new', padx=3, pady=2)
            sound_frame.pack()

##############################################################
# Making the mute button functionality
##############################################################
    def MuteSound(self, index):
        is_muted = self.mute_button_state[index]
        if is_muted:
            self.mute_button_state[index] = False
            self.mute_button_list[index].config(bg="green")
        else:
            self.mute_button_state[index] = True
            chanel = pygame.mixer.Channel(index)
            chanel.stop()
            self.mute_button_list[index].config(bg="red")

#######################
# Creating mute buttons
#######################
    def make_mute_butt(self):
        for button in range(self.num_of_chanells):
            mute_button = Button(self.root,text="Mute")
            mute_button.pack(side=BOTTOM)

mp = MusicPlayer()
MusicPlayer.start(mp)



