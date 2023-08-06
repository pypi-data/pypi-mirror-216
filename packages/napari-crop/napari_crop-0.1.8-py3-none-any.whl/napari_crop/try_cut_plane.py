import numpy as np
import napari
from skimage.data import cells3d
import pyclesperanto_prototype as cle

# from napari_crop import CutWithPlane

image = cells3d()
viewer = napari.Viewer()
viewer.add_image(image, name=['cells3d', 'nuclei3d'], channel_axis=1, scale=(1, 0.5, 0.5))
segmented = cle.voronoi_otsu_labeling(image[:, 1], spot_sigma=10, outline_sigma=1)
viewer.add_labels(segmented, name='labels', opacity=0.5, scale=(1, 0.5, 0.5))


# viewer.window.add_dock_widget(CutWithPlane(viewer), area='right')

napari.run()
