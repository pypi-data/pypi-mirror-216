import cv2
import math
import imgaug
import pyclipper
import numpy as np

import torch


import imgaug
import imgaug.augmenters as iaa
from shapely.geometry import Polygon
from collections import OrderedDict



class DataProcess:
    r'''Processes of data dict.
    '''

    def __call__(self, data, **kwargs):
        return self.process(data, **kwargs)

    def process(self, data, **kwargs):
        raise NotImplementedError

    def render_constant(self,
                        canvas,
                        xmin,
                        xmax,
                        ymin,
                        ymax,
                        value=1,
                        shrink=0):

        def shrink_rect(xmin, xmax, ratio):
            center = (xmin + xmax) / 2
            width = center - xmin
            return int(center - width * ratio + 0.5), int(center + width * ratio + 0.5)

        if shrink > 0:
            xmin, xmax = shrink_rect(xmin, xmax, shrink)
            ymin, ymax = shrink_rect(ymin, ymax, shrink)

        canvas[int(ymin + 0.5):int(ymax + 0.5) + 1, int(xmin + 0.5):int(xmax + 0.5) + 1] = value
        return canvas





class AugmenterBuilder(object):

    # ------------------------------------------------------------------------------
    # The implementation is adopted from DBNet,
    # made publicly available under the Apache License 2.0 at https://github.com/MhLiao/DB.
    # ------------------------------------------------------------------------------

    def __init__(self):
        pass

    def build(self, args, root=True):
        if args is None:
            return None
        elif isinstance(args, (int, float, str)):
            return args
        elif isinstance(args, list):
            if root:
                sequence = [self.build(value, root=False) for value in args]
                return iaa.Sequential(sequence)
            else:
                return getattr(
                    iaa,
                    args[0])(*[self.to_tuple_if_list(a) for a in args[1:]])
        elif isinstance(args, dict):
            if 'cls' in args:
                cls = getattr(iaa, args['cls'])
                return cls(
                    **{
                        k: self.to_tuple_if_list(v)
                        for k, v in args.items() if not k == 'cls'
                    })
            else:
                return {
                    key: self.build(value, root=False)
                    for key, value in args.items()
                }
        else:
            raise RuntimeError('unknown augmenter arg: ' + str(args))

    def to_tuple_if_list(self, obj):
        if isinstance(obj, list):
            return tuple(obj)
        return obj



class AugmentData(DataProcess):

    def __init__(self, cfg):
        self.augmenter_args = cfg.augmenter_args
        self.keep_ratio = cfg.keep_ratio
        self.only_resize = cfg.only_resize
        self.augmenter = AugmenterBuilder().build(self.augmenter_args)

    def may_augment_annotation(self, aug, data):
        pass

    def resize_image(self, image):
        origin_height, origin_width, c = image.shape
        resize_shape = self.augmenter_args[0][1]

        new_height_pad = resize_shape['height']
        new_width_pad = resize_shape['width']
        if self.keep_ratio:
            if origin_height > origin_width:
                new_height = new_height_pad
                new_width = int(
                    math.ceil(new_height / origin_height * origin_width / 32)
                    * 32)
            else:
                new_width = new_width_pad
                new_height = int(
                    math.ceil(new_width / origin_width * origin_height / 32)
                    * 32)
            image = cv2.resize(image, (new_width, new_height))

        else:
            image = cv2.resize(image, (new_width_pad, new_height_pad))

        return image

    def process(self, data):
        image = data['image']
        aug = None
        shape = image.shape
        if self.augmenter:
            aug = self.augmenter.to_deterministic()
            if self.only_resize:
                data['image'] = self.resize_image(image)
            else:
                data['image'] = aug.augment_image(image)
            self.may_augment_annotation(aug, data, shape)

        filename = data.get('filename', data.get('data_id', ''))
        data.update(filename=filename, shape=shape[:2])
        if not self.only_resize:
            data['is_training'] = True
        else:
            data['is_training'] = False
        return data


