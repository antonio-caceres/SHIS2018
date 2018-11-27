import os
import imageio

if __name__ == "__main__":
    for file_name in os.listdir(os.getcwd() + "/data/user"):
        print(file_name)
        if file_name != '.DS_Store':
            image_input = imageio.imread("data/user/" + file_name, as_gray=True)
            print(image_input, "\n\n", [image_input])
