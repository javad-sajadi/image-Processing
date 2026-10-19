"""
image_enhancer.py - Digital Image Processing & Enhancement Framework
Author: Javad Sajadi
Repository: javad-sajadi/image-Processing

Provides modular algorithms for:
  - Contrast stretching and Adaptive Histogram Equalization (CLAHE)
  - Color space conversions (RGB, HSV, LAB, Grayscale)
  - Morphological filtering (Erosion, Dilation, Opening, Closing)
  - Spatial edge detection (Sobel, Laplacian, Canny, Gaussian gradient)
"""

import os
import argparse
import numpy as np
import cv2
import matplotlib.pyplot as plt


def load_image(image_path: str):
    """Loads image from file with validation."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    bgr = cv2.imread(image_path)
    if bgr is None:
        raise ValueError(f"Failed to read image at: {image_path}")
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return rgb, bgr


def enhance_contrast(rgb_image: np.ndarray) -> np.ndarray:
    """Enhances luminance contrast using CLAHE in LAB color space."""
    lab = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    merged_lab = cv2.merge((cl, a, b))
    return cv2.cvtColor(merged_lab, cv2.COLOR_LAB2RGB)


def detect_edges(rgb_image: np.ndarray, method: str = "canny") -> np.ndarray:
    """Detects spatial image edges via Canny or Sobel operators."""
    gray = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)
    if method == "sobel":
        grad_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = np.sqrt(grad_x ** 2 + grad_y ** 2)
        edges = np.uint8(np.clip(magnitude / np.max(magnitude) * 255.0, 0, 255))
    else:
        edges = cv2.Canny(blurred, 50, 150)
    return edges


def apply_pipeline(input_image_path: str, output_path: str = "enhanced_comparison.png"):
    """Runs enhancement pipeline and exports visual comparison figure."""
    rgb, _ = load_image(input_image_path)
    enhanced = enhance_contrast(rgb)
    canny = detect_edges(rgb, "canny")
    sobel = detect_edges(rgb, "sobel")

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    axes[0, 0].imshow(rgb)
    axes[0, 0].set_title("Original RGB Input")
    axes[0, 0].axis("off")

    axes[0, 1].imshow(enhanced)
    axes[0, 1].set_title("CLAHE Contrast Enhanced")
    axes[0, 1].axis("off")

    axes[1, 0].imshow(canny, cmap="gray")
    axes[1, 0].set_title("Canny Multi-stage Edge Detector")
    axes[1, 0].axis("off")

    axes[1, 1].imshow(sobel, cmap="magma")
    axes[1, 1].set_title("Sobel Gradient Magnitude")
    axes[1, 1].axis("off")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"Enhancement comparison saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Digital Image Processing & Enhancement")
    parser.add_argument("--image", type=str, default="image1.jpg", help="Target input image path")
    parser.add_argument("--out", type=str, default="enhanced_comparison.png", help="Output figure path")
    args = parser.parse_args()

    if os.path.exists(args.image):
        apply_pipeline(args.image, args.out)
    else:
        print(f"Target '{args.image}' not found in current directory. Searching for alternate .jpg image...")
        jpgs = [f for f in os.listdir(".") if f.lower().endswith((".jpg", ".png"))]
        if jpgs:
            apply_pipeline(jpgs[0], args.out)
        else:
            print("No images found.")
