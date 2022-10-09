from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
import pygame
import random
from time import *
from mutagen.mp3 import MP3

page = Tk()
page.title('MUSIC PLAYER 2.0')
page.geometry('690x1180')
pygame.mixer.init()

play_img = PhotoImage(file='PNGs/play_btn.png')
stop_img = PhotoImage(file='PNGs/stop_btn.png')
bskip_img = PhotoImage(file='PNGs/bskip_btn.png')
skip_img = PhotoImage(file='PNGs/skip_btn.png')
pause_img = PhotoImage(file='PNGs/pause_btn.png')
music_img = PhotoImage(file='PNGs/music_btn.png')
shuffle_img = PhotoImage(file='PNGs/shuffle.png')

global paused
paused = False

def timer():
	global play_time
	play_time = pygame.mixer.music.get_pos() / 1000
	
	global play_form
	play_form = strftime('%M:%S', gmtime(play_time))
	
	current_song = songs_list.curselection()
	song = songs_list.get(current_song)
	song = f'/storage/0403-0201/Music/{song}.mp3'
	mut = MP3(song)
	song_length = mut.info.length
	
	global len_form
	len_form = strftime('%M:%S', gmtime(song_length))
	play_time += 1
	if int(slider_btn.get()) == int(song_length):
		count_bar.config(text= f'{len_form}                                                                                                                   {len_form}')
	elif int(slider_btn.get()) == int(play_time):
		slide_position = int(song_length)
		slider_btn.config(to=slide_position, value=int(play_time))
	else :
		slide_position = int(song_length)
		slider_btn.config(to=slide_position, value=int(slider_btn.get()))
		slide_form = strftime('%M:%S', gmtime(slider_btn.get()))
		count_bar.config(text= f'{slide_form}                                                                                                                   {len_form}')
		next_time = int(slider_btn.get()) +1
		slider_btn.config(value=next_time)
    
	count_bar.after(1000, timer)

def add_songs():
    songs = filedialog.askopenfilenames(initialdir='/storage/0403-0201/Music', title='Music', filetypes=(('mp3 Files', '*.mp3'),))
    for song in songs:
        song = song.replace('/storage/0403-0201/Music/', '')
        song = song.replace('.mp3', '')
        songs_list.insert(END, song)

def play(is_paused):
    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        song = songs_list.get(ACTIVE)
        song = f'/storage/0403-0201/Music/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        
    play_btn.grid_forget(), pause_btn.grid(row=0,column=1)
    play_bun.grid_forget(), pause_bun.grid(row=4,column=2)
    
    title = is_paused.widget.curselection()[0]
    song = is_paused.widget.get(title)
    sing = f'/storage/0403-0201/Music/{song}.mp3'
    pygame.mixer.music.load(sing)
    pygame.mixer.music.play(loops=0)
    
    lab_lab.config(text=song)
    lab_btn.config(text=song)
    timer()
    slider_btn.config(value=int(play_time))
    count_bar.config(text= f'{play_form}                                                                                                                 {len_form}')
def slider(x):
	song = songs_list.get(ACTIVE)
	song = f'/storage/0403-0201/Music/{song}.mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0, start=int(slider_btn.get()))
   
def pause(is_paused):
    global paused
    paused = is_paused
    pygame.mixer.music.pause()
    paused = True
    
    pause_btn.grid_forget(), play_btn.grid(row=0,column=1)
    pause_bun.grid_forget(), play_bun.grid(row=4,column=2)
    
    timer()
    slider_btn.config(value=int(play_time))
    count_bar.config(text= f'{play_form}                                                                                                                 {len_form}')
def shuffle():
	list = songs_list.get(0, END)
	song = random.choice(list)
	sing = f'/storage/0403-0201/Music/{song}.mp3'
	pygame.mixer.music.load(sing)
	pygame.mixer.music.play(loops=0)
	
	songs_list.selection_clear(0, END)
	lab_lab.config(text=song)
	lab_btn.config(text=song)
	
	timer()
	slider_btn.config(value=int(play_time))
	count_bar.config(text= f'{play_form}                                                                                                                 {len_form}')
def next():
	next_song = songs_list.curselection()
	next_song = next_song[0]+1
	song = songs_list.get(next_song)
	sing = f'/storage/0403-0201/Music/{song}.mp3'
	pygame.mixer.music.load(sing)
	pygame.mixer.music.play(loops=0)
	
	songs_list.selection_clear(0, END)
	songs_list.activate(next_song)
	songs_list.selection_set(next_song, last=None)
	
	lab_lab.config(text=song)
	lab_btn.config(text=song)
	
	timer()
	slider_btn.config(value=int(play_time))
	count_bar.config(text= f'{play_form}                                                                                                                 {len_form}')
def back():
	next_song = songs_list.curselection()
	next_song = next_song[0]-1
	song = songs_list.get(next_song)
	sing = f'/storage/0403-0201/Music/{song}.mp3'
	pygame.mixer.music.load(sing)
	pygame.mixer.music.play(loops=0)
	
	songs_list.selection_clear(0, END)
	songs_list.activate(next_song)
	songs_list.selection_set(next_song, last=None)
	
	lab_lab.config(text=song)
	lab_btn.config(text=song)
	
	timer()
	slider_btn.config(value=int(play_time))
	count_bar.config(text= f'{play_form}                                                                                                                 {len_form}')		
