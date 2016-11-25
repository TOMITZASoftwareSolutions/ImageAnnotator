## Deploying
    Open terminal in folder where Dockerfile is:
    1. Create a folder where you place your video/images and a labels.txt file where you place tags in a single line separated by space
    2. Build docker image:
        docker build -t image_annotator .
    3. Start docker container:
        docker run -p 80:9191 -it -v  <local_data_folder>:/ image_annotator python app.py --video_path /<video_name> --decompose_fps 2
    4. Open localhost:80 in Chrome Browser
    5. See progress in terminal for video decomposition
    
## Commandline Arguments 
    <local_data_folder> - The folder on your local machine where the video is - the folder is mounted in root on docker so when specifying video name you should use /
    --video_path /<video_name> the name of your video
    --decompose_fps - sampling rate from the original video (based on this and the video size the loading time will vary)

## Shortcut Controls
    Play: Space key
    Rewind: → key
    Forward: ← key
    Playback Speed Increase: . key
    Playback Speed Descrease: , key
    Tags: 1,2,3...
    
## Example of run command:
    docker run -p 80:9191 -it -v /$PWD/:/data image_annotator python app.py --video_path /data/"CrossChek Inspection - Wet Clay.mp4" --decompose_fps 2
