# 🎥 Python Media Converter Pro

A modern, lightweight, and safe batch media converter built with Python. This tool allows you to convert videos and images in bulk using a clean **Dark Mode GUI**.

It supports smart filtering (e.g., "Only convert `.mov` files") and creates a backup of processed files instead of deleting them, ensuring no data loss.

## ✨ Features

- **🌑 Modern Dark Mode GUI:** Easy on the eyes, built with standard `tkinter` but styled for a professional look.
- **🔄 Batch Processing:** Select a folder and convert hundreds of files at once.
- **🎯 Smart Filtering:** - Choose a specific source format (e.g., only convert `.mov` to `.mp4`).
  - Or select `* (All)` to convert every supported media file found.
- **🛡️ Non-Destructive Workflow:** Original files are **not** deleted. Upon successful conversion, they are safely moved to a subfolder named `_ERLEDIGT` (Done).
- **📦 Supported Formats:**
  - **Video:** MP4, MOV, WEBM, AVI, MKV, GIF
  - **Image:** JPG, PNG, WEBP, BMP, HEIC (input only)

## 🛠️ Prerequisites

You need to have Python installed on your system.
This project relies on two powerful libraries:
- **MoviePy** (for video processing)
- **Pillow** (for image processing)

## 🚀 Installation

1. **Clone the repository**
    ```bash
    git clone [https://github.com/phillipp-schlueter/python-media-converter.git](https://github.com/phillipp-schlueter/python-media-converter.git)
    cd python-media-converter
    ```
2. **Install dependencies**
    pip install -r requirements.txt
3. **Usage**
    - Run the Program
    - Select Source Folder
    - Choose Formats: Select the file type you want to convert (Source - Left), then select the desired output format (Target - Right).
    - Check "Move originals to '_ERLEDIGT'" to clean up your folder automatically after conversion.
    - Click the "START CONVERSION" button and watch the progress bar.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://www.google.com/search?q=https://github.com/phillipp-schlueter/python-media-converter/issues).

## 📝 License
Distributed under the MIT License. See LICENSE for more information.