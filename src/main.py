import convert
import image_io
import options
import parse_logs

if __name__ == '__main__':

    parser = options.get_options_parser()
    args = parser.parse_args()

    meta_file = 'frames.meta'
    if args.v:
        frames_dir = 'output-frames/'
        convert.video_to_frames(args.path, frames_dir, args.ts)
    else:
        frames_dir = args.path
        meta_file = args.i

    frames_meta = parse_logs.parse_logs(meta_file)
    print(len(frames_meta))

    if args.images:
        image_io.display_images_from_dir(frames_dir, args.deinterlace or args.bob,
                                            args.bob, args.deinterlace, frames_meta)
    elif args.video:
        image_io.create_video_from_dir(frames_dir, args.output, args.deinterlace or args.bob,
                                        args.bob, args.ips, args.deinterlace, frames_meta)
        image_io.play_video(args.output)
