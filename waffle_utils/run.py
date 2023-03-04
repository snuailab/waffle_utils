import typer
from rich import print

from waffle_utils.dataset import Dataset
from waffle_utils.dataset.format import Format
from waffle_utils.file.io import unzip
from waffle_utils.file.network import get_file_from_url
from waffle_utils.video.defaults import DEFAULT_FRAME_RATE
from waffle_utils.video.tools import create_video, extract_frames

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


# video processing docs
input_video_path_docs = "path to input video file"
input_frames_dir_docs = "directory to input frame image files"
output_frames_dir_docs = "directory to output frame image files"
output_video_path_docs = "path for output video file"
frame_rate_docs = "frame rate"
verbose_docs = "verbose"


@app.command(name="extract_frames")
def _extract_frames(
    input_path: str = typer.Option(..., help=input_video_path_docs),
    output_dir: str = typer.Option(..., help=output_frames_dir_docs),
    frame_rate: int = typer.Option(DEFAULT_FRAME_RATE, help=frame_rate_docs),
    verbose: bool = typer.Option(False, help=verbose_docs),
):
    """Extract Frames from a Video File"""

    extract_frames(input_path, output_dir, frame_rate, verbose)


@app.command(name="create_video")
def _create_video(
    input_dir: str = typer.Option(..., help=input_frames_dir_docs),
    output_path: str = typer.Option(..., help=output_video_path_docs),
    frame_rate: int = typer.Option(DEFAULT_FRAME_RATE, help=frame_rate_docs),
    verbose: bool = typer.Option(False, help=verbose_docs),
):
    """Create a Video from Frame Image Files"""

    create_video(input_dir, output_path, frame_rate, verbose)


if __name__ == "__main__":
    app()
