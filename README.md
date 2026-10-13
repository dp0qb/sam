# 地质图SAM 2.1 + Google Colab 测试项目

用于评估Meta SAM 2.1对彩色地质图的地质体候选区域分割效果，并尝试从GeoTIFF生成面要素。

## 直接运行

1. 打开 `notebooks/geological_sam2_colab.ipynb`，选择 **Open in Colab**，或在Colab中通过「文件 → 上传笔记本」载入 `.ipynb`。
2. 在 Colab 中设置「运行时 → 更改运行时类型 → GPU（如T4）」。GPU是否可选由Google账户和配额决定。私有GitHub仓库可通过Colab的GitHub授权读取；若授权不可用，请直接下载Notebook并在Colab上传。
3. 顺序运行Notebook。默认 `SOURCE='demo'` 使用程序生成的示例地质图，`MODE='auto'` 自动分割。
4. 切换 `SOURCE='upload'` 可以上传 **PNG/JPG/GeoTIFF**；修改 `MODE='point'` 或 `'box'` 使用交互提示。
5. 下载自动生成的 `sam_results.zip`，查看Mask、分割叠加图、GeoJSON等。

## 数据坐标

* GeoTIFF存在CRS时，Notebook保存与推理预览网格对应、带原CRS的 `sam_regions_georeferenced.tif`，另生成EPSG:4326的`sam_polygons_wgs84.geojson`。
* 图片不带地理参考时，Mask及矢量的坐标均为**像素坐标**，不可当作真实GIS位置。
* 为便于Colab推理，大图会缩小到 `MAX_EDGE`；因此结果用于原型和评估，不保证原生分辨率精度。
* SAM候选Mask本身没有地质代号、地层名称、断层性质等专业属性，不能直接作为可交付的MapGIS成果。

## 项目结构

```text
notebooks/geological_sam2_colab.ipynb    # 独立运行，不需要其他仓库代码
README.md
.gitignore
tests/test_notebook_structure.py        # Notebook结构和语法检查
```

## 第三方依赖与使用限制

核心模型来自[facebookresearch/sam2](https://github.com/facebookresearch/sam2)，其源代码在Apache-2.0许可下发布。模型代码及权重由Notebook首次运行时从Meta官方来源下载，仓库**不包含模型权重**。运行需访问GitHub和Meta模型下载站点。

不要上传涉密或其他未经授权的地质资料到Colab、公开仓库或其他云服务。私有GitHub仓库只用于保存代码，并不改变Colab是外部云服务的事实。请使用公开或获准外部处理的数据测试。

## 常见问题

- **没有GPU**：在Colab「运行时」中选择GPU；若配额不允许，可尝试CPU，但速度会明显降低。
- **安装报错**：先「运行时 → 重新启动会话」，重新执行安装单元；Colab环境变化可能影响PyTorch依赖。
- **分割为空/效果不理想**：修改 `MODE='point'` 指定目标，或调小 `MIN_AREA_PIXELS`，再用真实样例做对照。
- **大图显存不足**：降低 `MAX_EDGE` 或 `AUTO_POINTS_PER_SIDE`，并将 `MODE='point'` 作为起点。
- **遇到Google Colab交互点击问题**：设置 `USE_CLICK_UI=False`，修改 `MANUAL_POINT` 或 `MANUAL_BOX` 后重新运行分割单元。
- **要输出MapGIS原生文件**：当前原型只输出GeoJSON及Mask；后续需要开发矢量要素属性映射、拓扑和MapGIS写出模块。

**官方参考**：[SAM 2 README](https://github.com/facebookresearch/sam2) · [官方交互分割示例](https://github.com/facebookresearch/sam2/blob/main/notebooks/image_predictor_example.ipynb) · [官方自动分割示例](https://github.com/facebookresearch/sam2/blob/main/notebooks/automatic_mask_generator_example.ipynb)