class AugmentDetectionData(AugmentData):

    def may_augment_annotation(self, aug: imgaug.augmenters.Augmenter, data,
                               shape):
        if aug is None:
            return data

        line_polys = []
        keypoints = []
        texts = []
        new_polys = []
        for line in data['lines']:
            texts.append(line['text'])
            new_poly = []
            for p in line['poly']:
                new_poly.append((p[0], p[1]))
                keypoints.append(imgaug.Keypoint(p[0], p[1]))
            new_polys.append(new_poly)
        if not self.only_resize:
            keypoints = aug.augment_keypoints(
                [imgaug.KeypointsOnImage(keypoints=keypoints,
                                         shape=shape)])[0].keypoints
            new_polys = np.array([[p.x, p.y]
                                  for p in keypoints]).reshape([-1, 4, 2])
        for i in range(len(texts)):
            poly = new_polys[i]
            line_polys.append({
                'points': poly,
                'ignore': texts[i] == '###',
                'text': texts[i]
            })

        data['polys'] = line_polys



class MakeBorderMap(DataProcess):
    r'''
    Making the border map from detection data with ICDAR format.
    Typically following the process of class `MakeICDARData`.
    '''

    def __init__(self, *args, **kwargs):
        self.shrink_ratio = 0.4
        self.thresh_min = 0.3
        self.thresh_max = 0.7

    def process(self, data, *args, **kwargs):
        r'''
        required keys:
            image, polygons, ignore_tags
        adding keys:
            thresh_map, thresh_mask
        '''
        image = data['image']
        polygons = data['polygons']
        ignore_tags = data['ignore_tags']
        canvas = np.zeros(image.shape[:2], dtype=np.float32)
        mask = np.zeros(image.shape[:2], dtype=np.float32)

        for i in range(len(polygons)):
            if ignore_tags[i]:
                continue
            self.draw_border_map(polygons[i], canvas, mask=mask)
        canvas = canvas * (self.thresh_max - self.thresh_min) + self.thresh_min
        data['thresh_map'] = canvas
        data['thresh_mask'] = mask
        return data

    def draw_border_map(self, polygon, canvas, mask):
        polygon = np.array(polygon)
        assert polygon.ndim == 2
        assert polygon.shape[1] == 2

        polygon_shape = Polygon(polygon)
        distance = polygon_shape.area * \
            (1 - np.power(self.shrink_ratio, 2)) / polygon_shape.length
        subject = [tuple(lp) for lp in polygon]
        padding = pyclipper.PyclipperOffset()
        padding.AddPath(subject, pyclipper.JT_ROUND,
                        pyclipper.ET_CLOSEDPOLYGON)
        padded_polygon = np.array(padding.Execute(distance)[0])
        cv2.fillPoly(mask, [padded_polygon.astype(np.int32)], 1.0)

        xmin = padded_polygon[:, 0].min()
        xmax = padded_polygon[:, 0].max()
        ymin = padded_polygon[:, 1].min()
        ymax = padded_polygon[:, 1].max()
        width = xmax - xmin + 1
        height = ymax - ymin + 1

        polygon[:, 0] = polygon[:, 0] - xmin
        polygon[:, 1] = polygon[:, 1] - ymin

        xs = np.broadcast_to(
            np.linspace(0, width - 1, num=width).reshape(1, width),
            (height, width))
        ys = np.broadcast_to(
            np.linspace(0, height - 1, num=height).reshape(height, 1),
            (height, width))

        distance_map = np.zeros((polygon.shape[0], height, width),
                                dtype=np.float32)
        for i in range(polygon.shape[0]):
            j = (i + 1) % polygon.shape[0]
            absolute_distance = self.distance(xs, ys, polygon[i], polygon[j])
            distance_map[i] = np.clip(absolute_distance / distance, 0, 1)
        distance_map = distance_map.min(axis=0)

        xmin_valid = min(max(0, xmin), canvas.shape[1] - 1)
        xmax_valid = min(max(0, xmax), canvas.shape[1] - 1)
        ymin_valid = min(max(0, ymin), canvas.shape[0] - 1)
        ymax_valid = min(max(0, ymax), canvas.shape[0] - 1)
        canvas[ymin_valid:ymax_valid + 1, xmin_valid:xmax_valid + 1] = np.fmax(
            1 - distance_map[ymin_valid - ymin:ymax_valid - ymax + height,
                             xmin_valid - xmin:xmax_valid - xmax + width],
            canvas[ymin_valid:ymax_valid + 1, xmin_valid:xmax_valid + 1])

    def distance(self, xs, ys, point_1, point_2):
        '''
        compute the distance from point to a line
        ys: coordinates in the first axis
        xs: coordinates in the second axis
        point_1, point_2: (x, y), the end of the line
        '''
        height, width = xs.shape[:2]
        square_distance_1 = np.square(xs
                                      - point_1[0]) + np.square(ys
                                                                - point_1[1])
        square_distance_2 = np.square(xs
                                      - point_2[0]) + np.square(ys
                                                                - point_2[1])
        square_distance = np.square(point_1[0]
                                    - point_2[0]) + np.square(point_1[1]
                                                              - point_2[1])

        cosin = (square_distance - square_distance_1 - square_distance_2) / \
            (2 * np.sqrt(square_distance_1 * square_distance_2))
        square_sin = 1 - np.square(cosin)
        square_sin = np.nan_to_num(square_sin)
        result = np.sqrt(square_distance_1 * square_distance_2
                         * np.abs(square_sin) / (square_distance + 1e-6))

        result[cosin < 0] = np.sqrt(
            np.fmin(square_distance_1, square_distance_2))[cosin < 0]
        # self.extend_line(point_1, point_2, result)
        return result

    def extend_line(self, point_1, point_2, result):
        ex_point_1 = (
            int(
                round(point_1[0]
                      + (point_1[0] - point_2[0]) * (1 + self.shrink_ratio))),
            int(
                round(point_1[1]
                      + (point_1[1] - point_2[1]) * (1 + self.shrink_ratio))))
        cv2.line(
            result,
            tuple(ex_point_1),
            tuple(point_1),
            4096.0,
            1,
            lineType=cv2.LINE_AA,
            shift=0)
        ex_point_2 = (
            int(
                round(point_2[0]
                      + (point_2[0] - point_1[0]) * (1 + self.shrink_ratio))),
            int(
                round(point_2[1]
                      + (point_2[1] - point_1[1]) * (1 + self.shrink_ratio))))
        cv2.line(
            result,
            tuple(ex_point_2),
            tuple(point_2),
            4096.0,
            1,
            lineType=cv2.LINE_AA,
            shift=0)
        return ex_point_1, ex_point_2



