#Author: Vansh Bhatt
#Student ID: 301471598

#Mini-Photoshop Application



# Import the required libraries
import tkinter 
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import numpy


# Global variables to store the image and its copy
img = None
original_img = None
grayimg= None
rotatedimg = None
brightness_factor = 1.0

# Function to open and display a BMP image
def open():

    global img, original_img, rotatedimg, brightness_factor
    # Open a file dialog to select a BMP file
    file = filedialog.askopenfilename(filetypes=[("BMP files", "*.bmp")])
    if file:
        # Open the image using PIL
        img = Image.open(file)
        # Keep a copy of the original image and the rotated image
        original_img = img.copy() 
        rotatedimg = img.copy() 
        # Reset the brightness factor
        brightness_factor = 1.0
        display(img)
       




#================Helper Functions================

# Function to display two images side by side
def displayside(img1, img2):

    # Create a new image with the combined width and the maximum height
    new_img = Image.new('RGB', (img1.width + img2.width, max(img1.height, img2.height)))
    # Paste the original image on the left side and the new image on the right side
    new_img.paste(img1, (0, 0))
    new_img.paste(img2, (img1.width, 0))

    photo = ImageTk.PhotoImage(new_img)
    container['image'] = photo
    container.image = photo


# Function to display a single image
def display(image):

    # Convert the PIL image to a Tkinter PhotoImage
    photo = ImageTk.PhotoImage(image)
    # Display the image in the container
    container['image'] = photo
    # Keep a reference to the image to prevent it from being garbage collected
    container.image = photo


# Function to perform the selected core operation
def core():

    # Retrieve the selected core operation from the ComboBox
    operation = coredrop.get()
    # Perform the selected operation
    if operation == "Grayscale":
        grayscale(True)
    elif operation == "Ordered Dithering":
        orddither()
    elif operation == "Auto Level":
        autolev()


# Function to perform the selected optional operation
def optional():

    # Retrieve the selected optional operation from the ComboBox
    operation = optionaldrop.get()
    # Perform the selected operation
    if operation == "Invert Colors":
        invert()
    elif operation == "Rotate 90 Degrees":
        rotate()
    elif operation == "Resize Image":
        resize()
    elif operation == "Adjust Brightness":
        brighten()





#====================Core Operations====================


# Function to convert the image to grayscale
def grayscale(toshow):

    global grayimg

    if img:
        # Convert the image to an RGB NumPy array
        pixels = numpy.array(img.convert("RGB"), dtype=numpy.float32)

        # Extract the R, G, B channels
        R = pixels[..., 0]
        G = pixels[..., 1]
        B = pixels[..., 2]

        # Compute the luminance values directly
        y = (0.299 * R + 0.587 * G + 0.114 * B).astype(numpy.uint8)

        # Create a grayscale image from the Y values
        grayimg = Image.fromarray(y)
        
        if toshow:
        # Display the original and grayscale images side by side
            displayside(original_img, grayimg)



# Function for ordered dithering using the provided algorithm
def orddither():

    global grayimg
    if img :
        # Get the grayscale image if not already done
        grayscale(False)

        # Convert grayscale image to NumPy array for pixel manipulation
        imgpixels = numpy.array(grayimg)

        # Define the 4x4 Bayer matrix for dithering
        bayermtrix = numpy.array([
            [0, 8, 2, 10],
            [12, 4, 14, 6],
            [3, 11, 1, 9],
            [15, 7, 13, 5]
        ])

        # Normalize the Bayer matrix to match grayscale pixel range [0, 255]
        bayermtrix = bayermtrix / 16.0 * 255

        # Get the dimensions of the Image matrix
        height=imgpixels.shape[0]
        width=imgpixels.shape[1]   
        # Bayer matrix size
        n = 4

        # Create an output array for the dithered image
        ditimg = numpy.zeros_like(imgpixels)

        # Apply ordered dithering algorithm
        for x in range(width):
            for y in range(height):
                i = x % n  
                j = y % n  

                # Compare pixel intensity with the Bayer matrix threshold
                if imgpixels[y, x] > bayermtrix[j, i]:
                    ditimg[y, x] = 255  
                else:
                    ditimg[y, x] = 0   

        # Convert the dithered pixel array back to an image
        ditimg = Image.fromarray(ditimg)

        # Display the original grayscale image and the dithered image side by side
        displayside(grayimg, ditimg)



