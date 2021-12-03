import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path
from typing import Iterator, Optional

def display_image(image: np.array) -> None:
    plt.imshow(image)
    plt.show()

def play_frames_as_video(image_list: np.array,
                            output_path: Path,
                            dpi: int = 50,
                            fps: int = 30,
                            title: str = 'video',
                            comment: Optional[str] = None,
                            writer: str = 'ffmpeg'
                        ) -> None:
    _, height, width, _ = image_list.shape
    figure, axes = plt.subplots(figsize = (width / dpi, height / dpi))

    figure.subplots_adjust(left = 0,
                            bottom = 0,
                            right = 1,
                            top = 1,
                            wspace = None,
                            hspace = None,
                        )

    mpl_writer = mpl.animation.writers[writer]
    metadata = { 'title': title, 'artist': __name__, 'comment': comment, }
    mpl_writer = mpl_writer(fps = fps, metadata = { k: v for k, v in metadata.items() if v is not None },)

    iterator = iter(image_list)
    with mpl_writer.saving(figure, output_path, dpi = dpi):
        plot = axes.imshow(next(iterator), interpolation = 'nearest')
        mpl_writer.grab_frame()

        for image in iterator:
            plot.set_data(image)
            mpl_writer.grab_frame()

    # call a subprocess
