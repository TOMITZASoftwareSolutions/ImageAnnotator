import cv2
import os
import tqdm
import argparse


class VideoFrameDecomposerAndSaverManager:
    def __init__(self):
        self.decomposition_fps = None

    def decompose(self, video_name, video_path, images_output_path, decomposition_fps=2, progress_callback=None):
        video_capture = cv2.VideoCapture(video_path)

        extracted_image_files = os.listdir(images_output_path)

        try:
            frames_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            print frames_count
            fps = video_capture.get(cv2.CAP_PROP_FPS)
            print fps
        except:
            pass

        try:
            frames_count = int(video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
            print frames_count
            fps = video_capture.get(cv2.cv.CV_CAP_PROP_FPS)
            print fps
        except:
            pass

        # video_capture.set(cv2.cv.CV_CAP_PROP_FPS,240)
        if decomposition_fps < fps:
            self.decomposition_fps = decomposition_fps
            skip_frame_count = int(round(fps / decomposition_fps))
        else:
            self.decomposition_fps = fps
            skip_frame_count = 1

        def next_frame():
            frame_no = 0
            ret = True
            while ret:
                ret = video_capture.grab()

                frame_no += 1
                frame = None

                frame_file_name = '{1}-{0}.png'.format(frame_no, video_name)

                if frame_no % skip_frame_count == 0 and frame_file_name not in extracted_image_files:
                    ret, frame = video_capture.retrieve()

                if frame_no == frames_count:
                    break

                yield frame_no, frame, frame_file_name

        for frame_no, frame, frame_file_name in tqdm.tqdm(next_frame(), total=frames_count):
            # get frame by frame
            frame_path = os.path.join(images_output_path, frame_file_name)

            if frame is not None:
                cv2.imwrite(frame_path, frame)
                if progress_callback:
                    progress_callback.progress(frame_no, frames_count, images_output_path)


class ProgressCallback:
    def progress(self, frame_no, frames_count, frames_output_path):
        return NotImplemented('Implement this motherfucker')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', default='../example_data/CrossChekInspectionWetClay.mp4')

    args = parser.parse_args()

    videoframedecomposer = VideoFrameDecomposerAndSaverManager()
    video_path = args.video
    video_name = 'CrossChekInspectionWetClay.mp4'
    output_folder = '../example_data/'


    class progress_callback:
        def progress(self, frame_no, frames_count, frames_output_path):
            print 'Progress {0} of {1}'.format(frame_no, frames_count)


    videoframedecomposer.decompose(video_name, video_path, output_folder, decomposition_fps=30)
