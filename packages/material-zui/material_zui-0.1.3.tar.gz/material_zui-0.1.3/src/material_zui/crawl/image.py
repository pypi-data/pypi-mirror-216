from uuid import uuid4
import requests
from bs4 import BeautifulSoup

from material_zui.image import download, download_base64, base64_ext
from material_zui.list import list_range
from material_zui.validate import is_base64, is_valid_url


def get_all_image_urls(url: str, limit: int = 0, start_index: int = 0) -> list[str]:
    '''
    Get all image url and base64 of image tags
    '''
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    images = soup.find_all("img")
    # Create a directory to store the downloaded images
    # if not os.path.exists("images"):
    #     os.mkdir("images")
    images = list_range(images, limit, start_index)
    return [image["src"] for image in images]


def download_image_urls(src_images: list[str], output_path: str) -> None:
    '''
    Download image from src url
    @src_images: must be a valid url (with `http(s)` prefix) or base64 string
    '''
    for src_image in src_images:
        if is_valid_url(src_image):
            print('Downloading', src_image)
            filename = src_image.split("/")[-1]
            file_output_path = f'{output_path}/{filename}'
            download(src_image, file_output_path)
        elif is_base64(src_image):
            print('Downloading', src_image)
            ext = base64_ext(src_image)
            if ext:
                filename = f'{str(uuid4())}.{ext}'
                file_output_path = f'{output_path}/{filename}'
                download_base64(src_image, file_output_path)
        else:
            print('Invalid type value', src_image)
    print("Download complete!")


def download_all_image(url: str, output_path: str, limit: int = 0, start_index: int = 0) -> None:
    '''
    Download all image from url
    @url: must be a valid url (with `http(s)` prefix)
    '''
    src_images = get_all_image_urls(url, limit, start_index)
    download_image_urls(src_images, output_path)

# def download_all_image(url: str, output_path: str, limit: int = 0, start_index: int = 0) -> None:
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")
#     images = soup.find_all("img")

#     # Create a directory to store the downloaded images
#     # if not os.path.exists("images"):
#     #     os.mkdir("images")
#     end_index = start_index+limit
#     images = get_all_image_urls(url,limit,start_index)
#     # src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
#     # download_base64(src, f'{output_path}/abc.png')
#     # ext = base64_ext(src)
#     for image in images:
#         src = image["src"]
#         if is_valid_url(src):
#             print('Downloading', src)
#             filename = src.split("/")[-1]
#             file_output_path = f'{output_path}/{filename}'
#             download(src, file_output_path)
#         elif is_base64(src):
#             print('Downloading', src)
#             ext = base64_ext(src)
#             if ext:
#                 filename = f'{str(uuid4())}.{ext}'
#                 file_output_path = f'{output_path}/{filename}'
#                 download_base64(src, file_output_path)
#         else:
#             print('Invalid type value', src)
#     print("Download complete!")
