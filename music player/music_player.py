import os
import pygame
from tkinter import filedialog, Tk, Menu, Listbox, PhotoImage, Frame, Button, END


# Choose a folder filled with downloaded mp3 music to add into the player

# Initialize main application window
root = Tk()
root.title("Music Player")
root.geometry("500x300")

# Initialize Pygame mixer
pygame.mixer.init()

# Global variables
songs = []
current_song = ""
paused = False

def load_music():
    """Load music from selected directory."""
    global current_song
    root.directory = filedialog.askdirectory()
    
    songs.clear()
    songlist.delete(0, END)
    
    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == ".mp3":
            songs.append(song)
            songlist.insert(END, song)
    
    if songs:
        songlist.selection_set(0)
        current_song = songs[0]

def play_music():
    """Play or resume the selected music."""
    global current_song, paused
    if not paused:
        pygame.mixer.music.load(os.path.join(root.directory, current_song))
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.unpause()
        paused = False

def pause_music():
    """Pause the currently playing music."""
    global paused
    pygame.mixer.music.pause()
    paused = True

def next_music():
    """Play the next song in the list."""
    global current_song
    try:
        index = (songs.index(current_song) + 1) % len(songs)
        songlist.selection_clear(0, END)
        songlist.selection_set(index)
        current_song = songs[index]
        play_music()
    except ValueError:
        pass

def prev_music():
    """Play the previous song in the list."""
    global current_song
    try:
        index = (songs.index(current_song) - 1) % len(songs)
        songlist.selection_clear(0, END)
        songlist.selection_set(index)
        current_song = songs[index]
        play_music()
    except ValueError:
        pass

# Menu bar setup
menubar = Menu(root)
root.config(menu=menubar)
organise_menu = Menu(menubar, tearoff=False)
organise_menu.add_command(label="Select Folder", command=load_music)
menubar.add_cascade(label="Add Music", menu=organise_menu)

# Song list display
songlist = Listbox(root, bg="black", fg="white", width=100, height=15)
songlist.pack()

# Load button images
play_btn_image = PhotoImage(file="play.png")
pause_btn_image = PhotoImage(file="pause.png")
next_btn_image = PhotoImage(file="next.png")
prev_btn_image = PhotoImage(file="previous.png")

# Control buttons frame
control_frame = Frame(root)
control_frame.pack()

# Control buttons
Button(control_frame, image=prev_btn_image, borderwidth=0, command=prev_music).grid(row=0, column=0, padx=7, pady=10)
Button(control_frame, image=play_btn_image, borderwidth=0, command=play_music).grid(row=0, column=1, padx=7, pady=10)
Button(control_frame, image=pause_btn_image, borderwidth=0, command=pause_music).grid(row=0, column=2, padx=7, pady=10)
Button(control_frame, image=next_btn_image, borderwidth=0, command=next_music).grid(row=0, column=3, padx=7, pady=10)

# Run main event loop
root.mainloop()
