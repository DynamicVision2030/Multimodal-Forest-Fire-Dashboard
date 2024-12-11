import os
import pandas as pd
import random
import shutil
from PIL import Image, ImageEnhance

# Paths for your current structure
root_dir = "Sony Works"
train_csv_path = os.path.join(root_dir, "train2.csv")
test_csv_path = os.path.join(root_dir, "test2.csv")
fire_train_dir = os.path.join(root_dir, "fire", "train")
fire_test_dir = os.path.join(root_dir, "fire", "test")
nofire_train_dir = os.path.join(root_dir, "nofire", "train")
nofire_test_dir = os.path.join(root_dir, "nofire", "test")

# Functions to augment images
def augment_image(image_path):
    # Open an image file
    with Image.open(image_path) as img:
        # Randomly adjust brightness, contrast, and rotation
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(random.uniform(0.7, 1.3))

        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(random.uniform(0.8, 1.2))

        img = img.rotate(random.uniform(-10, 10))  # Slight rotation
        return img

# Function to create synthetic data
def create_synthetic_data(src_dir, dest_dir, prefix, count=100):
    image_files = [f for f in os.listdir(src_dir) if f.endswith('.jpg')]
    total_files = len(image_files)
    if total_files == 0:
        print(f"No images found in {src_dir}")
        return 0

    new_files = []
    for _ in range(count):
        original_file = random.choice(image_files)
        original_path = os.path.join(src_dir, original_file)
        
        # Augment the image
        augmented_img = augment_image(original_path)

        # Save the augmented image
        new_file_name = f"{prefix}_{random.randint(1000, 9999)}.jpg"
        new_path = os.path.join(dest_dir, new_file_name)
        augmented_img.save(new_path)
        new_files.append(new_file_name)

    return new_files

# Function to update CSV with new data
def update_csv(csv_path, data_dir, new_data, label):
    df = pd.read_csv(csv_path)

    for file_name in new_data:
        if 'fire' in data_dir:
            label_value = 1
        else:
            label_value = 0
        
        # Here you need to adjust this based on the columns you have in your CSV
        new_row = {
            'x:image': f"./{data_dir}/{file_name}",  # Update path to match your structure
            'x2:spectrogram': f"./{data_dir}/{file_name}",  # Assuming same filename for spectrogram
            'y:label;nofire;fire': label_value,
            # Include other columns if needed
        }
        df = df.append(new_row, ignore_index=True)
    
    # Save updated CSV
    df.to_csv(csv_path, index=False)

# Generate synthetic data and update CSVs
def generate_synthetic_data():
    # Define how many synthetic images you want for each category
    synthetic_count = 2500  # Adjust as needed

    # Generate for 'fire' category
    print("Generating synthetic fire images...")
    fire_train_new = create_synthetic_data(fire_train_dir, fire_train_dir, "fire", synthetic_count)
    fire_test_new = create_synthetic_data(fire_test_dir, fire_test_dir, "fire", synthetic_count // 2)

    # Update train and test CSVs for 'fire'
    update_csv(train_csv_path, "fire/train", fire_train_new, label=1)
    update_csv(test_csv_path, "fire/test", fire_test_new, label=1)

    # Generate for 'nofire' category
    print("Generating synthetic nofire images...")
    nofire_train_new = create_synthetic_data(nofire_train_dir, nofire_train_dir, "nofire", synthetic_count)
    nofire_test_new = create_synthetic_data(nofire_test_dir, nofire_test_dir, "nofire", synthetic_count // 2)

    # Update train and test CSVs for 'nofire'
    update_csv(train_csv_path, "nofire/train", nofire_train_new, label=0)
    update_csv(test_csv_path, "nofire/test", nofire_test_new, label=0)

    print("Synthetic data generation complete!")

# Run the function
generate_synthetic_data()
