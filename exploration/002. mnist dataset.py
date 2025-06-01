import json
import os

from torchvision import datasets, transforms


def download_and_save_mnist_samples(num_samples_per_class=5, save_dir='mnist_png_samples'):
    """
    Downloads the MNIST dataset and saves a specified number of PNG image
    samples for each class.

    Args:
        num_samples_per_class (int): Number of images to save for each digit.
        save_dir (str): The directory where the PNG images will be saved.
                         A subdirectory for each class will be created.
    """
    resume = []

    # Create the main save directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"Created directory: {save_dir}")

    # Download MNIST dataset
    print("Downloading MNIST dataset...")
    # Using a simple transform to convert images to tensors
    # MNIST images are 28x28 grayscale
    transform = transforms.ToTensor()
    
    # Download the training dataset
    mnist_trainset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    print("MNIST dataset downloaded successfully.")

    # Data loader to iterate through the dataset
    # We don't need a complex data loader, just iterating through the set is fine
    
    # Keep track of saved images for each class
    saved_counts = {i: 0 for i in range(10)} # For digits 0-9
    class_dirs = {}

    # Create subdirectories for each class
    for i in range(10):
        class_dir = os.path.join(save_dir, str(i))
        if not os.path.exists(class_dir):
            os.makedirs(class_dir)
        class_dirs[i] = class_dir
        print(f"Created directory for class {i}: {class_dir}")

    print(f"\nSaving {num_samples_per_class} samples for each class...")
    # Iterate through the dataset
    for i in range(len(mnist_trainset)):
        image_tensor, label = mnist_trainset[i] # image_tensor is a CxHxW tensor, label is an int

        if saved_counts[label] < num_samples_per_class:
            # Convert tensor to PIL Image
            # The tensor is (1, 28, 28) for grayscale.
            # We need to remove the channel dimension for PIL Image.
            # Also, scale from [0, 1] to [0, 255] if necessary (ToTensor already does this scale).
            image_pil = transforms.ToPILImage()(image_tensor) # This handles normalization if any

            # Define filename: e.g., class_0_sample_1.png
            filename = f"class_{label}_sample_{saved_counts[label] + 1}.png"
            filepath = os.path.join(class_dirs[label], filename)

            # Save the image
            image_pil.save(filepath)
            resume.append({
                'filename': filename,
                'label': label,
                'filepath': filepath
            })
            # print(f"Saved: {filepath}") # Uncomment for verbose output

            saved_counts[label] += 1

        # Check if we have saved enough samples for all classes
        if all(count >= num_samples_per_class for count in saved_counts.values()):
            print("\nAll required samples have been saved.")
            break
    
    if not all(count >= num_samples_per_class for count in saved_counts.values()):
        print("\nFinished iterating through the dataset.")
        for i in range(10):
            print(f"Saved {saved_counts[i]}/{num_samples_per_class} for class {i}.")
    
    # Save resume
    resume_file = os.path.join(save_dir, 'resume.json')
    with open(resume_file, 'w') as f:
        json.dump(resume, f, indent=4)

if __name__ == '__main__':
    # --- Configuration ---
    NUMBER_OF_SAMPLES_PER_DIGIT = 10  # How many images to save for each digit (0-9)
    OUTPUT_DIRECTORY = 'static/data/mnist' # Main directory to store the PNGs
    # -------------------

    download_and_save_mnist_samples(
        num_samples_per_class=NUMBER_OF_SAMPLES_PER_DIGIT,
        save_dir=OUTPUT_DIRECTORY
    )
    print(f"\nProcess complete. Images saved in '{OUTPUT_DIRECTORY}' directory, sorted by class.")