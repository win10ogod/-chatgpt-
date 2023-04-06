from tkinter import Tk, Label, Button, filedialog, Checkbutton, IntVar
from PIL import Image
import os
import gzip

def convert_images():
    # Get the path of the folder containing the images
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select folder containing images")

    # Determine whether to include grayscale values
    grayscale = grayscale_var.get()

    # Determine whether to convert the pixel sequence to characters
    convert_to_chars = chars_var.get()

    # Convert each image to a pixel sequence
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            with Image.open(image_path) as image:
                if grayscale:
                    image = image.convert('L')
                pixels = list(image.getdata())

            # Convert the pixel sequence to characters if desired
            if convert_to_chars:
                char_pixels = [char_map[int(p/255*len(char_map))] for p in pixels]
                pixels = char_pixels

            # Save the pixel sequence as a text file
            output_path = os.path.join(folder_path, f"{filename.split('.')[0]}.txt")
            if compress_var.get():
                output_path += ".gz"
                with gzip.open(output_path, 'wb') as file:
                    file.write(bytes(str(pixels), 'utf-8'))
            else:
                with open(output_path, 'w') as file:
                    file.write(str(pixels))

    # Display a message when the conversion is complete
    message_label.config(text="Conversion complete!")

# Create a GUI window
window = Tk()
window.title("Image Converter")

# Create a label and a button
title_label = Label(window, text="Image Converter")
title_label.pack()

convert_button = Button(window, text="Convert Images", command=convert_images)
convert_button.pack()

message_label = Label(window, text="")
message_label.pack()

# Create checkboxes for additional options
grayscale_var = IntVar()
grayscale_check = Checkbutton(window, text="Include grayscale values", variable=grayscale_var)
grayscale_check.pack()

chars_var = IntVar()
chars_check = Checkbutton(window, text="Convert pixel sequence to characters", variable=chars_var)
chars_check.pack()

char_map = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']

compress_var = IntVar()
compress_check = Checkbutton(window, text="Compress output files", variable=compress_var)
compress_check.pack()

# Run the GUI
window.mainloop()
