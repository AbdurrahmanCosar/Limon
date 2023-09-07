import os
from requests import get
from io import BytesIO
from PIL import Image
from typing import Optional

class ImageDownloader:
    def __init__(self, link_dict: dict):
        self.links = link_dict

    def _switch_directory(self, folder_name: Optional[str] = None):
        """
        Checks the file path. If it is in the wrong directory, 
        it comes back and enters the correct directory.
        If it is in the main directory(images), it enters the specified directory

        images: -> Main Folder
            icon_folder -> Subfolder
                icon.png
            badge_folder -> Subfolder
                badge.png
        """
        curr_path = os.getcwd().split('/')[-1]

        if (folder_name and folder_name == curr_path) or (not folder_name and curr_path == "images"):
            return
        elif folder_name and curr_path != "images":
            target_directory = '../' + folder_name
        elif not folder_name and curr_path != "images":
            target_directory = '..'
        else:
            target_directory = folder_name

        os.chdir(target_directory)

    def restore_directory(self):
        curr_path = os.getcwd().split('/')
        if curr_path[-1] == "images":
            old_directory = "../../../"
        else:
            old_directory = "../../../../"

        os.chdir(old_directory)

    async def start_download(self):
        """Download images in database to specified directories"""
        # Set directory
        os.chdir("cogs/assets") 
        os.makedirs("images", mode=0o777, exist_ok=True)
        os.chdir("images")
        os.makedirs("expense_icons", mode=0o777, exist_ok=True)
        os.makedirs("badges", mode=0o777, exist_ok=True)
        
        try:
            for key, value in self.links.items():
                response = get(value)
                img = Image.open(BytesIO(response.content)).convert("RGBA")

                # Change directory
                if key[:4] == "icon":
                    self._switch_directory("expense_icons")
                elif key[:5] == "badge":
                    self._switch_directory("badges")
                else:
                    self._switch_directory()

                img.save(f'{key}.png')
            self.restore_directory()
            return True
        except Exception as err:
            print(err)
            return False