class MakeICDARData(DataProcess):

    def __init__(self, debug=False, **kwargs):
        self.shrink_ratio = 0.4
        self.debug = debug

    def process(self, data):
        polygons = []
        ignore_tags = []
        annotations = data['polys']
        for annotation in annotations:
            polygons.append(np.array(annotation['points']))
            ignore_tags.append(annotation['ignore'])
        ignore_tags = np.array(ignore_tags, dtype=np.uint8)
        filename = data.get('filename', data['data_id'])
        if self.debug:
            self.draw_polygons(data['image'], polygons, ignore_tags)
        shape = np.array(data['shape'])
        return OrderedDict(
            image=data['image'],
            polygons=polygons,
            ignore_tags=ignore_tags,
            shape=shape,
            filename=filename,
            is_training=data['is_training'])

    def draw_polygons(self, image, polygons, ignore_tags):
        for i in range(len(polygons)):
            polygon = polygons[i].reshape(-1, 2).astype(np.int32)
            ignore = ignore_tags[i]
            if ignore:
                color = (255, 0, 0)  # depict ignorable polygons in blue
            else:
                color = (0, 0, 255)  # depict polygons in red

            cv2.polylines(image, [polygon], True, color, 1)

    polylines = staticmethod(draw_polygons)


class ICDARCollectFN():

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, batch):
        data_dict = OrderedDict()
        for sample in batch:
            for k, v in sample.items():
                if k not in data_dict:
                    data_dict[k] = []
                if isinstance(v, np.ndarray):
                    v = torch.from_numpy(v)
                data_dict[k].append(v)
        data_dict['image'] = torch.stack(data_dict['image'], 0)
        return data_dict



