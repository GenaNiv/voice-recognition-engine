# Speaker Recognition Engine

The Speaker Recognition Engine is a command-line tool for managing speaker audio data. It supports the following functionalities:
- Enrolling new speakers
- Recognizing speakers from audio samples
- Listing all enrolled speakers
- Deleting speaker records

The engine leverages machine learning techniques, specifically Gaussian Mixture Models (GMM), 
to perform accurate and robust speaker identification.

## Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your_username/your_repository_name.git
   cd your_repository_name```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt```

3. **Verify the Installation**
   ```bash
   python cli.py --help```