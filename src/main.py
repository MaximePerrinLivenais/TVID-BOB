import convert
import image_io
import options

if __name__ == '__main__':

    parser = options.get_options_parser()
    args = parser.parse_args()

    print(args.ts)

    frames_dir = 'output-frames/'
    convert.video_to_frames(args.video_path, frames_dir, args.ts)

    if args.images:
        image_io.display_images_from_dir(frames_dir, deinterlacing = args.deinterlace)
    elif args.video:
        image_io.create_video_from_dir(frames_dir, args.output, args.deinterlace, args.ips)
        image_io.play_video(args.output)
