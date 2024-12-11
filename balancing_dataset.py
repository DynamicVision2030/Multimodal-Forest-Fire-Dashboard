import os
import pandas as pd
import random
from PIL import Image, ImageEnhance

# Paths for your current structure - use absolute paths if needed
root_dir = "/home/kl/Downloads/Sony"  # Change this to the absolute path if needed
train_csv_path = os.path.join(root_dir, "train3.csv")
test_csv_path = os.path.join(root_dir, "test3.csv")
fire_train_dir = os.path.join(root_dir, "fire", "train")
fire_test_dir = os.path.join(root_dir, "fire", "test")
nofire_train_dir = os.path.join(root_dir, "nofire", "train")
nofire_test_dir = os.path.join(root_dir, "nofire", "test")
nofire_mapping_file = os.path.join(root_dir, "nofire_mapping.csv")  # Mapping file path

# Load the nofire mapping if it exists
if os.path.exists(nofire_mapping_file):
    nofire_mapping = pd.read_csv(nofire_mapping_file)
else:
    raise FileNotFoundError(f"Mapping file not found: {nofire_mapping_file}")

# Functions to augment images
def augment_image(image_path):
    with Image.open(image_path) as img:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(random.uniform(0.7, 1.3))

        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(random.uniform(0.8, 1.2))

        img = img.rotate(random.uniform(-10, 10))  # Slight rotation
        return img

# Functions to augment spectrograms
def augment_spectrogram(spectrogram_path):
    with Image.open(spectrogram_path) as img:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(random.uniform(0.8, 1.2))

        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(random.uniform(0.8, 1.2))

        img = img.transform(
            img.size, Image.AFFINE, (1, 0, random.randint(-10, 10), 0, 1, random.randint(-5, 5))
        )
        return img

# Function to generate weather data
def generate_weather_data(label):
    if label == 1:  # Fire data
        temperature = random.randint(35, 50)  # Higher temperatures for fire
        humidity = random.randint(10, 40)     # Lower humidity for fire
    else:  # No fire data
        temperature = random.randint(20, 30)  # Lower temperatures for no fire
        humidity = random.randint(50, 70)     # Higher humidity for no fire
    return temperature, humidity

# Function to generate social media data
def generate_social_media_data(label):
    fire_keywords = ["fire", "smoke", "burn", "flames"]
    no_fire_keywords = ["clear weather", "calm", "none"]
    if label == 1:  # Fire data
        return random.choice(fire_keywords)
    else:  # No fire data
        return random.choice(no_fire_keywords)

# Function to create synthetic data for both images and spectrograms
def create_synthetic_data(src_dir, dest_dir, prefix, count=100, is_fire=True):
    if not os.path.exists(src_dir):
        print(f"Source directory does not exist: {src_dir}")
        return []

    image_files = [f for f in os.listdir(src_dir) if f.endswith('.jpg')]
    total_files = len(image_files)
    if total_files == 0:
        print(f"No images found in {src_dir}")
        return []

    new_files = []
    for _ in range(count):
        original_file = random.choice(image_files)
        original_path = os.path.join(src_dir, original_file)

        if is_fire:
            # Fire category, using the same number for spectrogram
            spectrogram_number = original_file.split('_')[-1].replace('.jpg', '')
            original_spectrogram_path = os.path.join(src_dir, f"{spectrogram_number}.png")
        else:
            # No fire category, use mapping file
            matching_row = nofire_mapping[nofire_mapping['image'] == original_file]
            if matching_row.empty:
                print(f"No matching spectrogram found for {original_file}. Skipping.")
                continue
            spectrogram_file = matching_row['spectrogram'].values[0]
            original_spectrogram_path = os.path.join(src_dir, spectrogram_file)

        # Augment image and spectrogram
        augmented_img = augment_image(original_path)
        augmented_spectrogram = augment_spectrogram(original_spectrogram_path)

        # Save augmented data
        new_file_base = f"{prefix}_{random.randint(1000, 9999)}"
        new_img_path = os.path.join(dest_dir, new_file_base + ".jpg")
        new_spectrogram_path = os.path.join(dest_dir, new_file_base + ".png")
        augmented_img.save(new_img_path)
        augmented_spectrogram.save(new_spectrogram_path)
        new_files.append((new_img_path, new_spectrogram_path))

    return new_files

# Function to update CSV with new data including weather and social media
def update_csv(csv_path, data_dir, new_data, label):
    df = pd.read_csv(csv_path)

    new_rows = []
    for img_path, spec_path in new_data:
        temperature, humidity = generate_weather_data(label)
        social_media_keyword = generate_social_media_data(label)
        
        new_row = {
            'x:image': img_path,
            'x2:spectrogram': spec_path,
            'y:label;nofire;fire': label,
            'temperature': temperature,
            'humidity': humidity,
            'social_media_keywords': social_media_keyword,
        }
        new_rows.append(new_row)
    
    new_df = pd.DataFrame(new_rows)
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(csv_path, index=False)

# Generate synthetic data and update CSVs
def generate_synthetic_data():
    current_train_df = pd.read_csv(train_csv_path)
    current_no_fire_count = current_train_df[current_train_df['y:label;nofire;fire'] == 0].shape[0]
    current_fire_count = current_train_df[current_train_df['y:label;nofire;fire'] == 1].shape[0]
    additional_count = current_fire_count - current_no_fire_count

    synthetic_count = additional_count

    print(f"Generating {synthetic_count} synthetic 'nofire' images and spectrograms...")

    nofire_train_new = create_synthetic_data(nofire_train_dir, nofire_train_dir, "nofire", synthetic_count, is_fire=False)
    nofire_test_new = create_synthetic_data(nofire_test_dir, nofire_test_dir, "nofire", synthetic_count // 2, is_fire=False)

    update_csv(train_csv_path, "nofire/train", nofire_train_new, label=0)
    update_csv(test_csv_path, "nofire/test", nofire_test_new, label=0)

    print("Synthetic data generation complete!")

# Run the function
generate_synthetic_data()
