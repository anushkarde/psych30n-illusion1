"""
Extra Credit: Generate multiple RDS images with different depth scales
This creates variations showing shallow, medium, and deep 3D effects
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

def generate_rds_with_depth(width, height, depth_scale, dot_density):
    """Generate an RDS with a specific depth scale."""
    depth_map = create_star_depth_map(width, height)
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    for y in range(height):
        for x in range(width):
            if np.random.random() < dot_density:
                brightness = int(np.random.random() * 255)
                depth = depth_map[y, x]
                shift = int(depth * depth_scale)
                
                # Left eye (red) - shifted left
                left_x = max(0, x - shift)
                img_array[y, left_x, 0] = brightness
                
                # Right eye (cyan) - shifted right
                right_x = min(width - 1, x + shift)
                img_array[y, right_x, 1] = brightness
                img_array[y, right_x, 2] = brightness
    
    return Image.fromarray(img_array)

if __name__ == "__main__":
    width, height = 800, 600
    dot_density = 0.5
    
    # Define different depth scales
    depth_variations = [
        (5, "shallow"),
        (10, "slight"),
        (20, "medium"),
        (30, "deep"),
        (40, "very_deep")
    ]
    
    print("Generating RDS variations with different depths...\n")
    
    for depth_scale, label in depth_variations:
        img = generate_rds_with_depth(width, height, depth_scale, dot_density)
        filename = f"extra_credit_depth_{label}_{depth_scale}.png"
        img.save(filename)
        print(f"✓ Generated '{filename}' with depth_scale={depth_scale}")
    
    print("\nAll variations saved!")
    print("\nDepth Scale Guide:")
    print("- 5 (shallow): Very subtle 3D effect")
    print("- 10 (slight): Noticeable but gentle depth")
    print("- 20 (medium): Clear 3D pop-out effect")
    print("- 30 (deep): Strong 3D effect")
    print("- 40 (very deep): Dramatic 3D effect (may be harder to fuse)")
    print("\nView each with red-cyan glasses to compare the depth differences!")