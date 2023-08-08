from pygame import mixer
from time import time, sleep
import win32api

music_intensity = 0
start_offset = 0

KEYSTROKES_TO_HIGH_ACTIVITY = 10
TIME_TO_LOW_ACTIVITY = 30
VOLUME = 1

def activity_intensity(change:float):
    global music_intensity
    
    music_intensity += change

    if change > 0 and music_intensity > 0.5:
        music_intensity = 1

    if music_intensity < 0:
        music_intensity = 0
    if music_intensity > 1:
        music_intensity = 1


def change_music():
    global music_intensity
    global start_offset

    primary_music_start = 2
    primary_music_cutoff = 50
    secondary_music_start = 80
    secondary_music_cutoff = 141

    if music_intensity > 0.5 and (start_offset+mixer.music.get_pos()/1000 < secondary_music_start or start_offset+mixer.music.get_pos()/1000 > secondary_music_cutoff):
        mixer.music.fadeout(1000)
        sleep(1)
        mixer.music.stop()
        mixer.music.play(-1, secondary_music_start, 1000)
        start_offset = secondary_music_start
    elif music_intensity <= 0.5 and start_offset+mixer.music.get_pos()/1000 > primary_music_cutoff:
        mixer.music.fadeout(1000)
        sleep(1)
        mixer.music.stop()
        mixer.music.play(-1, primary_music_start, 1000)
        start_offset = primary_music_start

def music_debug():
    global music_intensity
    global start_offset
    print(music_intensity)
    print("pos, ", start_offset+mixer.music.get_pos()/1000)

def main():
    mixer.init(size= 32)
    mixer.music.load("OperaMusic.mp3")
    mixer.music.rewind()
    mixer.music.set_volume(VOLUME)
    mixer.music.play(-1)

    last_decrease = 0
    last_keys = [i for  i in range(0, 256)]
    for i in range(0, 256):
        win32api.GetAsyncKeyState(i)#init to avoid bug
    sleep(1)
    while True:

        for i in range(5, 256):
            if win32api.GetAsyncKeyState(i) != 0:
                if last_keys[i] != 1:
                    #print(i)
                    activity_intensity(0.5/KEYSTROKES_TO_HIGH_ACTIVITY)
                last_keys[i] = 1
            else:
                last_keys[i] = 0

        if time() > last_decrease+1:
            music_debug()
            activity_intensity(-0.5/TIME_TO_LOW_ACTIVITY)#descends the music passively
            last_decrease = time()

        change_music()

        sleep(0.05)



if __name__ == "__main__":
    main()
