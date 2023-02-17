from waffle_utils.dataset import Dataset
from waffle_utils.file import io, network


def test_network():
    url = "https://github.com/snuailab/waffle_utils/raw/main/mnist.zip"

    dummy_tmp_dir = "tmp"
    dummy_zip_file = "tmp/mnist.zip"
    dummy_data_root_dir = "tmp/dataset"
    dummy_dataset_name = "mnist"

    dummy_extract_dir = "tmp/extract"
    dummy_coco_root_dir = "tmp/extract/raw"
    dummy_coco_file = "tmp/extract/exports/coco.json"

    network.get_file_from_url(url, dummy_zip_file, create_directory=True)
    io.unzip(dummy_zip_file, dummy_extract_dir, create_directory=True)

    # ds = Dataset.from_coco(
    #     dummy_dataset_name,
    #     dummy_coco_file,
    #     dummy_coco_root_dir,
    #     root_dir=dummy_data_root_dir,
    # )

    ds = Dataset.from_directory(dummy_dataset_name, dummy_data_root_dir)

    ds.split_train_val(train_split_ratio=0.8)

    # todo export
    # ds.export

    # io.remove_directory(dummy_tmp_dir)
