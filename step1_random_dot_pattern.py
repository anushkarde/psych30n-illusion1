"""
Step 1: Generate and display the random dot pattern
This creates the base random dots before any stereoscopic displacement
"""
import numpy as np
from PIL import Image

def generate_random_dots(width=800, height=600, dot_density=0.5):
    """
    Generate a random dot pattern.
    
    Parameters:
    - width: Image width in pixels
    - height: Image height in pixels
    - dot_density: Probability of placing a dot (0.0-1.0)
    
    Returns:
    - PIL Image object (grayscale)
    """
    # Create grayscale image
    img_array = np.zeros((height, width), dtype=np.uint8)
    
    # Place random dots
    for y in range(height):
        for x in range(width):
            if np.random.random() < dot_density:
                # Random brightness for each dot
                brightness = int(np.random.random() * 255)
                img_array[y, x] = brightness
    
    return Image.fromarray(img_array, mode='L')

if __name__ == "__main__":
    # Generate random dot pattern
    random_dots = generate_random_dots(
        width=800,
        height=600,
        dot_density=0.5
    )
    
    # Save the image
    random_dots.save("step1_random_dots.png")
    print("✓ Random dot pattern saved as 'step1_random_dots.png'")
    
    # Display the image
    random_dots.show()