def stop():
    pygame.mixer.music.stop()
    songs_list.selection_clear(ACTIVE)
    
    slider_btn.config(value=0)
    count_bar.config(text='')
    lab_lab.config(text='')
    lab_btn.config(text='')
    
def del_song():
	pygame.mixer.music.stop()
	songs_list.delete(ACTIVE)
	
	slider_btn.config(value=0)
	count_bar.config(text='')
	lab_lab.config(text='')
	lab_btn.config(text='')

def clear_list():
	pygame.mixer.music.stop()
	songs_list.delete(0,END)
	
	slider_btn.config(value=0)
	count_bar.config(text='')
	lab_lab.config(text='')
	lab_btn.config(text='')

def volume(x):
	pygame.mixer.music.set_volume(volume_btn.get())

def goto(btn):
	if btn == 'menu':
		mother3.grid_forget(), mother.grid_forget(), mother1.grid()
	elif btn == 'songs':
		mother3.grid(),child.grid(columnspan=2)
	elif btn == 'btn':
		mother.grid_forget(),mother3.grid_forget(),mother2.grid()
	elif btn == 'back':
		mother2.grid_forget(),mother1.grid_forget(),mother.grid(),mother3.grid()

	
mother = Frame(page)
mother.grid()

Button(mother,text='≡',font=('arial',18,'bold'),borderwidth=0,command=lambda:goto('menu')).grid(row=0,sticky='w')

Button(mother,text='+',font=('arial',15,'bold'),borderwidth=0,command=add_songs).grid(row=0,column=1,sticky='e')

Label(mother,text='NS Player',font=('arial',10,'bold')).grid(row=0,sticky='e')

Label(mother,text='Songs',font=('arial',6,'bold')).grid(row=1,columnspan = 2, pady=20)

mother1 = Frame(page)

Button(mother1,text='←',font=('arial',14,'bold'),borderwidth=0,command=lambda:goto('back')).grid(row=0,column=0,sticky='w')

Label(mother1,text='Settings',font=('arial',10,'bold')).grid(row=0, column = 1, pady = 40, sticky='w')

Label(mother1,text='To Remove Song',font=('arial',6)).grid(row=1,sticky='w')

Button(mother1, text='Click Here...',fg='red',borderwidth=0,font=('arial',5,'bold'),command=del_song).grid(row=1,column=1,pady=20)

Label(mother1,text='To Clear Playlist',font=('arial',6)).grid(row=2,sticky='w')

Button(mother1,text='Click Here...',fg='red',borderwidth=0,font=('arial',5,'bold'),command=clear_list).grid(row=2,column=1,pady=20)

Label(mother1,text='Set Volume : ',font=('arial',6,'bold')).grid(row=4,sticky='w')

volume_btn = ttk.Scale(mother1, from_=0,to=1,orient=HORIZONTAL,value=1,length=450,command=volume)
volume_btn.grid(row=4,column=1,pady=20,sticky='w')

child = Frame(mother)
child.grid(columnspan=2)
songs_list = Listbox(child, width=38,height=22,bg='silver')
songs_list.bind('<<ListboxSelect>>',play)
songs_list.grid(row=0,columnspan=2)

mother2 = Frame(page)

Button(mother2,text='←',font=('arial',14,'bold'),borderwidth=0,command=lambda:goto('back')).grid(row=0,columnspan=2,sticky='w')

lab_lab = Label(mother2,text='',font=('arial',6,'bold'))
lab_lab.grid(row=0,column=1,columnspan=3,pady=(30,0))

Label(mother2,image=music_img).grid(row=1,columnspan=5,pady=20)

count_bar = Label(mother2, text='', font=('arial',5))
count_bar.grid(row=3,columnspan=5)

Button(mother2,image=bskip_img,borderwidth=0,command=back).grid(row=4,column=1)

Button(mother2, image=stop_img, borderwidth=0,command=stop).grid(row=4,column=4)

Button(mother2,image=skip_img,borderwidth=0,command=next).grid(row=4,column=3)

Button(mother2,image=shuffle_img,borderwidth=0,command=shuffle).grid(row=4,column=0)

pause_bun = Button(mother2,image=pause_img,borderwidth=0,command=lambda: pause(paused))

play_bun = Button(mother2,image=play_img,borderwidth=0,command=lambda: play(paused))

slider_btn = ttk.Scale(mother2,from_=0,to=100,orient=HORIZONTAL,value=0,length=550,command=slider)
slider_btn.grid(row=3,column=0,columnspan=5)

mother3 = Frame(page)
mother3.grid()

lab_btn = Button(mother3,text='',font=('arial',6,'bold'),borderwidth=0,command=lambda:goto('btn'))

lab_btn.grid(row=0,column=0)
pause_btn = Button(mother3,image=pause_img,borderwidth=0,command=lambda:pause(paused))

play_btn = Button(mother3,image=play_img,borderwidth=0,command=lambda:play(paused))

page.mainloop()