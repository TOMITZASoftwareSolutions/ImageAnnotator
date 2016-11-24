import os


class ImageFilesManager:
    def __init__(self, video_path, images_path):
        self.video_path = video_path
        self.images_path = images_path

        if self.video_path:
            self.video_name = self.video_path.split('/')[-1]
            self.data_folder = video_path.replace(self.video_name, '')
            self.images_path = os.path.join(self.data_folder, 'images',self.video_name)
        elif self.images_path:
            self.data_folder = self.images_path.split('/')[-1]

        if not os.path.exists(self.images_path):
            os.makedirs(self.images_path)



    def get_image_file(self, index=0):
        image_files = self.get_image_files()

        index = int(index)
        image_file = image_files[index % len(image_files)]

        return image_file

    def get_image_files(self):
        previous_directory = os.getcwd()

        os.chdir(self.images_path)

        def sort_key(key):
            key = key.replace('{0}-'.format(self.video_name),'')
            index = int(key.split('.')[0])
            return index

        image_files = sorted(filter(os.path.isfile, os.listdir('.')), key=sort_key)

        os.chdir(previous_directory)

        return image_files
