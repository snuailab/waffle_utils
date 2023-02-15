![header](https://github.com/snuailab/assets/blob/main/snuailab/full/snuAiLab.black.300ppi.png?raw=true)

# Waffle Utils
- waffle util tools
- [Waffle Data Convention](https://snuailab.notion.site/Waffle-Data-Convention-7547fda8c1ca48798d00bd4658ea96bf)

# Usage
### Generate Dataset
```python
from waffle_utils import data_tools as dt
from waffle_utils.data.formats import DetAnn

ds = dt.create_dataset("dataset_dir")

img_id = ds.add_image(image_path="images/apple.png")
cat_id = ds.add_category(supercategory=None, name="apple")
ann_id = ds.add_annotation(
    img_id,
    DetAnn(
        cat_id=cat_id,
        xyxy=[100, 100, 200, 200]
    )
)

ann = ds.get_anns(img_id=img_id)[0]
bbox = ann.bbox
bbox.xyxy  # [100, 100, 200, 200]
bbox.xywh  # [100, 100, 100, 100]
bbox.cxcywh  # [150, 150, 100, 100]
bbox.aspect_ratio  # 1
bbox.area  # 10000

ds.export("save_dir", dt.YOLO_DETECTION)
"""
save_dir/
    images/
        apple.png
    annotations.json
"""
ds.export("save_dir", dt.COCO_DETECTION)
"""
save_dir/
    images/
        apple.png
    labels/
        apple.txt
"""
```
### Format Converting
```python
from waffle_utils import DataTools as dt

ds = dt.from_directory("save_dir", dt.YOLO_DETECTION)
ds.export("save_dir", dt.COCO_DETECTION)
```

### CLI
```python
todo
```
