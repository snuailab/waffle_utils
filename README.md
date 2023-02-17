![header](https://github.com/snuailab/assets/blob/main/snuailab/full/snuAiLab.black.300ppi.png?raw=true)

# Waffle Utils
- waffle util tools
- [Waffle Data Convention](https://snuailab.notion.site/Waffle-Data-Convention-7547fda8c1ca48798d00bd4658ea96bf)

# Usage
### Create Dataset from coco format
```python
from waffle_utils.dataset import Dataset

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

ds = Dataset.from_coco(
    dummy_dataset_name,
    dummy_coco_file,
    dummy_coco_root_dir,
    root_dir=dummy_data_root_dir,
)

ds = Dataset.from_directory(dummy_dataset_name, dummy_data_root_dir)

ds.split_train_val(train_split_ratio=0.8)
```
### Format Converting
```python
todo
```

### CLI
```python
todo
```
