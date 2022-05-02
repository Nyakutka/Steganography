from PIL import Image
from random import seed, randint
from pathlib import Path
import ffmpeg

ffmpeg.input('giphy.gif').filter('scale', 200, 200).output('./gif_frames/image%d.png').overwrite_output().run()
ffmpeg.input('video.mp4').filter('fps', 25).output('./video_frames/image%d.png').overwrite_output().run()

gif_frames_folder = Path('./gif_frames')
video_frames_folder = Path('./video_frames')
n_gif_frames = len(list(gif_frames_folder.iterdir()))
n_video_frames = len(list(video_frames_folder.iterdir()))
H = n_video_frames // n_gif_frames

gif_frame_width = gif_frame_height = 200
for i in range(1, n_gif_frames):
    with Image.open(f'./video_frames/image{(i - 1) * H + 1}.png').convert("RGBA") as video_frame, Image.open(f'./gif_frames/image{i}.png').convert("RGBA") as gif_frame:
        seed(12345)
        vid_frame_width, vid_frame_height = video_frame.size
        crc = 0.0
        hash_xy = {}
        for gif_frame_x in range(gif_frame_width):
            for gif_frame_y in range(gif_frame_height):
                r, g, b, a = gif_frame.getpixel((gif_frame_x, gif_frame_y))
                while True:
                    x_one = randint(0, vid_frame_width - 1)
                    y_one = randint(0, vid_frame_height - 1)
                    key_xy = y_one * vid_frame_width + x_one
                    if key_xy in hash_xy.keys():
                        continue
                    crc += (0.2627 * r + 0.678 * g + 0.0593 * b) * key_xy
                    hash_xy[key_xy] = True
                    video_frame.putpixel((x_one, y_one), (r, g, b, a))
                    break

        video_frame.save(f'./video_frames/image{(i - 1) * H + 1}.png', "PNG")

ffmpeg.input('./video_frames/image%d.png', framerate=25).output('out.mp4', q=0).overwrite_output().run()