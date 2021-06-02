# standard libs
import asyncio
import argparse

# third party libs
import pygame as pg
import sounddevice as sd


# tried to learn "asyncio" while making this so called project. Still got roads to cover
# a lot pygame functionality is still not implemented

# argument parsing
parser = argparse.ArgumentParser(description="uses monitor's backlight to visualize music")
parser.add_argument("--fps", help="Frames per second of visuals (default=30)")
parser.add_argument("--size", help="tuple for size of the screen ((1920,1080) by default)")
parser.add_argument("--threshold", help="threshold for determining color (default=20000)")
args = parser.parse_args()

# defining some important variables
if args.size is None:
    size = (1920, 1080)
else:
    size = (args.size).split(",")
    size = [int(i) for i in size]
    size = tuple(size)
if args.fps is None:
    fps = 30
else:
    try:
        fps = int(args.fps)
    except Exception as e:
        print(e)
if args.threshold is None:
    threshold = 20000
else:
    try:
        threshold = int(args.threshold)
    except Exception as e:
        print(e)
    

# variable of sounddevice
sd.default.samplerate = 22050
block = sd.default.samplerate // fps


# code for using input stream with async 
async def inputstream_generator(block, channels=1, **kwargs):
    # block: size of array which holds the input data 
    # before putting it in a queue.
    q_in = asyncio.Queue()
    Loop = asyncio.get_event_loop()

    def callback(indata, frame_count, time_info, status):
        Loop.call_soon_threadsafe(q_in.put_nowait, max(indata))


    stream = sd.InputStream(callback=callback, channels=channels, blocksize=block,
    dtype='int16', **kwargs)

    with stream:
        while True:
            indata = await q_in.get()
            yield indata

# determine color through a lot of if/else
async def color_gen(threshold):
    async for indata in inputstream_generator(block):  
        color = (0,0,0)
        if indata == 0:
            color = (0,0,0)
        elif indata > 0 and indata <= threshold * 7//100 :
            color = (179, 5, 5)
        elif indata > threshold * (7//100) and indata <= threshold * 14//100 :
            color = (255, 0, 0)
        elif indata > threshold * (14//100) and indata <= threshold * 21//100 :
            color = (255, 0, 102)
        elif indata > threshold * 21//100 and indata <= threshold * 28//100 :
            color = (204, 51, 153)
        elif indata > threshold * 28//100 and indata <= threshold * 35//100 :
            color = (153, 0, 153)
        elif indata > threshold * 35//100 and indata <= threshold * 42//100 :
            color = (102, 0, 102)
        elif indata > threshold * 42//100 and indata <= threshold * 49//100 :
            color = (153, 0, 255)
        elif indata > threshold * 49//100 and indata <= threshold * 56//100 :
            color = (102, 0, 255)
        elif indata > threshold * 56//100 and indata <= threshold * 63//100 :
            color = (51, 51, 204)   
        elif indata > threshold * 63//100 and indata <= threshold * 70//100 :
            color = (0, 102, 255)
        elif indata > threshold * 70//100 and indata <= threshold * 77//100 :
            color = (51, 153, 255)
        elif indata > threshold * 77//100 and indata <= threshold * 84//100 :
            color = (102, 204, 255)
        elif indata > threshold * 84//100:
            color = (255, 255, 255)
        else:
            pass
        yield color

# display the color on pygame window
async def display(scr):
    async for color in color_gen(threshold):
        scr.fill(color)
        pg.display.flip()

# main function obviously
async def main():
    pg.init()
    scr = pg.display.set_mode(size)
    await asyncio.gather(display(scr))

# running the main coroutine
asyncio.run(main())

