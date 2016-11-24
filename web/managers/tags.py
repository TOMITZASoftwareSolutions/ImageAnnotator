import os


class TagsManager:
    def __init__(self, tags_folder=None):
        self.tags_folder = tags_folder

    def get_tags(self):
        tags_file = os.path.join(self.tags_folder, 'labels.txt')
        with open(tags_file) as f:
            tags = f.readline()

        return tags.split(' ')
