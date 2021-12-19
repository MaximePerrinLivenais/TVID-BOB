import argparse

def get_options_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('path', help = 'the path to the video or images to use', type = str)
    parser.add_argument('-o', '--output', help = 'output stream name', type = str,
                            default = 'output.mpeg')
    parser.add_argument('--ips', help = 'images per seconds of the stream', type = int,
                            default = None)
    parser.add_argument('-t', '--ts', help = 'demux a TS stream', type = str)

    input_type = parser.add_mutually_exclusive_group(required = True)
    input_type.add_argument('-i', help = 'input is an image dir', type = str)
    input_type.add_argument('-v', help = 'input is a video', action = 'store_true')

    deinterlacer = parser.add_mutually_exclusive_group()
    deinterlacer.add_argument('--deinterlace', help = 'deinterlace the video stream',
                                type = float, default = None, nargs = '?')
    deinterlacer.add_argument('--bob', help = 'deinterlace the video stream using bob',
                                action = 'store_true')
    deinterlacer.add_argument('--raw', action = 'store_true')

    command = parser.add_mutually_exclusive_group(required = True);
    command.add_argument('--images', help = 'display images composing the stream',
                            action = 'store_true')
    command.add_argument('--video', help = 'play the stream', action = 'store_true')

    return parser
