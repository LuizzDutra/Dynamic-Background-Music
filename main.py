import keyboard as kb
from pygame import mixer
from time import time, sleep
import win32api

music_intensity = 0
start_offset = 0

def activity_intensity(change:float):
    global music_intensity
    
    music_intensity += change

    if change > 0 and music_intensity > 0.5:
        music_intensity = 1

    if music_intensity < 0:
        music_intensity = 0
    if music_intensity > 1:
        music_intensity = 1


def change_music(music: mixer.music):
    global music_intensity
    global start_offset

    primary_point = 2
    secondary_point = 75

    if music_intensity > 0.5 and start_offset+music.get_pos()/1000 < secondary_point:
        mixer.music.fadeout(2000)
        sleep(2)
        music.stop()
        mixer.music.play(-1, secondary_point, 2000)
        start_offset = secondary_point
    elif music_intensity <= 0.5 and start_offset+music.get_pos()/1000 > secondary_point:
        mixer.music.fadeout(2000)
        sleep(2)
        music.stop()
        music.play(-1, primary_point, 2000)
        start_offset = primary_point

def music_debug():
    global music_intensity
    global start_offset
    print(music_intensity)
    print("pos, ", start_offset+mixer.music.get_pos()/1000)

def main():
    mixer.init(size= 32)
    mixer.music.load("OperaMusic.mp3")
    mixer.music.rewind()
    mixer.music.set_volume(1)
    mixer.music.play(-1)

    last_decrease = 0
    last_keys = [i for  i in range(0, 256)]
    for i in range(0, 256):
        win32api.GetAsyncKeyState(i)#init to avoid bug
    sleep(3)
    while True:
        for i in range(5, 256):
            if win32api.GetAsyncKeyState(i) != 0:
                if last_keys[i] != 1:
                    #print(i)
                    activity_intensity(0.066)
                last_keys[i] = 1
            else:
                last_keys[i] = 0




        if time() > last_decrease+1:
            music_debug()
            activity_intensity(-0.025)#descends the music passively
            last_decrease = time()

        change_music(mixer.music)

        sleep(0.05)



if __name__ == "__main__":
    main()
