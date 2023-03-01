import typer
from rich import print

from waffle_utils.dataset import Dataset
from waffle_utils.dataset.format import Format
from waffle_utils.file.io import unzip
from waffle_utils.file.network import get_file_from_url
from waffle_utils.video_processing.video_tools import VideoTools

app = typer.Typer()

# dataset docs
name_docs = "Dataset Name"
root_dir_docs = "Dataset Root Directory. Default to ./datasets"

# coco docs
coco_file_docs = "COCO json file"
coco_root_dir_docs = "COCO image root directory"

# split docs
train_split_ratio_docs = (
    "train data ratio. val ratio will be set to (1-train_split_ratio)"
)

# export docs
format_docs = f"[{', '.join(map(lambda x: x.name, Format))}]"

# video processing docs
input_video_path_docs = "input video file path"
input_images_path_docs = "input image files path"
output_images_path_docs = "output images path"
output_video_path_docs = "output video file path"
frame_rate_docs = "frame rate"
fps_docs = "frames per second"
verbose_docs = "verbose"


@app.command(name="get_file_from_url")
def _get_file_from_url(
    url: str = typer.Option(..., help="download link"),
    file_path: str = typer.Option(..., help="download output file"),
    create_directory: bool = True,
):
    get_file_from_url(url, file_path, create_directory=create_directory)
    print(f"Downloading File {file_path} has been completed.")


@app.command(name="unzip")
def _unzip(
    url: str = typer.Option(..., help="download link"),
    output_dir: str = typer.Option(..., help="output directory"),
    create_directory: bool = True,
):
    unzip(url, output_dir, create_directory=create_directory)


@app.command(name="from_coco")
def _from_coco(
    name: str = typer.Option(..., help=name_docs),
    root_dir: str = typer.Option(None, help=root_dir_docs),
    coco_file: str = typer.Option(..., help=coco_file_docs),
    coco_root_dir: str = typer.Option(..., help=coco_root_dir_docs),
):
    """Import Dataset from COCO Format"""

    Dataset.from_coco(
        name,
        coco_file=coco_file,
        coco_root_dir=coco_root_dir,
        root_dir=root_dir,
    )


@app.command(name="split_train_val")
def _split_train_val(
    name: str = typer.Option(..., help=name_docs),
    root_dir: str = typer.Option(None, help=root_dir_docs),
    train_split_ratio: float = typer.Option(..., help=train_split_ratio_docs),
    random_seed: int = 0,
):
    """split train validation"""

    ds = Dataset.from_directory(name, root_dir=root_dir)
    ds.split_train_val(train_split_ratio, seed=random_seed)


@app.command(name="export")
def _export(
    name: str = typer.Option(..., help=name_docs),
    root_dir: str = typer.Option(None, help=root_dir_docs),
    export_format: str = typer.Option(..., help=format_docs),
):
    """Export Dataset"""

    ds = Dataset.from_directory(name, root_dir)

    export_format = export_format.upper()
    if not hasattr(Format, export_format):
        raise ValueError(
            f"Does not support {export_format} format. Try with {format_docs}"
        )

    ds.export(Format[export_format])


@app.command(name="extract_frames")
def _extract_frames(
    input_path: str = typer.Option(..., help=input_video_path_docs),
    output_path: str = typer.Option(..., help=output_images_path_docs),
    frame_rate: int = typer.Option(30, help=frame_rate_docs),
    verbose: bool = typer.Option(False, help=verbose_docs),
):
    """Extract Frames from a Video File"""

    vt = VideoTools.from_video(input_path, output_path)
    vt.extract_frames(frame_rate, verbose)


@app.command(name="create_video")
def _create_video(
    input_path: str = typer.Option(..., help=input_images_path_docs),
    output_path: str = typer.Option(..., help=output_video_path_docs),
    fps: int = typer.Option(30, help=fps_docs),
    verbose: bool = typer.Option(False, help=verbose_docs),
):
    """Create a Video from Frame Image Files"""

    vt = VideoTools.from_images(input_path, output_path)
    vt.create_video(fps, verbose)


if __name__ == "__main__":
    app()
