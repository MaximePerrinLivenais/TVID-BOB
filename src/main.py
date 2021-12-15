import convert
import image_io
import options

if __name__ == '__main__':

    parser = options.get_options_parser()
    args = parser.parse_args()

    if args.v:
        frames_dir = 'output-frames/'
        convert.video_to_frames(args.path, frames_dir, args.ts)
    elif args.i:
        frames_dir = args.path

    if args.images:
        image_io.display_images_from_dir(frames_dir, args.deinterlace or args.bob,
                                            args.bob, not args.bff)
    elif args.video:
        image_io.create_video_from_dir(frames_dir, args.output, args.deinterlace or args.bob,
                                        args.bob, args.ips, not args.bff)
        image_io.play_video(args.output)
