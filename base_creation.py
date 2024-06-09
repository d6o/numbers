import cv2
import os


# Function to split the image into 4 quadrants, apply transformations, and save them
def split_and_transform_image(image_path, output_dir):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if image is None:
        print(f"Error: Unable to load image from {image_path}")
        return

    # Get image dimensions
    height, width = image.shape

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
image_path = '/Users/diegosiqueira/Playground/numbers/output.png'

# Directory to save the quadrants
output_dir = '/Users/diegosiqueira/Playground/numbers/out'

# Split, transform, and save the image
split_and_transform_image(image_path, output_dir)
# Path to the input image
