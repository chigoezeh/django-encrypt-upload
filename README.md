# Django File Upload & Encryption - RNS Trial Task

This project is a Django-based application that handles file uploads, encrypts files using **AWS KMS**, and stores the encrypted files locally. It is a trial task for the position of **Senior Backend Developer** at RNS.ID.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [AWS Setup](#aws-setup)
- [Running the Application](#running-the-application)
- [URL Structure](#url-structure)
- [License](#license)

## Prerequisites

Before setting up the project, ensure you have the following installed:

- Python 3.x
- pip (Python package manager)
- Django 3.x or newer
- Pipenv
- AWS account with KMS configured

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/chigoezeh/django-encrypt-upload.git
   cd rns_jobs
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

   **Required Packages**:

   - Django
   - boto3
   - cryptography

   Alternatively, if there is no `requirements.txt` file, you can install the dependencies individually:

   ```bash
   pip install django boto3 cryptography
   ```

3. Set up a new Django project and configure it to include the application.

## AWS Setup

To use this application in production, you'll need AWS credentials and an AWS KMS Key ID.

1. **Create an IAM user**:
   - Grant **Programmatic Access** and attach permissions for AWS KMS and S3 (if using S3 for storage).
2. **Create an AWS KMS Key**:

   - Use the AWS Management Console to create a KMS key.

3. **Add AWS credentials** to your Django project's `settings.py` file:

   ```python
   AWS_ACCESS_KEY_ID = 'your-access-key'
   AWS_SECRET_ACCESS_KEY = 'your-secret-key'
   AWS_REGION = 'your-region'
   AWS_KMS_KEY_ID = 'your-kms-key-id'
   ENCRYPTED_FILES_DIR = 'path/to/store/encrypted/files'
   ```

   Make sure to replace `'your-access-key'`, `'your-secret-key'`, `'your-region'`, and `'your-kms-key-id'` with your actual AWS credentials.

## Running the Application

1. **Start the Django development server**:

   ```bash
   python manage.py runserver
   ```

2. **Access the application**:
   - Go to `http://localhost:8000/trial_task/` to access the file upload interface.
3. **File Upload**:
   - Upload a file, and it will be encrypted using AWS KMS.

## URL Structure

The project uses the following URL structure:

- **Upload Page**: `/upload/` - The page where users can upload files.
- **API Endpoint**: `/process-upload/` - The endpoint that handles file uploads and encryption.

### Example URL Configuration (`urls.py`):

```python
from django.urls import path
from .views import process_uploaded_file

urlpatterns = [
    path('upload/', process_uploaded_file, name='upload'),
]
```

## Directory Structure

This project saves files to the local file system. You can configure the directory for encrypted files in the `settings.py` file using the `ENCRYPTED_FILES_DIR` setting:

```python
ENCRYPTED_FILES_DIR = 'path/to/your/encrypted/files'
```

The project will automatically create two directories:

- One for the encrypted files.
- Another for storing the encryption keys.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
