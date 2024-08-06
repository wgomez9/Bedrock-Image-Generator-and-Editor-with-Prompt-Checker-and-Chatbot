import boto3
import pickle
import io
from config_file import Config
from PIL import Image
import numpy as np
import hashlib

# Save an image to S3 and return its key
def save_image_to_s3(img, key_prefix):
    s3 = boto3.client('s3')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_data = img_byte_arr.getvalue()
    img_hash = hashlib.md5(img_data).hexdigest()
    image_key = f"{key_prefix}/{img_hash}.png"
    
    # Check if image already exists, save if it doesn't
    try:
        s3.head_object(Bucket=Config.S3_BUCKET_NAME, Key=image_key)
    except:
        # Image doesn't exist, so save it
        s3.put_object(Bucket=Config.S3_BUCKET_NAME, Key=image_key, Body=img_data)
    
    return image_key

# Delete an image from S3
def delete_image_from_s3(image_key):
    s3 = boto3.client('s3')
    s3.delete_object(Bucket=Config.S3_BUCKET_NAME, Key=image_key)

# Save data to S3, handling both dictionaries and other data types
def save_to_s3(data, key):
    s3 = boto3.client('s3')
    if isinstance(data, dict):
        for session_name, session_data in data.items():
            session_key = f"{key}/{session_name}/session_data.pkl"
            session_data_copy = session_data.copy()

            for image_type in ['base_images', 'variation_images', 'editing_images']:
                if image_type in session_data_copy:
                    session_data_copy[image_type] = [img if isinstance(img, str) else save_image_to_s3(img, f"{key}/{session_name}/{image_type}") for img in session_data_copy[image_type]]

            pickled_data = pickle.dumps(session_data_copy)
            s3.put_object(Bucket=Config.S3_BUCKET_NAME, Key=session_key, Body=pickled_data)
    else:
        pickled_data = pickle.dumps(data)
        s3.put_object(Bucket=Config.S3_BUCKET_NAME, Key=key, Body=pickled_data)

# Load data from S3, handling both session data and other data types
def load_from_s3(key):
    s3 = boto3.client('s3')
    try:
        if key in ['stability_sessions', 'titan_sessions', 'chat_image_editor_sessions']:
            sessions = {}
            response = s3.list_objects_v2(Bucket=Config.S3_BUCKET_NAME, Prefix=f"{key}/")
            for obj in response.get('Contents', []):
                if obj['Key'].endswith('session_data.pkl'):
                    session_name = obj['Key'].split('/')[1]
                    session_data = pickle.loads(s3.get_object(Bucket=Config.S3_BUCKET_NAME, Key=obj['Key'])['Body'].read())
                    sessions[session_name] = session_data
            return sessions
        else:
            response = s3.get_object(Bucket=Config.S3_BUCKET_NAME, Key=key)
            return pickle.loads(response['Body'].read())
    except Exception as e:
        print(f"Error loading from S3: {str(e)}")
        return None

# Delete data from S3
def delete_from_s3(key):
    s3 = boto3.client('s3')
    try:
        response = s3.list_objects_v2(Bucket=Config.S3_BUCKET_NAME, Prefix=key)
        for obj in response.get('Contents', []):
            s3.delete_object(Bucket=Config.S3_BUCKET_NAME, Key=obj['Key'])
        print(f"Successfully deleted: {key}")
    except Exception as e:
        print(f"Failed to delete: {key}. Error: {str(e)}")