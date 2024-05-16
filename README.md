# Newspaper Question Answering (NQA) backend

## Description

The Newspaper Question Answering (NQA) backend is a crucial component of a system designed to provide answers to questions within the given newspaper's domain. This backend is responsible for processing and analyzing the textual content of newspaper , extracting relevant information, storing it,and generating accurate responses to user queries.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You need to have Python 3.11 installed on your machine.

## Installation

Follow these steps to get started with the project:

### Step 1: Install Python 3.11

1. **Download Python 3.11**: Visit the official [Python website](https://www.python.org/downloads/) and download the installer for Python 3.11 suitable for your operating system.

2. **Install Python 3.11**: Run the installer and follow the on-screen instructions. Make sure to add Python to your PATH during the installation process.

3. **Verify Installation**: Open a terminal or command prompt and run the following command to verify the installation:

   ```sh
   python --version
   ```

   You should see an output like `Python 3.11.x`, indicating that Python 3.11 is successfully installed.

### Step 2: Set Up the Project

1. **Clone the repository**: If you haven't already, clone this repository to your local machine:

   ```sh
   git clone "this repository link"
   ```

2. **Navigate to the project directory**:

   ```sh
   cd src_nqa_backend
   ```

3. **Run the setup script** using Python 3.11:

   > **Note**: This will do most of the work. **Skip this step** if you want to setup things manually

   ```sh
   python setup.py
   ```

### Step 3: Create and Activate Virtual Environment

1. **Create a virtual environment** named `nqa_venv`:

   ```sh
   python -m venv nqa_venv
   ```

2. **Deactivate any active virtual environment** (if applicable):

   ```sh
   deactivate
   ```

3. **Activate the virtual environment**:

   - On Windows:

     ```sh
     .\nqa_venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```sh
     source nqa_venv/bin/activate
     ```

4. **Install the required packages**:

   ```sh
   pip install -r requirements.txt
   ```

   > **Note**: Only if your pip installation is successful, then run the below command!

### Step 5: Download Tesseract and install it in the ocr_engine directory

1. It should be stored like :

   ```sh
   ./ocr_engine/teseract/
                        |--> doc/
                        |--> tessdata/
                        |--> *.html
                        |--> *.exe (if windows)
                        |--> *.out (if linux)
                        |--> *.dll
   ```

2. **Note**: Only if you are a linux user go to environment folder/config.json:

   ```sh
      Change
         "OcrEnginePath": "./ocr_engine/tesseract/tesseract.exe"
      to
         "OcrEnginePath": "./ocr_engine/tesseract/tesseract.out"
   ```

### Step 6: Run the Application

1. **Navigate to the directory** containing `app.py` (if not already in the correct directory):

   ```sh
   cd src_nqa_backend
   ```

2. **To Run `app.py`** using the virtual environment:

   ```sh
   uvicorn app:app
   ```

## Usage

Provide instructions on how to use the project after installation. This could include examples of commands to run or a brief guide on how to operate the software.

## Contributing

If you want to contribute to this project, please follow the standard procedures for contributing:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Create a pull request.

## License

This project uses the following license: [MIT License](LICENSE).

## Contact

If you have any questions, please feel free to contact us at [aadityaprabu@gmail.com].

---
