"""
Step 2: Generate separate left eye (red) and right eye (cyan) images
This shows how the stereoscopic effect is created by shifting dots based on depth
"""
import numpy as np
from PIL import Image
import math

def create_star_depth_map(width, height):
    """Create a depth map with a 5-pointed star shape."""
    depth_map = np.zeros((height, width))
    center_x, center_y = width / 2, height / 2
    outer_radius = min(width, height) / 4
    inner_radius = outer_radius * 0.4
    
    for y in range(height):
        for x in range(width):
            dx = x - center_x
            dy = y - center_y
            distance = math.sqrt(dx * dx + dy * dy)
            angle = math.atan2(dy, dx)
            
            # Create 5-pointed star
            star_angle = (angle + math.pi / 2) % (2 * math.pi / 5)
            star_radius = inner_radius + (outer_radius - inner_radius) * \
                (0.5 + 0.5 * math.cos(5 * star_angle))
            
            # Check if point is inside star
            if distance < star_radius:
                depth_map[y, x] = 1 - (distance / star_radius) * 0.5
            else:
                depth_map[y, x] = 0
    
    return depth_map

def generate_eye_images(width=800, height=600, depth_scale=20, dot_density=0.5):
    """
    Generate separate left eye (red) and right eye (cyan) images.
    
    The key concept:
    - Left eye image: dots shifted LEFT based on depth (red channel)
    - Right eye image: dots shifted RIGHT based on depth (cyan channels)
    - The disparity between these creates the 3D effect
    
    Parameters:
    - width: Image width in pixels
    - height: Image height in pixels
    - depth_scale: How much displacement (0-50)
    - dot_density: Probability of placing a dot (0.0-1.0)
    
    Returns:
    - Tuple of (left_eye_img, right_eye_img) as PIL Images
    """
    # Create depth map
    depth_map = create_star_depth_map(width, height)
    
    # Initialize arrays for left and right eye
    left_array = np.zeros((height, width, 3), dtype=np.uint8)
    right_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Generate dots with depth-based displacement
    for y in range(height):
        for x in range(width):
            if np.random.random() < dot_density:
                brightness = int(np.random.random() * 255)
                depth = depth_map[y, x]
                shift = int(depth * depth_scale)
                
                # Left eye sees red, shifted LEFT (negative direction)
                left_x = max(0, x - shift)
                left_array[y, left_x, 0] = brightness  # Red channel only
                
                # Right eye sees cyan, shifted RIGHT (positive direction)
                right_x = min(width - 1, x + shift)
                right_array[y, right_x, 1] = brightness  # Green channel
                right_array[y, right_x, 2] = brightness  # Blue channel
    
    return Image.fromarray(left_array), Image.fromarray(right_array)

if __name__ == "__main__":
    # Generate left and right eye images
    left_img, right_img = generate_eye_images(
        width=800,
        height=600,
        depth_scale=20,
        dot_density=0.5
    )
    
    # Save the images
    left_img.save("step2_left_eye_red.png")
    right_img.save("step2_right_eye_cyan.png")
    
    print("✓ Left eye image (red) saved as 'step2_left_eye_red.png'")
    print("✓ Right eye image (cyan) saved as 'step2_right_eye_cyan.png'")
    print("\nExplanation:")
    print("- Left eye image shows red dots shifted LEFT based on depth")
    print("- Right eye image shows cyan dots shifted RIGHT based on depth")
    print("- Where the star is (high depth), dots are shifted MORE")
    print("- Background (zero depth) has no shift")
    
    # Display the images
    left_img.show()
    right_img.show()