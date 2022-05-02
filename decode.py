from PIL import Image
from random import seed, randint
import ffmpeg
import ffmpy
from encode import H, gif_frame_width, gif_frame_height, n_gif_frames

ffmpeg.input('out.mp4').filter('fps', 25).output('./result_video_frames/image%d.png').overwrite_output().run()

for i in range(1, n_gif_frames):
    with Image.open(f'./result_video_frames/image{(i - 1) * H + 1}.png').convert("RGBA") as result_video_frame, Image.new("RGBA", (gif_frame_width, gif_frame_height)) as result_gif_frame:
        seed(12345)
        video_frame_width, video_frame_height = result_video_frame.size
        crc = 0.0
        hash_xy = {}
        for x_two in range(gif_frame_width):
            for y_two in range(gif_frame_height):
                while True:
                    x_one = randint(0, video_frame_width - 1)
                    y_one = randint(0, video_frame_height - 1)
                    key_xy = y_one * video_frame_width + x_one
                    if key_xy in hash_xy.keys():
                        continue
                    hash_xy[key_xy] = True
                    r, g, b, a = result_video_frame.getpixel((x_one, y_one))
                    crc += (0.2627 * r + 0.678 * g + 0.0593 * b) * key_xy
                    result_gif_frame.putpixel((x_two, y_two), (r, g, b, a))
                    break
        result_gif_frame.save(f'./result_gif_frames/image{i}.png', "PNG")

ffmpeg.input('./result_gif_frames/image%d.png', framerate=10).output('res_gif.mp4', q=0).overwrite_output().run()
ff = ffmpy.FFmpeg(
	inputs = {"res_gif.mp4" : None},
	outputs = {"res_gif.gif" : None})
ff.run()