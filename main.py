import requests
import functools
from config import settings, headers

headers = headers

payload = {}
folders = []

siteURL = settings['siteURL']
rootFolder = settings['rootFolder']
downloadURL = settings['downloadURL']

imageDownloadPath = settings['imageDownloadPath']

getListAction = settings['getListAction']
getFilesAction = settings['getFilesAction']

HTTP_AUTH = settings['HTTP_AUTH']

@functools.lru_cache(maxsize=None)
def getFolders(url):
    try:
        print(f'Parsing {url}')
        response = requests.request("POST", url, headers=headers, data=payload)
        responseJSON = response.json()

        if responseJSON:
            for folder in responseJSON:
                folder_name = folder['id']
                folders.append(folder_name)
                newURL = siteURL + getListAction + folder_name + '/&type=dir'
                getFolders(newURL)

        return folders
    except Exception as e:
        print(f'Error - {e} ----------------------------------------- in {url}')


def downloadImage(image):
    try:
        print('Starting to download the image...')
        imageURL = downloadURL + image + HTTP_AUTH
        img = requests.get(imageURL, headers=headers, data=payload)
        img_file = open(imageDownloadPath + image.replace("/", "-"), 'wb')
        img_file.write(img.content)
        img_file.close()
        print('Image downloaded')
    except Exception as e:
        print(f'Error - {e} ----------------------------------------- in {image}')

if __name__ == "__main__":
    rootFolderURL = siteURL + getListAction +  rootFolder + '/&type=dir'
    for image in getFolders(rootFolderURL):
        if '.jpg' in image or '.png' in image:
            downloadImage(image)
        else:
            getFilesURL = siteURL + getFilesAction + image
            images = requests.get(getFilesURL, headers=headers, data=payload)
            images = images.json()
            imagesJSON = images['results']
            for img in imagesJSON:
                if '.jpg' in img or '.png' in img:
                    downloadImage(image)