# Function for auto level adjustment
def autolev():
    if img:
        
        # Convert image to a NumPy array
        pixels = numpy.array(img)
        totalpixels = pixels.size  # Total number of pixels in the image

        # Count the number of pixels for each intensity level
        Count = numpy.zeros(256, dtype=int)
        # Flatten the pixel array and count the occurrences of each intensity level
        for i in range(len(pixels.flat)):
            Count[pixels.flat[i]] += 1

        # Calculate the ideal count 
        ideal = totalpixels // 256

        # Create a new mapping for intensity levels
        stretch = numpy.zeros(256, dtype=numpy.uint8)

        # Change the intensity levels based on the ideal count
        current_level = 0
        for level in range(256):
            if Count[level] < ideal:
                # If below the ideal count, move to the next level
                current_level += 1
            stretch[level] = current_level

        # Apply the stretching to the pixels
        newimg = stretch[pixels]

        # Convert the stretched pixel array back to an image
        autolevimg = Image.fromarray(newimg)

        # Display the original image and the auto-leveled image side by side
        displayside(original_img, autolevimg)







#====================Optional Operations====================



# Optional Operation 1: Invert Colors
def invert():
    if img:
        # Convert the image to an RGB NumPy array
        pixels = numpy.array(img.convert("RGB"), dtype=numpy.uint8)

        # Invert the colors by subtracting each channel from 255
        newpix = 255 - pixels

        # Convert the inverted pixel array back to an image
        inverted_img = Image.fromarray(newpix)

        # Display the inverted image
        display(inverted_img)



# Optional Operation 2: Adjust Brightness
def brighten():
    global brightness_factor
    if img:
        # Convert the image to a NumPy array
        pixels = numpy.array(img, dtype=numpy.float32)

        # Increase the brightness factor by 10%
        brightness_factor *= 1.1

        # Apply the brightness adjustment
        bright_pixels = pixels * brightness_factor

        # Clamp pixel values to the range [0, 255] if they go out of bounds
        bright_pixels = numpy.clip(bright_pixels, 0, 255).astype(numpy.uint8)

        # Create a new image from the adjusted pixel values
        bright_img = Image.fromarray(bright_pixels)

        # Display the brightened image
        display(bright_img)


# Optional Operation 3: Rotate 90 Degrees on every click
def rotate():
    global rotatedimg
    
    if rotatedimg:
        # Rotate the image by 90 degrees
        rtimg = rotatedimg.rotate(-90, expand=True)
        # Display the rotated image
        display(rtimg)    
        # Keep track of the current image state
        rotatedimg = rtimg 

        
        
# Optional Operation 4: Resize Image to a fixed size
def resize():
    
    if img:

        # Resize to a smaller size (200x200) for simplicity
        resized_img = img.resize((200, 200))
        display(resized_img)








#====================GUI====================

# Create the main application window
root = tkinter.Tk()
root.title("Mini-Photoshop")
root.geometry("1200x800")

# Button to open a BMP file
openbutton = tkinter.Button(root, text="Open File", command=open)
openbutton.pack(pady=10)

# Dropdown for selecting core operations
coredrop = ttk.Combobox(root, values=["Core Operations","Grayscale", "Ordered Dithering", "Auto Level"], state="readonly")
coredrop.current(0) 
coredrop.pack(pady=10)

# Button to execute the selected core operation
corebutton = tkinter.Button(root, text="Perform Core Operation", command=core)
corebutton.pack(pady=10)

# Dropdown for selecting optional operations
optionaldrop = ttk.Combobox(root, values=["Optional Operations","Invert Colors", "Rotate 90 Degrees", "Resize Image", "Adjust Brightness"], state="readonly")
optionaldrop.current(0)  
optionaldrop.pack(pady=10)

# Button to execute the selected optional operation
optionalbutton= tkinter.Button(root, text="Perform Optional Operation", command=optional)
optionalbutton.pack(pady=10)

# Button to exit the application
exitbutton = tkinter.Button(root, text="Exit", command=root.quit)
exitbutton.pack(pady=10)

# Container to display the image
container = tkinter.Label(root)
container.pack(expand=True)

# Start the Tkinter event loop
root.mainloop()
