import argparse

def get_options_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('path', help = 'the path to the video or images to use', type = str)
    input_type = parser.add_mutually_exclusive_group(required = True)
    input_type.add_argument('-i', help = 'input is an image dir', action = 'store_true')
    input_type.add_argument('-v', help = 'input is a video', action = 'store_true')

    parser.add_argument('-o', '--output', help = 'output stream name', type = str,
                            default = 'output.mpeg')
    parser.add_argument('--deinterlace', help = 'deinterlace the video stream',
                            action = 'store_true')
    parser.add_argument('--ips', help = 'images per seconds of the stream', type = int,
                            default = 25)
    parser.add_argument('-t', '--ts', help = 'demux a TS stream', type = str)

    top_field_first = parser.add_mutually_exclusive_group()
    top_field_first.add_argument('--tff', help = 'frames are top field first',
                                    action = 'store_true', default = True)
    top_field_first.add_argument('--bff', help = 'frames are bottom field first',
                                    action = 'store_true', default = False)

    command = parser.add_mutually_exclusive_group(required = True);
    command.add_argument('--images', help = 'display images composing the stream',
                            action = 'store_true')
    command.add_argument('--video', help = 'play the stream', action = 'store_true')

    return parser