class MakeSegDetectionData(DataProcess):
    r'''
    Making binary mask from detection data with ICDAR format.
    Typically following the process of class `MakeICDARData`.
    '''

    def __init__(self, **kwargs):
        self.min_text_size = 6
        self.shrink_ratio = 0.4

    def process(self, data):
        '''
        requied keys:
            image, polygons, ignore_tags, filename
        adding keys:
            mask
        '''
        image = data['image']
        polygons = data['polygons']
        ignore_tags = data['ignore_tags']
        image = data['image']
        filename = data['filename']

        h, w = image.shape[:2]
        if data['is_training']:
            polygons, ignore_tags = self.validate_polygons(
                polygons, ignore_tags, h, w)
        gt = np.zeros((1, h, w), dtype=np.float32)
        mask = np.ones((h, w), dtype=np.float32)

        for i in range(len(polygons)):
            polygon = polygons[i]
            height = max(polygon[:, 1]) - min(polygon[:, 1])
            width = max(polygon[:, 0]) - min(polygon[:, 0])
            if ignore_tags[i] or min(height, width) < self.min_text_size:
                cv2.fillPoly(mask,
                             polygon.astype(np.int32)[np.newaxis, :, :], 0)
                ignore_tags[i] = True
            else:
                polygon_shape = Polygon(polygon)
                distance = polygon_shape.area * \
                    (1 - np.power(self.shrink_ratio, 2)) / polygon_shape.length
                subject = [tuple(lp) for lp in polygons[i]]
                padding = pyclipper.PyclipperOffset()
                padding.AddPath(subject, pyclipper.JT_ROUND,
                                pyclipper.ET_CLOSEDPOLYGON)
                shrinked = padding.Execute(-distance)
                if shrinked == []:
                    cv2.fillPoly(mask,
                                 polygon.astype(np.int32)[np.newaxis, :, :], 0)
                    ignore_tags[i] = True
                    continue
                shrinked = np.array(shrinked[0]).reshape(-1, 2)
                cv2.fillPoly(gt[0], [shrinked.astype(np.int32)], 1)

        if filename is None:
            filename = ''
        data.update(
            image=image,
            polygons=polygons,
            gt=gt,
            mask=mask,
            filename=filename)
        return data

    def validate_polygons(self, polygons, ignore_tags, h, w):
        '''
        polygons (numpy.array, required): of shape (num_instances, num_points, 2)
        '''
        if len(polygons) == 0:
            return polygons, ignore_tags
        assert len(polygons) == len(ignore_tags)
        for polygon in polygons:
            polygon[:, 0] = np.clip(polygon[:, 0], 0, w - 1)
            polygon[:, 1] = np.clip(polygon[:, 1], 0, h - 1)

        for i in range(len(polygons)):
            area = self.polygon_area(polygons[i])
            if abs(area) < 1:
                ignore_tags[i] = True
            if area > 0:
                polygons[i] = polygons[i][::-1, :]
        return polygons, ignore_tags

    def polygon_area(self, polygon):
        edge = 0
        for i in range(polygon.shape[0]):
            next_index = (i + 1) % polygon.shape[0]
            edge += (polygon[next_index, 0] - polygon[i, 0]) * (
                polygon[next_index, 1] + polygon[i, 1])

        return edge / 2.



class NormalizeImage(DataProcess):
    RGB_MEAN = np.array([122.67891434, 116.66876762, 104.00698793])

    def process(self, data):
        assert 'image' in data, '`image` in data is required by this process'
        image = data['image']
        image -= self.RGB_MEAN
        image /= 255.
        image = torch.from_numpy(image).permute(2, 0, 1).float()
        data['image'] = image
        return data

    @classmethod
    def restore(self, image):
        image = image.permute(1, 2, 0).to('cpu').numpy()
        image = image * 255.
        image += self.RGB_MEAN
        image = image.astype(np.uint8)
        return image


