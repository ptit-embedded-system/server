import cloudinary
import cloudinary.uploader
import cloudinary.api
import configparser


class CloudinaryClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        config = configparser.ConfigParser()
        config.read('config/config.ini')
        cloud_name = config['cloudinary']['cloud_name']
        api_key = int(config['cloudinary']['api_key'])
        api_secret = config['cloudinary']['api_secret']
        if not cls._instance:
            cls._instance = super(CloudinaryClient, cls).__new__(cls)
            cls._instance.cld = cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret
            )
        return cls._instance

    def upload_file(self, file_path):
        response = cloudinary.uploader.upload(file_path, resource_type="auto", format="mp3")
        return response

    def delete_file(self, public_id):
        response = cloudinary.api.delete_resources(public_id)
        return response

    def get_file_info(self, public_id):
        response = cloudinary.api.resource(public_id)
        return response
