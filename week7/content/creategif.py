import imageio
from moviepy.editor import *

clip = (VideoFileClip("screencapture.mp4")
        .subclip((0,1),(0,36))
        .resize(0.9))
clip.write_gif("screencapture.gif")
