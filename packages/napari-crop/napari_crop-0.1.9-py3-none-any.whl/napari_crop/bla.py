import numpy as np
import napari

arr_2d = np.arange(0, 25).reshape((5, 5))  # 2d case

# array([[ 0,  1,  2,  3,  4],
#        [ 5,  6,  7,  8,  9],
#        [10, 11, 12, 13, 14],
#        [15, 16, 17, 18, 19],
#        [20, 21, 22, 23, 24]])
shapes = [
    np.array([[1, 1], [1, 3], [4, 3], [4, 1]]),
    np.array([[0.5, 0.5], [0.5, 3.5], [4.51, 3.5], [4.51, 0.5]]),
    np.array([[0, 2], [2, 0], [3, 2], [2, 4]]),
]
shape_types = ["rectangle", "ellipse", "polygon"]

viewer = napari.Viewer()
# viewer.add_image(arr_2d)
# viewer.add_shapes(shapes, shape_type=shape_types)

napari.run()
