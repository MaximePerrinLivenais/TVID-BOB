import argparse

def get_options_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('video_path', help = 'the path to the video to use', type = str)

    parser.add_argument('-o', '--output', help = 'output stream name', type = str,
                            default = 'output.mpeg')
    parser.add_argument('--deinterlace', help = 'deinterlace the video stream',
                            action = 'store_true')
    parser.add_argument('--ips', help = 'images per seconds of the stream', type = int,
                            default = 25)
    parser.add_argument('-t', '--ts', help = 'demux a TS stream', type = int)

    command = parser.add_mutually_exclusive_group(required = True);
    command.add_argument('--images', help = 'display images composing the stream',
                            action = 'store_true')
    command.add_argument('--video', help = 'play the stream', action = 'store_true')

    return parser
