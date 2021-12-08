import sys

import image_io

command = sys.argv[1]
dir_path = sys.argv[2]

if command == 'display':
    image_io.display_images_from_dir(dir_path, deinterlacing = True)
elif command == 'video':
    image_io.create_video_from_dir(dir_path, sys.argv[3], True)
