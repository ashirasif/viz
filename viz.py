import sounddevice as sd
import asyncio
import pygame as pg
import sys

size = (1920, 1080)
threshold = int(sys.argv[1])
fps = int(sys.argv[2])

# variable of sounddevice

sd.default.samplerate = 22050
block = sd.default.samplerate // fps

async def inputstream_generator(block, channels=1, **kwargs):
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

async def display(scr):
    async for color in color_gen(threshold):
        scr.fill(color)
        pg.display.flip()

async def main():
    pg.init()
    scr = pg.display.set_mode(size)
    await asyncio.gather(display(scr))

asyncio.run(main())

