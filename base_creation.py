import cv2
import numpy as np
import os

# Function to split the image into 4 quadrants, apply transformations, and save them
def split_and_transform_image(image_path, output_dir):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if image is None:
        print(f"Error: Unable to load image from {image_path}")
        return

    # Replace transparent background with white
    if image.shape[2] == 4:  # Check if the image has an alpha channel
        alpha_channel = image[:, :, 3]
        _, mask = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)
        color = image[:, :, :3]
        white_background = np.ones_like(color, dtype=np.uint8) * 255
        image = cv2.bitwise_not(cv2.bitwise_not(color, mask=mask) + cv2.bitwise_not(white_background, mask=cv2.bitwise_not(mask)))

    # Get image dimensions
    height, width, _ = image.shape

    # Calculate the midpoint
    mid_x, mid_y = width // 2, height // 2

    # Define the four quadrants
    quadrants = {
        "top_left": image[0:mid_y, 0:mid_x],
        "top_right": image[0:mid_y, mid_x:width],
        "bottom_left": image[mid_y:height, 0:mid_x],
        "bottom_right": image[mid_y:height, mid_x:width]
    }

    # Apply transformations and save each quadrant
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for name, quadrant in quadrants.items():
        if name == "top_left":
            # Mirror horizontally
            quadrant = cv2.flip(quadrant, 1)
        elif name == "top_right":
            # No mirroring needed
            pass
        elif name == "bottom_left":
            # Mirror both vertically and horizontally
            quadrant = cv2.flip(quadrant, -1)
        elif name == "bottom_right":
            # Mirror vertically
            quadrant = cv2.flip(quadrant, 0)

        output_path = os.path.join(output_dir, f"{name}.png")
        cv2.imwrite(output_path, quadrant)
        print(f"Saved {name} quadrant to {output_path}")

# Path to the input image
image_path = '/tests/dcode-9999.png'

# Directory to save the quadrants
output_dir = '/Users/diegosiqueira/Playground/numbers/out'

# Split, transform, and save the image
split_and_transform_image(image_path, output_dir)
# Path to the input image
