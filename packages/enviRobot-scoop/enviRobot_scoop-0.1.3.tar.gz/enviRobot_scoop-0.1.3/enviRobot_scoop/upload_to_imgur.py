import pyimgur
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='./.env')
def init_imgur():
    CLIENT_ID = os.getenv('IMGUR_ID')
    return pyimgur.Imgur(CLIENT_ID)

def upload_to_imgur(img_path):
    # upload to imgur, returns with an url
    im = init_imgur()
    url = im.upload_image(img_path,title='').link
    return url

if __name__ == '__main__':
    print(upload_to_imgur('image/sample.png'))