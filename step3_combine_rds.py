"""
Step 3: Generate the final combined RDS (anaglyph stereogram)
This combines the left and right eye images into a single image
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

def generate_combined_rds(width=800, height=600, depth_scale=20, dot_density=0.5):
    """
    Generate the final combined RDS anaglyph image.
    
    This combines both eye views into a single image:
    - Red channel contains the left eye view (shifted left)
    - Green/Blue channels contain the right eye view (shifted right)
    
    When viewed with red-cyan glasses, each eye sees only its corresponding view,
    and the brain interprets the disparity as depth.
    
    Parameters:
    - width: Image width in pixels
    - height: Image height in pixels
    - depth_scale: Amount of depth displacement (0-50)
    - dot_density: Probability of placing a dot (0.0-1.0)
    
    Returns:
    - PIL Image object (RGB)
    """
    # Create depth map
    depth_map = create_star_depth_map(width, height)
    
    # Create RGB image array
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Generate random dots with stereoscopic displacement
    for y in range(height):
        for x in range(width):
            if np.random.random() < dot_density:
                brightness = int(np.random.random() * 255)
                depth = depth_map[y, x]
                shift = int(depth * depth_scale)
                
                # Red channel (left eye view) - shifted LEFT
                left_x = max(0, x - shift)
                img_array[y, left_x, 0] = brightness
                
                # Cyan channels (right eye view) - shifted RIGHT
                right_x = min(width - 1, x + shift)
                img_array[y, right_x, 1] = brightness  # Green
                img_array[y, right_x, 2] = brightness  # Blue
    
    return Image.fromarray(img_array)

if __name__ == "__main__":
    # Generate the combined RDS
    combined_rds = generate_combined_rds(
        width=800,
        height=600,
        depth_scale=20,
        dot_density=0.5
    )
    
    # Save the image
    combined_rds.save("step3_combined_rds.png")
    
    print("✓ Combined RDS saved as 'step3_combined_rds.png'")
    print("\nExplanation:")
    print("- This image contains BOTH eye views in a single image")
    print("- Red channel = left eye view (dots shifted left)")
    print("- Green+Blue channels = right eye view (dots shifted right)")
    print("- View with red-cyan 3D glasses (red lens on LEFT eye)")
    print("- Your brain will fuse the two views and perceive depth!")
    print("- The star should appear to pop OUT toward you")
    
    # Display the image
    combined_rds.show()