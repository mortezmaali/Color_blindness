import cv2
import numpy as np

# Function to simulate color blindness by applying a color transformation matrix
def simulate_color_blindness(img, cb_type):
    if cb_type == "protanope":
        transform_matrix = np.array([[0.567, 0.433, 0],
                                     [0.558, 0.442, 0],
                                     [0, 0.242, 0.758]])
    elif cb_type == "deuteranope":
        transform_matrix = np.array([[0.625, 0.375, 0],
                                     [0.7, 0.3, 0],
                                     [0, 0.3, 0.7]])
    elif cb_type == "tritanope":
        transform_matrix = np.array([[0.95, 0.05, 0],
                                     [0, 0.433, 0.567],
                                     [0, 0.475, 0.525]])
    else:
        return img
    
    return cv2.transform(img, transform_matrix)

# Function to add text with a dark edge (outline) to the image
def add_text_with_outline(img, text, position, font_scale=3, color=(255, 255, 255), thickness=5, outline_thickness=10):
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Add dark outline
    cv2.putText(img, text, position, font, font_scale, (0, 0, 0), outline_thickness, lineType=cv2.LINE_AA)
    
    # Add main text on top of the outline
    return cv2.putText(img, text, position, font, font_scale, color, thickness, lineType=cv2.LINE_AA)

# Function to create the Macbeth ColorChecker image
def create_macbeth_colorchecker():
    color_patches = [
        (115, 82, 68),  (194, 150, 130), (98, 122, 157),  (87, 108, 67),   (133, 128, 177), (103, 189, 170),
        (214, 126, 44), (80, 91, 166),   (193, 90, 99),   (94, 60, 108),   (157, 188, 64),  (224, 163, 46),
        (56, 61, 150),  (70, 148, 73),   (175, 54, 60),   (231, 199, 31),  (187, 86, 149),  (8, 133, 161),
        (243, 243, 242), (200, 200, 200), (160, 160, 160), (122, 122, 121), (85, 85, 85),   (52, 52, 52)
    ]
    
    rows, cols = 4, 6
    patch_size = 100
    macbeth_image = np.zeros((rows * patch_size, cols * patch_size, 3), dtype=np.uint8)
    
    for i in range(rows):
        for j in range(cols):
            color = color_patches[i * cols + j]
            macbeth_image[i * patch_size:(i + 1) * patch_size, j * patch_size:(j + 1) * patch_size] = color
    
    return macbeth_image

# Function to display the video with labels and simulations
def display_color_blindness_video_with_labels(image, screen_width, screen_height, duration=8):
    img = cv2.resize(image, (screen_width, screen_height))
    
    fps = 30
    text_position = (50, screen_height - 150)  # Adjusted position to make text appear higher
    
    # Normal vision
    img_normal = add_text_with_outline(img.copy(), "Normal Vision", text_position)
    frames = [img_normal] * (fps * duration)
    
    # Protanopia simulation
    img_protanope = simulate_color_blindness(img, "protanope")
    img_protanope = add_text_with_outline(img_protanope, "Protanopia", text_position)
    frames += [img_protanope] * (fps * duration)
    
    # Deuteranopia simulation
    img_deuteranope = simulate_color_blindness(img, "deuteranope")
    img_deuteranope = add_text_with_outline(img_deuteranope, "Deuteranopia", text_position)
    frames += [img_deuteranope] * (fps * duration)
    
    # Tritanopia simulation
    img_tritanope = simulate_color_blindness(img, "tritanope")
    img_tritanope = add_text_with_outline(img_tritanope, "Tritanopia", text_position)
    frames += [img_tritanope] * (fps * duration)
    
    # Display the video
    for frame in frames:
        cv2.imshow('Color Blindness Simulation', frame)
        if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

# Screen resolution
screen_width = 1920
screen_height = 1080

# Create the Macbeth ColorChecker image
macbeth_image = create_macbeth_colorchecker()

# Display the video
display_color_blindness_video_with_labels(macbeth_image, screen_width, screen_height)
