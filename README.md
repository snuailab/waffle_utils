![header](https://github.com/snuailab/assets/blob/main/snuailab/full/snuAiLab.black.300ppi.png?raw=true)

# Waffle Utils
- waffle util tools
- [Waffle Data Convention](https://snuailab.notion.site/Waffle-Data-Convention-7547fda8c1ca48798d00bd4658ea96bf)

# Examples
### Create Dataset from coco format
```python
from waffle_utils.dataset import Dataset
from waffle_utils.dataset.format import Format

url = "https://github.com/snuailab/waffle_utils/raw/main/mnist.zip"

dummy_zip_file = "mnist.zip"
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
)

ds = Dataset.from_directory(dummy_dataset_name, dummy_data_root_dir)

ds.split_train_val(train_split_ratio=0.8)
ds.export(Format.YOLO_DETECTION)
```

```
python main.py get_file_from_url --url https://github.com/snuailab/waffle_utils/raw/main/mnist.zip --file-path tmp/mnist.zip
python main.py unzip --url tmp/mnist.zip --output-dir tmp/extract
python main.py from_coco --name mnist --coco-file tmp/extract/exports/coco.json --coco-root-dir tmp/extract/raw
python main.py split_train_val --name mnist --train-split-ratio 0.8
python main.py export --name mnist --export-format yolo_detection
```
### Format Converting
```python
todo
```

### CLI
```python
todo
```
