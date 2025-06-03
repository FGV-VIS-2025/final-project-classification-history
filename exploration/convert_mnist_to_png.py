import os
from mnist import MNIST # Uses python-mnist library
from PIL import Image
import numpy as np

def save_mnist_as_png(dataset_type, images, labels, output_dir_base, num_images_per_class=50):
    """
    Saves a subset of MNIST images as PNG files.

    Args:
        dataset_type (str): 'train' or 'test'.
        images (list): List of MNIST image data (flattened lists or numpy arrays).
        labels (list): List of MNIST labels.
        output_dir_base (str): The base directory to save images (e.g., '../public/mnist_pngs').
        num_images_per_class (int): Number of images to save for each class.
    """
    print(f"Processing {dataset_type} dataset...")
    # Create base directory if it doesn't exist
    os.makedirs(output_dir_base, exist_ok=True)

    output_dir = os.path.join(output_dir_base, dataset_type)
    os.makedirs(output_dir, exist_ok=True)

    # Create subdirectories for each class (0-9)
    for i in range(10):
        os.makedirs(os.path.join(output_dir, str(i)), exist_ok=True)

    # Keep track of how many images we've saved for each class
    saved_counts = {i: 0 for i in range(10)}
    total_saved = 0

    for i, (image_data, label) in enumerate(zip(images, labels)):
        if saved_counts[label] < num_images_per_class:
            try:
                # MNIST images are 28x28. python-mnist provides them as flat lists.
                # Reshape to 28x28 numpy array
                image_np = np.array(image_data, dtype=np.uint8).reshape(28, 28)
                img = Image.fromarray(image_np, 'L') # 'L' mode for grayscale

                # Define filename, e.g., image_0001.png
                filename = f"image_{saved_counts[label]:04d}.png"
                filepath = os.path.join(output_dir, str(label), filename)
                img.save(filepath)

                saved_counts[label] += 1
                total_saved += 1
                if i % 1000 == 0:
                    print(f"  Processed {i}/{len(images)} images from source...")

            except Exception as e:
                print(f"Error saving image {i} for label {label}: {e}")

        # Check if we have saved enough images for all classes
        if all(count >= num_images_per_class for count in saved_counts.values()):
            print(f"Saved required {num_images_per_class} images for all classes in {dataset_type} set.")
            break
    
    print(f"Finished processing {dataset_type}. Total images saved: {total_saved}")


if __name__ == "__main__":
    # --- Configuration ---
    # Path to where your MNIST data is located
    mnist_data_path = './mnist_data_raw'
    # Base output directory for PNGs (relative to this script's location)
    # This will place them in cnn-explainer/public/mnist_pngs
    png_output_dir = os.path.join('..', 'public', 'mnist_pngs')
    
    # Number of images to save per digit (0-9) for train and test sets
    NUM_IMAGES_PER_CLASS_TRAIN = 50 
    NUM_IMAGES_PER_CLASS_TEST = 20

    print("Starting MNIST to PNG conversion...")

    # Ensure the directory for raw MNIST data exists (it should if files are there)
    if not os.path.isdir(mnist_data_path):
        print(f"Error: MNIST data directory not found at {os.path.abspath(mnist_data_path)}")
        print("Please ensure the manually downloaded MNIST files are in this directory.")
        exit()
    
    # Load MNIST data using python-mnist
    try:
        print(f"Loading MNIST data from: {os.path.abspath(mnist_data_path)}")
        mndata = MNIST(mnist_data_path)
        # Set gz to False because your files do not have the .gz extension
        mndata.gz = False 
        
        train_images, train_labels = mndata.load_training()
        test_images, test_labels = mndata.load_testing()
        print("MNIST data loaded successfully.")
        
    except Exception as e:
        print(f"Could not load MNIST data. Error: {e}")
        print(f"Please ensure the uncompressed MNIST files (e.g., 'train-images-idx3-ubyte')")
        print(f"are correctly placed in the directory: {os.path.abspath(mnist_data_path)}")
        exit()

    # Save training images
    save_mnist_as_png('train', train_images, train_labels, png_output_dir, NUM_IMAGES_PER_CLASS_TRAIN)

    # Save testing images
    save_mnist_as_png('test', test_images, test_labels, png_output_dir, NUM_IMAGES_PER_CLASS_TEST)

    print("-----------------------------------------------------------------")
    print(f"MNIST to PNG conversion complete!")
    print(f"PNG images saved in: {os.path.abspath(png_output_dir)}")
    print(f"  - Training images: {NUM_IMAGES_PER_CLASS_TRAIN} per class.")
    print(f"  - Testing images:  {NUM_IMAGES_PER_CLASS_TEST} per class.")
    print("-----------------------------------------------------------------")
