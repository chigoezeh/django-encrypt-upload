from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.conf import settings
import boto3
#from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Create your views here.

# Set up KMS client
kms_client = boto3.client(
    'kms',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

# We need to check and be sure directories exit.
ENCRYPTED_FILES_DIR = settings.ENCRYPTED_FILES_DIR
KEYS_DIR = os.path.join(ENCRYPTED_FILES_DIR, 'keys')
os.makedirs(ENCRYPTED_FILES_DIR, exist_ok=True)
os.makedirs(KEYS_DIR, exist_ok=True)


def initialize_uploaded_file(request):
    """Extracts the uploaded file from the request."""

    if 'file' not in request.FILES:
        raise ValueError('No file selected.')
    return request.FILES['file']


def generate_encryption_key():
    """Generates new encryption key via AWS KMS."""
    try:
        kms_response = kms_client.generate_data_key(
            KeyId=settings.AWS_KMS_KEY_ID,
            KeySpec='AES_256'
        )
        return kms_response['Plaintext'], kms_response['CiphertextBlob']
    except Exception as e:
        raise

def encrypt_file_data(file_data, encryption_key):
    """Encrypts the file data using the encryption key from AWS KMS."""
    try:
        # Initialize AES cipher with the encryption key
        cipher = Cipher(algorithms.AES(encryption_key), modes.CFB8(encryption_key[:16]), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(file_data) + encryptor.finalize()
        return encrypted_data
    except Exception as e:
        logger.error(f"Error encrypting file data: {str(e)}", exc_info=True)
        raise

""" def encrypt_file_data(file_data):
    try:
        # Here we generate a random key instance
        cipher = Fernet(Fernet.generate_key())
        return cipher.encrypt(file_data)
    except Exception as e:
        raise """


def save_encrypted_file(file_name, encrypted_data):
    """Saves the encrypted file to the file system."""
    secured_file_path = os.path.join(ENCRYPTED_FILES_DIR, file_name)
    try:
        with open(secured_file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)
    except Exception as e:
        raise


def save_encryption_key(file_name, encrypted_key):
    """Saves the encrypted encryption key to a separate file."""

    key_file_path = os.path.join(KEYS_DIR, f"{file_name}.key")
    try:
        with open(key_file_path, 'wb') as key_file:
            key_file.write(encrypted_key)
    except Exception as e:
        raise

@csrf_exempt
def process_uploaded_file(request):
    """Main function to handle file upload, encryption, and saving."""
    if request.method == 'POST':
        try:
            # Commence file extraction
            uploaded_file = initialize_uploaded_file(request)
            file_data = uploaded_file.read()

            # Generate KMS encryption key
            encryption_key, encrypted_key = generate_encryption_key()

            # We now encrypt the file data
            encrypted_data = encrypt_file_data(file_data, encryption_key)

            # Finalize the upload process.
            # Save the encrypted file and the key
            save_encrypted_file(uploaded_file.name, encrypted_data)
            save_encryption_key(uploaded_file.name, encrypted_key)

            return JsonResponse({'message': 'File uploaded successfully'}, status=200)

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            # now at this point, an error occurred.
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'trial_task/upload.html')
