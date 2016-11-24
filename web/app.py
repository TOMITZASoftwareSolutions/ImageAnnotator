import argparse

from flask import Flask, render_template, request, send_from_directory

from managers.decomposer import VideoFrameDecomposerAndSaverManager
from managers.imagefiles import ImageFilesManager
from managers.tags import TagsManager
from managers.saver import TagSaverManager

app = Flask(__name__)

images_file_manager = None
decompose_fps = None


# @app.route('/')
# def index():
#     return redirect(url_for('tag_page'), code=200)


@app.route('/', methods=['GET'])
def tag_page():
    if images_file_manager.video_path:
        decomposer = VideoFrameDecomposerAndSaverManager()
        decomposer.decompose(images_file_manager.video_name, images_file_manager.video_path,
                             images_file_manager.images_path, decompose_fps)
        fps = decomposer.decomposition_fps
    else:
        fps = decompose_fps
    tags_manager = TagsManager(images_file_manager.data_folder)
    tags = tags_manager.get_tags()
    indexed_tags = zip(range(1, len(tags) + 1), tags)
    return render_template('tagging.html', tags=indexed_tags,
                           images_count=len(images_file_manager.get_image_files()),
                           images=images_file_manager.get_image_files(), decompose_fps=fps)


@app.route('/images/<image>', methods=['GET'])
def images(image):
    app.logger.info(image)
    return send_from_directory(images_file_manager.images_path, image)


@app.route('/save', methods=['POST'])
def save_tags():
    tags = request.form['tags']
    tags_saver_manager = TagSaverManager()
    tags_saver_manager.save(images_file_manager.get_image_files(), tags, images_file_manager.data_folder,
                            images_file_manager.images_path)
    return render_template('workdone.html')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path",
                        default='example_data/mov_bbb.mp4')
    parser.add_argument("--images_path", default=None)
    parser.add_argument("--decompose_fps", default=5)

    args = parser.parse_args()

    video_path = args.video_path
    images_path = args.images_path
    decompose_fps = int(args.decompose_fps)

    print 'Video path: {0}'.format(video_path)
    print 'Images path: {0}'.format(images_path)
    print 'Decompose speed: {0}'.format(decompose_fps)

    images_file_manager = ImageFilesManager(video_path=video_path, images_path=images_path)

    app.local = True
    app.run(port=9191, host="0.0.0.0",
            debug=True)
