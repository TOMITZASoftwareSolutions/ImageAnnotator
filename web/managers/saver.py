import os
from shutil import copy2


class TagSaverManager:
    def __init__(self):
        pass

    def save(self, images=None, tags=None, data_folder=None, images_folder=None):
        tags = tags.split(',')

        dataset_path = os.path.join(data_folder, 'dataset')
        if not os.path.exists(dataset_path):
            os.mkdir(dataset_path)

        for tag, image in zip(tags, images):
            if tag != '':
                path = os.path.join(dataset_path, tag)
                if not os.path.exists(path):
                    os.mkdir(path)

                copy2(os.path.join(images_folder, image), os.path.join(path, image))


if __name__ == '__main__':
    tag_saver_manager = TagSaverManager()

    tags = ',,,wolf,kitten,cat,kitten'

    images = ['100.png', '101.png', '107.png', '108.png', '102.png', '103.png', '104.png']

    tag_saver_manager.save(images, tags, 'example_data')
