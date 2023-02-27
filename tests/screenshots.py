import glob
from PIL import Image

def make_gif(images_folder, gif_file):
    images = sorted(glob.glob(f"{images_folder}/*.jpg"))
    frames = [Image.open(image) for image in images]
    frame_one = frames[0]
    frame_one.save(gif_file,
                   format="GIF",
                   append_images=frames,
                   save_all=True,
                   duration=200,
                   loop=1)

if __name__ == "__main__":
    make_gif("test/screenshots", "test/screenshots.gif")
