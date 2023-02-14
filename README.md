![header](https://github.com/snuailab/assets/blob/main/snuailab/full/snuAiLab.black.300ppi.png?raw=true)

# Waffle Utils
- waffle util tools
- [Waffle Data Convention](https://snuailab.notion.site/Waffle-Data-Convention-7547fda8c1ca48798d00bd4658ea96bf)

# Usage
### Generate Dataset
```python
from waffle_utils.data import DataTools as DT
from waffle_utils.data.formats import DetAnn

dt = DT()

img_id = dt.add_image(image_path="images/apple.png")
cat_id = dt.add_category(supercategory=None, name="apple")
ann_id = dt.add_annotation(
    img_id,
    DetAnn(
        cat_id=cat_id,
        xyxy=[100, 100, 200, 200]
    )
)

ann = dt.get_anns(img_id=img_id)[0]
bbox = ann.bbox
bbox.xyxy  # [100, 100, 200, 200]
bbox.xywh  # [100, 100, 100, 100]
bbox.cxcywh  # [150, 150, 100, 100]
bbox.aspect_ratio  # 1
bbox.area  # 10000

dt.export("save_dir", DT.YOLO_DETECTION)
"""
save_dir/
    images/
        apple.png
    annotations.json
"""
dt.export("save_dir", DT.COCO_DETECTION)
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
from waffle_utils.data import DataTools as DT

dt = DT.from_directory("save_dir", DT.YOLO_DETECTION)
dt.export("save_dir", DT.COCO_DETECTION)
```

### CLI
```python
todo
```