class RandomCropData(DataProcess):
    # random crop algorithm similar to https://github.com/argman/EAST

    def __init__(self, cfg):
        self.size = cfg.size
        self.max_tries = cfg.max_tries
        self.min_crop_side_ratio = 0.1
        self.require_original_image = False

    def process(self, data):

        size = self.size

        img = data['image']
        ori_img = img
        ori_lines = data['polys']

        all_care_polys = [
            line['points'] for line in data['polys'] if not line['ignore']
        ]
        crop_x, crop_y, crop_w, crop_h = self.crop_area(img, all_care_polys)
        scale_w = size[0] / crop_w
        scale_h = size[1] / crop_h
        scale = min(scale_w, scale_h)
        h = int(crop_h * scale)
        w = int(crop_w * scale)
        padimg = np.zeros((size[1], size[0], img.shape[2]), img.dtype)
        padimg[:h, :w] = cv2.resize(
            img[crop_y:crop_y + crop_h, crop_x:crop_x + crop_w], (w, h))
        img = padimg

        lines = []
        for line in data['polys']:
            poly_ori = np.array(line['points']) - (crop_x, crop_y)
            poly = (poly_ori * scale).tolist()
            if not self.is_poly_outside_rect(poly, 0, 0, w, h):
                lines.append({**line, 'points': poly})
        data['polys'] = lines

        if self.require_original_image:
            data['image'] = ori_img
        else:
            data['image'] = img
        data['lines'] = ori_lines
        data['scale_w'] = scale
        data['scale_h'] = scale

        return data

    def is_poly_in_rect(self, poly, x, y, w, h):
        poly = np.array(poly)
        if poly[:, 0].min() < x or poly[:, 0].max() > x + w:
            return False
        if poly[:, 1].min() < y or poly[:, 1].max() > y + h:
            return False
        return True

    def is_poly_outside_rect(self, poly, x, y, w, h):
        poly = np.array(poly)
        if poly[:, 0].max() < x or poly[:, 0].min() > x + w:
            return True
        if poly[:, 1].max() < y or poly[:, 1].min() > y + h:
            return True
        return False

    def split_regions(self, axis):
        regions = []
        min_axis = 0
        for i in range(1, axis.shape[0]):
            if axis[i] != axis[i - 1] + 1:
                region = axis[min_axis:i]
                min_axis = i
                regions.append(region)
        return regions

    def random_select(self, axis, max_size):
        xx = np.random.choice(axis, size=2)
        xmin = np.min(xx)
        xmax = np.max(xx)
        xmin = np.clip(xmin, 0, max_size - 1)
        xmax = np.clip(xmax, 0, max_size - 1)
        return xmin, xmax

    def region_wise_random_select(self, regions, max_size):
        selected_index = list(np.random.choice(len(regions), 2))
        selected_values = []
        for index in selected_index:
            axis = regions[index]
            xx = int(np.random.choice(axis, size=1))
            selected_values.append(xx)
        xmin = min(selected_values)
        xmax = max(selected_values)
        return xmin, xmax

    def crop_area(self, img, polys):
        h, w, _ = img.shape
        h_array = np.zeros(h, dtype=np.int32)
        w_array = np.zeros(w, dtype=np.int32)
        for points in polys:
            points = np.round(points, decimals=0).astype(np.int32)
            minx = np.min(points[:, 0])
            maxx = np.max(points[:, 0])
            w_array[minx:maxx] = 1
            miny = np.min(points[:, 1])
            maxy = np.max(points[:, 1])
            h_array[miny:maxy] = 1
        # ensure the cropped area not across a text
        h_axis = np.where(h_array == 0)[0]
        w_axis = np.where(w_array == 0)[0]

        if len(h_axis) == 0 or len(w_axis) == 0:
            return 0, 0, w, h

        h_regions = self.split_regions(h_axis)
        w_regions = self.split_regions(w_axis)

        for i in range(self.max_tries):
            if len(w_regions) > 1:
                xmin, xmax = self.region_wise_random_select(w_regions, w)
            else:
                xmin, xmax = self.random_select(w_axis, w)
            if len(h_regions) > 1:
                ymin, ymax = self.region_wise_random_select(h_regions, h)
            else:
                ymin, ymax = self.random_select(h_axis, h)

            if xmax - xmin < self.min_crop_side_ratio * w or ymax - ymin < self.min_crop_side_ratio * h:
                # area too small
                continue
            num_poly_in_rect = 0
            for poly in polys:
                if not self.is_poly_outside_rect(poly, xmin, ymin, xmax - xmin,
                                                 ymax - ymin):
                    num_poly_in_rect += 1
                    break

            if num_poly_in_rect > 0:
                return xmin, ymin, xmax - xmin, ymax - ymin

        return 0, 0, w, h
