import copy
import json
import datetime
import logging
from uuid import uuid4
import time

import cv_utils
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytz
import tqdm

logger = logging.getLogger(__name__)


class GeomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Geom):
            obj_dict = obj.__dict__
            obj_dict["geom_type"] = obj.__class__.__name__
            return obj_dict
        if isinstance(obj, np.ndarray):
            try:
                obj = np.where(np.isnan(obj), None, obj)
            except:
                pass
            return obj.tolist()
        if isinstance(obj, datetime.datetime):
            return obj.astimezone(datetime.timezone.utc).isoformat()
        return json.JSONEncoder.default(self, obj)


class Geom:
    def __init__(
        self,
        coordinates=None,
        coordinate_indices=None,
        time_index=None,
        start_time=None,
        frames_per_second=None,
        num_frames=None,
        frame_width=None,
        frame_height=None,
        id=None,
        source_type=None,
        source_id=None,
        source_name=None,
        object_type=None,
        object_id=None,
        object_name=None,
    ):
        if coordinates is not None:
            try:
                coordinates = np.array(coordinates)
            except:
                raise ValueError("Coordinates for geom must be array-like")
            if coordinates.ndim > 3:
                raise ValueError("Coordinates for geom must be of dimension 3 or less")
            while coordinates.ndim < 3:
                coordinates = np.expand_dims(coordinates, axis=0)
        if time_index is not None:
            # Ragged time index
            try:
                time_index = np.array(time_index)
            except:
                raise ValueError("Time index must be array-like")
            if time_index.ndim != 1:
                raise ValueError("Time index must be one-dimensional")
            time_index_sort_order = np.argsort(time_index)
            time_index = time_index[time_index_sort_order]
            calculated_num_frames = time_index.shape[0]
            if coordinates is not None:
                if coordinates.shape[0] != calculated_num_frames:
                    raise ValueError(
                        "First dimension of coordinates array must be of same length as time index"
                    )
                coordinates = coordinates.take(time_index_sort_order, axis=0)
        elif (
            time_index is None
            and start_time is not None
            and frames_per_second is not None
            and num_frames is not None
        ):
            # Regular time index
            frames_per_second = float(frames_per_second)
            num_frames = int(round(num_frames))
        elif (
            time_index is None
            and start_time is None
            and frames_per_second is None
            and num_frames is None
        ):
            # No time index
            pass
        else:
            raise ValueError(
                "Must specify time index or all of start time/fps/number of frames or neither"
            )
        if id is None:
            id = uuid4().hex
        self.coordinates = coordinates
        self.coordinate_indices = coordinate_indices
        self.time_index = time_index
        self.start_time = start_time
        self.frames_per_second = frames_per_second
        self.num_frames = num_frames
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.id = id
        self.source_type = source_type
        self.source_id = source_id
        self.source_name = source_name
        self.object_type = object_type
        self.object_id = object_id
        self.object_name = object_name

    def to_json(self, indent=None):
        num_timesteps = self.coordinates.shape[0]
        num_points_per_timestep = self.coordinates.shape[1]
        num_points = num_timesteps * num_points_per_timestep
        logger.info(
            "Creating JSON for {} timesteps times {} points for a total of {} points".format(
                num_timesteps, num_points_per_timestep, num_points
            )
        )
        process_start_time = time.time()
        json_output = json.dumps(self, cls=GeomJSONEncoder, indent=indent)
        process_time_elapsed = time.time() - process_start_time
        logger.info(
            "Created JSON for {} points in {:.1f} seconds ({:.1f} microseconds per point)".format(
                num_points,
                process_time_elapsed,
                10**6 * process_time_elapsed / num_points,
            )
        )
        return json_output

    def resample(
        self,
        new_time_index=None,
        new_start_time=None,
        new_frames_per_second=None,
        new_num_frames=None,
        method="interpolate",
        progress_bar=False,
        notebook=False,
    ):
        if method not in ["interpolate", "fill"]:
            raise ValueError(
                "Available resampling methods are 'interpolate' and 'fill'"
            )
        if new_time_index is not None:
            # New ragged time index
            try:
                new_time_index = np.array(new_time_index)
            except:
                raise ValueError("New time index must be array-like")
            if new_time_index.ndim != 1:
                raise ValueError("New time index must be one-dimensional")
            new_time_index.sort()
            calculated_new_num_frames = new_time_index.shape[0]
            calculated_new_time_index = new_time_index
        elif (
            new_time_index is None
            and new_start_time is not None
            and new_frames_per_second is not None
            and new_num_frames is not None
        ):
            # New regular time index
            new_frames_per_second = float(new_frames_per_second)
            new_num_frames = int(round(new_num_frames))
            new_time_between_frames = datetime.timedelta(
                microseconds=int(round(10**6 / new_frames_per_second))
            )
            calculated_new_time_index = [
                new_start_time + i * new_time_between_frames
                for i in range(new_num_frames)
            ]
            calculated_new_num_frames = new_num_frames
        else:
            raise ValueError(
                "Must specify time index or all of start time/fps/number of frames"
            )
        if (
            self.time_index is None
            and self.start_time is None
            and self.frames_per_second is None
            and self.num_frames is None
        ):
            # No old time index
            new_geom = copy.deepcopy(self)
            new_geom.time_index = new_time_index
            new_geom.start_time = new_start_time
            new_geom.frames_per_second = new_frames_per_second
            new_geom.num_frames = new_num_frames
            new_geom.coordinates = np.tile(
                self.coordinates, (calculated_new_num_frames, 1, 1)
            )
            return new_geom
        elif (
            self.time_index is None
            and self.start_time is not None
            and self.frames_per_second is not None
            and self.num_frames is not None
        ):
            old_time_between_frames = datetime.timedelta(
                microseconds=int(round(10**6 / self.frames_per_second))
            )
            old_time_index = [
                self.start_time + i * old_time_between_frames
                for i in range(self.num_frames)
            ]
        elif self.time_index is not None:
            old_time_index = self.time_index
        else:
            raise ValueError(
                "Current time index is malformed. Must include time index or all of start time/fps/number of frames or neither."
            )
        coordinates_time_slice_shape = self.coordinates.shape[1:]
        new_coordinates_shape = (
            calculated_new_num_frames,
        ) + coordinates_time_slice_shape
        new_coordinates = np.full(new_coordinates_shape, np.nan)
        old_time_index_pointer = 0
        new_time_index_iterable = range(calculated_new_num_frames)
        if progress_bar:
            if notebook:
                new_time_index_iterable = tqdm.tqdm_notebook(new_time_index_iterable)
            else:
                new_time_index_iterable = tqdm.tqdm(new_time_index_iterable)
        for new_time_index_pointer in new_time_index_iterable:
            if (
                calculated_new_time_index[new_time_index_pointer]
                < old_time_index[old_time_index_pointer]
            ):
                continue
            if calculated_new_time_index[new_time_index_pointer] > old_time_index[-1]:
                continue
            while (
                calculated_new_time_index[new_time_index_pointer]
                > old_time_index[old_time_index_pointer + 1]
            ):
                old_time_index_pointer += 1
            if method == "interpolate":
                later_slice_weight = (
                    calculated_new_time_index[new_time_index_pointer]
                    - old_time_index[old_time_index_pointer]
                ) / (
                    old_time_index[old_time_index_pointer + 1]
                    - old_time_index[old_time_index_pointer]
                )
                earlier_slice_weight = 1.0 - later_slice_weight
            else:
                earlier_slice_weight = 1.0
                later_slice_weight = 0.0
            if earlier_slice_weight == 0.0:
                new_coordinates[new_time_index_pointer] = self.coordinates[
                    old_time_index_pointer + 1
                ]
            elif later_slice_weight == 0.0:
                new_coordinates[new_time_index_pointer] = self.coordinates[
                    old_time_index_pointer
                ]
            else:
                new_coordinates[new_time_index_pointer] = (
                    earlier_slice_weight * self.coordinates[old_time_index_pointer]
                    + later_slice_weight * self.coordinates[old_time_index_pointer + 1]
                )
        new_geom = copy.deepcopy(self)
        new_geom.time_index = new_time_index
        new_geom.start_time = new_start_time
        new_geom.frames_per_second = new_frames_per_second
        new_geom.num_frames = new_num_frames
        new_geom.coordinates = new_coordinates
        return new_geom


class Geom2D(Geom):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.coordinates is not None and self.coordinates.shape[-1] != 2:
            raise ValueError("For 2D geoms, size of last dimension must be 2")

    def plot_matplotlib(
        self,
        frame_index,
        image_size=None,
        background_image=None,
        background_alpha=None,
        show_axes=True,
        show=True,
    ):
        if image_size is None and background_image is not None:
            image_size = np.array(
                [background_image.shape[1], background_image.shape[0]]
            )
        fig, axes = plt.subplots()
        self.draw_matplotlib(axes, frame_index)
        cv_utils.format_2d_image_plot(image_size, show_axes)
        if background_image is not None:
            cv_utils.draw_background_image(background_image, background_alpha)
        if show:
            plt.show()

    def overlay_video(
        self,
        input_path,
        output_path,
        start_time=None,
        include_timestamp=False,
        progress_bar=False,
        notebook=False,
    ):
        video_input = cv_utils.VideoInput(input_path=input_path, start_time=start_time)
        if self.time_index is not None:
            video_start_time = video_input.video_parameters.start_time
            video_fps = video_input.video_parameters.fps
            video_frame_count = video_input.video_parameters.frame_count
            if (
                video_start_time is None
                or video_fps is None
                or video_frame_count is None
            ):
                raise ValueError(
                    "Video must have start time, FPS, and frame count info to overlay geom sequence"
                )

            video_output = cv_utils.VideoOutput(
                output_path, video_parameters=video_input.video_parameters
            )
            if progress_bar:
                if notebook:
                    t = tqdm.tqdm_notebook(total=video_frame_count)
                else:
                    t = tqdm.tqdm(total=video_frame_count)
            for frame_index in range(video_frame_count):
                frame = video_input.get_frame()
                if frame is None:
                    raise ValueError(
                        "Input video ended unexpectedly at frame number {}".format(
                            frame_index
                        )
                    )
                if frame_index < self.time_index.shape[0]:
                    frame = self.draw_opencv(image=frame, frame_index=frame_index)
                    if include_timestamp:
                        frame = cv_utils.draw_timestamp(
                            original_image=frame,
                            timestamp=self.time_index[frame_index],
                            box_alpha=0.6,
                        )
                video_output.write_frame(frame)
                if progress_bar:
                    t.update()
        else:
            video_output = cv_utils.VideoOutput(
                output_path, video_parameters=video_input.video_parameters
            )
            if progress_bar:
                if notebook:
                    t = tqdm.tqdm_notebook(
                        total=video_input.video_parameters.frame_count
                    )
                else:
                    t = tqdm.tqdm(total=video_input.video_parameters.frame_count)
            frame_count_stream = 0
            while video_input.is_opened():
                frame = video_input.get_frame()
                if frame is not None:
                    frame_count_stream += 1
                    frame = self.draw_opencv(frame, frame_index=frame_count_stream)
                    video_output.write_frame(frame)
                    if progress_bar:
                        t.update()
                else:
                    break
            if video_input.video_parameters.frame_count is not None and int(
                frame_count_stream
            ) != int(video_input.video_parameters.frame_count):
                logger.warning(
                    "Expected {} frames but got {} frames".format(
                        int(video_input.video_parameters.frame_count),
                        int(frame_count_stream),
                    )
                )
        video_input.close()
        video_output.close()
        if progress_bar:
            t.close()


class Geom3D(Geom):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.coordinates is not None and self.coordinates.shape[-1] != 3:
            raise ValueError("For 3D geoms, size of last dimension must be 3")

    def project_coordinates(
        self,
        rotation_vector,
        translation_vector,
        camera_matrix,
        distortion_coefficients,
        frame_width=None,
        frame_height=None,
    ):
        num_timesteps = self.coordinates.shape[0]
        num_points_per_timestep = self.coordinates.shape[1]
        num_points = num_timesteps * num_points_per_timestep
        logger.info(
            "Projecting {} timesteps times {} points for a total of {} points".format(
                num_timesteps, num_points_per_timestep, num_points
            )
        )
        process_start_time = time.time()
        image_corners = None
        if frame_width is not None and frame_height is not None:
            image_corners = [[0, 0], [frame_width, frame_height]]

        logger.info(f"Coord: {self.coordinates.reshape((-1, 3))}")
        logger.info(f"RV: {rotation_vector}")
        logger.info(f"TV: {translation_vector}")
        logger.info(f"CM: {camera_matrix}")
        logger.info(f"DC: {distortion_coefficients}")
        logger.info(f"IC: {image_corners}")

        new_coordinates_flattened = cv_utils.project_points(
            self.coordinates.reshape((-1, 3)),
            rotation_vector,
            translation_vector,
            camera_matrix,
            distortion_coefficients,
            remove_behind_camera=True,
            remove_outside_frame=True,
            image_corners=image_corners,
        )
        new_coordinates = new_coordinates_flattened.reshape(
            (num_timesteps, num_points_per_timestep, 2)
        )
        process_time_elapsed = time.time() - process_start_time
        logger.info(
            "Projected {} points in {:.1f} seconds ({:.1f} microseconds per point)".format(
                num_points,
                process_time_elapsed,
                10**6 * process_time_elapsed / num_points,
            )
        )
        return new_coordinates


class GeomCollection(Geom):
    def __init__(self, geom_list=None, **kwargs):
        super().__init__(**kwargs)
        self.geom_list = geom_list

    @classmethod
    def from_geom_list(
        cls,
        geom_list,
        start_time,
        end_time,
        frames_per_second,
        method="interpolate",
        progress_bar=False,
        notebook=False,
    ):
        num_spatial_dimensions = geom_list[0].coordinates.shape[-1]
        frame_width = geom_list[0].frame_width
        frame_height = geom_list[0].frame_height
        new_num_points = 0
        new_timestamp_set = set()

        rounded_time_index = pd.date_range(
            start=start_time,
            end=end_time,
            freq=f"{round(1/frames_per_second * 1000, 2)}L",
            inclusive="left",
        )
        rounded_time_index = rounded_time_index.tz_convert(
            tz=pytz.utc
        ).to_pydatetime()  # Convert to UTC and a numpy array with python Datetimes
        new_time_indexes = []

        for geom in geom_list:
            this_geom_timestamp_set = None
            if geom.coordinates.shape[-1] != num_spatial_dimensions:
                raise ValueError(
                    "All geoms in list must have the same number of spatial_dimensions"
                )
            if geom.frame_width is not None and geom.frame_width != frame_width:
                raise ValueError(
                    "All geoms in list must have the same frame width (if specified)"
                )
            if geom.frame_height is not None and geom.frame_height != frame_height:
                raise ValueError(
                    "All geoms in list must have the same frame height (if specified)"
                )
            if geom.time_index is not None:
                this_geom_timestamp_set = geom.time_index
                new_timestamp_set = new_timestamp_set.union(this_geom_timestamp_set)
            elif (
                geom.time_index is None
                and geom.start_time is not None
                and geom.frames_per_second is not None
                and geom.num_frames is not None
            ):
                time_between_frames = datetime.timedelta(
                    microseconds=int(round(10**6 / geom.frames_per_second))
                )
                calculated_time_index = [
                    geom.start_time + i * time_between_frames
                    for i in range(geom.num_frames)
                ]
                this_geom_timestamp_set = calculated_time_index
                new_timestamp_set = new_timestamp_set.union(this_geom_timestamp_set)
            elif (
                geom.time_index is None
                and geom.start_time is None
                and geom.frames_per_second is None
                and geom.num_frames is None
            ):
                pass
            else:
                raise ValueError(
                    "One of the geoms in the list has a malformed time index. Must include time index or all of start time/fps/number of frames or neither"
                )

            new_num_points += geom.coordinates.shape[1]
            new_time_indexes.append(this_geom_timestamp_set)

        new_calculated_num_frames = len(rounded_time_index)
        new_coordinates = np.full(
            (new_calculated_num_frames, new_num_points, num_spatial_dimensions), np.nan
        )
        new_geom_list = list()
        new_coordinates_point_index = 0
        if progress_bar:
            if notebook:
                geom_list = tqdm.tqdm_notebook(geom_list)
            else:
                geom_list = tqdm.tqdm(geom_list)
        for idx, geom in enumerate(geom_list):
            all_timestamps_list = list(
                set(rounded_time_index).union(new_time_indexes[idx])
            )

            all_timestamps_mapped_to_nan = pd.Series(
                np.full(
                    (
                        len(all_timestamps_list),
                        3,
                    ),
                    np.nan,
                ).tolist(),
                index=all_timestamps_list,
            )
            geom_timestamps_mapped_to_coordinates = pd.Series(
                geom.coordinates.reshape(
                    (
                        len(geom.time_index),
                        3,
                    )
                ).tolist(),
                index=geom.time_index,
            )
            all_timestamps_mapped_to_coordinates = (
                geom_timestamps_mapped_to_coordinates.combine_first(
                    all_timestamps_mapped_to_nan
                ).sort_index(ascending=True)
            )

            df_coordinates = pd.DataFrame(
                np.array(all_timestamps_mapped_to_coordinates.to_list()),
                index=all_timestamps_mapped_to_coordinates.index,
                columns=["x", "y", "z"],
            )
            df_coordinates = df_coordinates.interpolate(
                method="time", limit=10, limit_direction="both"
            )
            df_coordinates = df_coordinates[
                df_coordinates.index.isin(rounded_time_index)
            ]
            np_new_coordinates = df_coordinates.to_numpy().reshape(
                (len(df_coordinates), 1, 3)
            )

            new_geom = copy.deepcopy(geom)
            new_geom.time_index = df_coordinates.index.to_numpy()
            new_geom.start_time = start_time
            new_geom.frames_per_second = frames_per_second
            new_geom.frame_width = frame_width
            new_geom.frame_height = frame_height
            new_geom.num_frames = np_new_coordinates.shape[0]
            new_geom.coordinates = np_new_coordinates

            num_points = new_geom.coordinates.shape[1]
            new_coordinates[
                :,
                new_coordinates_point_index : (
                    new_coordinates_point_index + num_points
                ),
                :,
            ] = new_geom.coordinates

            if isinstance(geom, GeomCollection):
                for sub_geom in geom.geom_list:
                    new_sub_geom = copy.deepcopy(sub_geom)
                    new_sub_geom.time_index = new_geom.time_index
                    new_sub_geom.start_time = new_geom.start_time
                    new_sub_geom.frames_per_second = new_geom.frames_per_second
                    new_sub_geom.num_frames = new_geom.num_frames
                    new_sub_geom.coordinate_indices = [
                        coordinate_index + new_coordinates_point_index
                        for coordinate_index in new_sub_geom.coordinate_indices
                    ]
                    new_geom_list.append(new_sub_geom)
            else:
                new_geom.coordinate_indices = [
                    coordinate_index + new_coordinates_point_index
                    for coordinate_index in range(num_points)
                ]
                new_geom_list.append(new_geom)

            new_coordinates_point_index += num_points
        return cls(
            time_index=rounded_time_index,
            coordinates=new_coordinates,
            geom_list=new_geom_list,
            frame_width=frame_width,
            frame_height=frame_height,
        )


class Circle(Geom):
    def __init__(
        self, radius=6, line_width=1.5, color="#00ff00", fill=True, alpha=1.0, **kwargs
    ):
        super().__init__(**kwargs)
        self.radius = radius
        self.line_width = line_width
        self.color = color
        self.fill = fill
        self.alpha = alpha


class Point(Geom):
    def __init__(self, marker=".", size=6, color="#00ff00", alpha=1.0, **kwargs):
        super().__init__(**kwargs)
        self.marker = marker
        self.size = size
        self.color = color
        self.alpha = alpha


class Line(Geom):
    def __init__(self, line_width=1.5, color="#00ff00", alpha=1.0, **kwargs):
        super().__init__(**kwargs)
        self.line_width = line_width
        self.color = color
        self.alpha = alpha


class Text(Geom):
    def __init__(
        self,
        text=None,
        color="#00ff00",
        alpha=1.0,
        horizontal_alignment="center",
        vertical_alignment="bottom",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.text = text
        self.color = color
        self.alpha = alpha
        self.horizontal_alignment = horizontal_alignment
        self.vertical_alignment = vertical_alignment


class GeomCollection2D(Geom2D, GeomCollection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def draw_matplotlib(self, axis, frame_index):
        for geom_index, geom in enumerate(self.geom_list):
            geom.coordinates = self.coordinates.take(geom.coordinate_indices, 1)
            geom.draw_matplotlib(axis, frame_index)

    def draw_opencv(self, image, frame_index):
        for geom_index, geom in enumerate(self.geom_list):
            geom.coordinates = self.coordinates.take(geom.coordinate_indices, 1)
            image = geom.draw_opencv(image, frame_index)
        return image


class GeomCollection3D(Geom3D, GeomCollection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def project(
        self,
        rotation_vector,
        translation_vector,
        camera_matrix,
        distortion_coefficients,
        frame_width=None,
        frame_height=None,
    ):
        new_coordinates = None
        if self.coordinates is not None:
            new_coordinates = self.project_coordinates(
                rotation_vector=rotation_vector,
                translation_vector=translation_vector,
                camera_matrix=camera_matrix,
                distortion_coefficients=distortion_coefficients,
                frame_width=frame_width,
                frame_height=frame_height,
            )

        new_geom_list = [
            geom.project(
                rotation_vector=rotation_vector,
                translation_vector=translation_vector,
                camera_matrix=camera_matrix,
                distortion_coefficients=distortion_coefficients,
                frame_width=frame_width,
                frame_height=frame_height,
            )
            for geom in self.geom_list
        ]
        return GeomCollection2D(
            coordinates=new_coordinates,
            geom_list=new_geom_list,
            time_index=self.time_index,
            start_time=self.start_time,
            frames_per_second=self.frames_per_second,
            num_frames=self.num_frames,
            frame_width=frame_width,
            frame_height=frame_height,
        )


class Circle2D(Geom2D, Circle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def draw_matplotlib(self, axis, frame_index):
        if self.coordinates.shape[1:] != (1, 2):
            raise ValueError(
                "Draw method for Circle2D requires coordinates to be of shape (N, 1, 2)"
            )

        coordinates = self.coordinates[frame_index][0]

        if np.any(np.isnan(coordinates)):
            return

        axis.add_artist(
            plt.Circle(
                xy=coordinates,
                radius=self.radius,
                linewidth=self.line_width,
                edgecolor=self.color,
                fill=self.fill,
                facecolor=self.color,
                alpha=self.alpha,
            )
        )

    def draw_opencv(self, image, frame_index):
        if self.coordinates.shape[1:] != (1, 2):
            raise ValueError(
                "Draw method for Circle2D requires coordinates to be of shape (N, 1, 2)"
            )

        coordinates = self.coordinates[frame_index][0]

        if np.any(np.isnan(coordinates)):
            return image

        new_image = cv_utils.draw_circle(
            image,
            coordinates=coordinates,
            radius=self.radius,
            line_width=self.line_width,
            color=self.color,
            fill=self.fill,
            alpha=self.alpha,
        )
        return new_image


class Circle3D(Geom3D, Circle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def project(
        self,
        rotation_vector,
        translation_vector,
        camera_matrix,
        distortion_coefficients,
        frame_width=None,
        frame_height=None,
    ):
        new_coordinates = None
        if self.coordinates is not None:
            new_coordinates = self.project_coordinates(
                rotation_vector=rotation_vector,
                translation_vector=translation_vector,
                camera_matrix=camera_matrix,
                distortion_coefficients=distortion_coefficients,
                frame_width=frame_width,
                frame_height=frame_height,
            )
        return Circle2D(
            coordinates=new_coordinates,
            coordinate_indices=self.coordinate_indices,
            time_index=self.time_index,
            start_time=self.start_time,
            frames_per_second=self.frames_per_second,
            num_frames=self.num_frames,
            radius=self.radius,
            line_width=self.line_width,
            color=self.color,
            fill=self.fill,
            alpha=self.alpha,
            id=self.id,
            source_type=self.source_type,
            source_id=self.source_id,
            source_name=self.source_name,
            object_type=self.object_type,
            object_id=self.object_id,
            object_name=self.object_name,
            frame_width=frame_width,
            frame_height=frame_height,
        )


class Point2D(Geom2D, Point):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def draw_matplotlib(self, axis, frame_index):
        if self.coordinates.shape[1:] != (1, 2):
            raise ValueError(
                "Draw method for Point2D requires coordinates to be of shape (N, 1, 2)"
            )

        coordinates = self.coordinates[frame_index][0]

        if np.any(np.isnan(coordinates)):
            return

        s = None
        if self.size is not None:
            s = self.size**2
        axis.scatter(
            coordinates[0],
            coordinates[1],
            marker=self.marker,
            s=s,
            edgecolors=self.color,
            color=self.color,
            alpha=self.alpha,
        )

    def draw_opencv(self, image, frame_index):
        if self.coordinates.shape[1:] != (1, 2):
            raise ValueError(
                "Draw method for Point2D requires coordinates to be of shape (N, 1, 2)"
            )

        coordinates = self.coordinates[frame_index][0]

        if np.any(np.isnan(coordinates)):
            return image

        new_image = cv_utils.draw_point(
            image,
            coordinates=coordinates,
            marker=self.marker,
            marker_size=self.size,
            color=self.color,
            alpha=self.alpha,
        )
        return new_image


class Point3D(Geom3D, Point):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def project(
        self,
        rotation_vector,
        translation_vector,
        camera_matrix,
        distortion_coefficients,
        frame_width=None,
        frame_height=None,
    ):
        new_coordinates = None
        if self.coordinates is not None:
            new_coordinates = self.project_coordinates(
                rotation_vector=rotation_vector,
                translation_vector=translation_vector,
                camera_matrix=camera_matrix,
                distortion_coefficients=distortion_coefficients,
                frame_width=frame_width,
                frame_height=frame_height,
            )
        return Point2D(
            coordinates=new_coordinates,
            coordinate_indices=self.coordinate_indices,
            time_index=self.time_index,
            start_time=self.start_time,
            frames_per_second=self.frames_per_second,
            num_frames=self.num_frames,
            marker=self.marker,
            size=self.size,
            color=self.color,
            alpha=self.alpha,
            id=self.id,
            source_type=self.source_type,
            source_id=self.source_id,
            source_name=self.source_name,
            object_type=self.object_type,
            object_id=self.object_id,
            object_name=self.object_name,
            frame_width=frame_width,
            frame_height=frame_height,
        )


class Line2D(Geom2D, Line):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def draw_matplotlib(self, axis, frame_index):
        if self.coordinates.shape[1:] != (2, 2):
            raise ValueError(
                "Draw method for Line2D requires coordinates to be of shape (N, 2, 2)"
            )

        coordinates = self.coordinates[frame_index]

        if np.any(np.isnan(coordinates)):
            return

        axis.add_artist(
            plt.Line2D(
                (coordinates[0, 0], coordinates[1, 0]),
                (coordinates[0, 1], coordinates[1, 1]),
                linewidth=self.line_width,
                color=self.color,
                alpha=self.alpha,
            )
        )

    def draw_opencv(self, image, frame_index):
        if self.coordinates.shape[1:] != (2, 2):
            raise ValueError(
                "Draw method for Line2D requires coordinates to be of shape (N, 2, 2)"
            )

        coordinates = self.coordinates[frame_index]

        if np.any(np.isnan(coordinates)):
            return image

        new_image = cv_utils.draw_line(
            image,
            coordinates=coordinates,
            line_width=self.line_width,
            color=self.color,
            alpha=self.alpha,
        )
        return new_image


class Line3D(Geom3D, Line):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def project(
        self,
        rotation_vector,
        translation_vector,
        camera_matrix,
        distortion_coefficients,
        frame_width=None,
        frame_height=None,
    ):
        new_coordinates = None
        if self.coordinates is not None:
            new_coordinates = self.project_coordinates(
                rotation_vector=rotation_vector,
                translation_vector=translation_vector,
                camera_matrix=camera_matrix,
                distortion_coefficients=distortion_coefficients,
                frame_width=frame_width,
                frame_height=frame_height,
            )
        return Line2D(
            coordinates=new_coordinates,
            coordinate_indices=self.coordinate_indices,
            time_index=self.time_index,
            start_time=self.start_time,
            frames_per_second=self.frames_per_second,
            num_frames=self.num_frames,
            line_width=self.line_width,
            color=self.color,
            alpha=self.alpha,
            id=self.id,
            source_type=self.source_type,
            source_id=self.source_id,
            source_name=self.source_name,
            object_type=self.object_type,
            object_id=self.object_id,
            object_name=self.object_name,
            frame_width=frame_width,
            frame_height=frame_height,
        )


class Text2D(Geom2D, Text):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def draw_matplotlib(self, axis, frame_index):
        if self.coordinates.shape[1:] != (1, 2):
            raise ValueError(
                "Draw method for Text2D requires coordinates to be of shape (N, 1, 2)"
            )

        coordinates = self.coordinates[frame_index][0]

        if np.any(np.isnan(coordinates)):
            return

        axis.text(
            coordinates[0],
            coordinates[1],
            self.text,
            color=self.color,
            alpha=self.alpha,
            horizontalalignment=self.horizontal_alignment,
            verticalalignment=self.vertical_alignment,
            clip_on=True,
        )

    def draw_opencv(self, image, frame_index):
        if self.coordinates.shape[1:] != (1, 2):
            raise ValueError(
                "Draw method for Text2D requires coordinates to be of shape (N, 1, 2)"
            )

        coordinates = self.coordinates[frame_index][0]

        if np.any(np.isnan(coordinates)):
            return image

        new_image = cv_utils.draw_text(
            image,
            anchor_coordinates=coordinates,
            text=self.text,
            horizontal_alignment=self.horizontal_alignment,
            vertical_alignment=self.vertical_alignment,
            color=self.color,
            alpha=self.alpha,
        )
        return new_image


class Text3D(Geom3D, Text):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def project(
        self,
        rotation_vector,
        translation_vector,
        camera_matrix,
        distortion_coefficients,
        frame_width=None,
        frame_height=None,
    ):
        new_coordinates = None
        if self.coordinates is not None:
            new_coordinates = self.project_coordinates(
                rotation_vector=rotation_vector,
                translation_vector=translation_vector,
                camera_matrix=camera_matrix,
                distortion_coefficients=distortion_coefficients,
                frame_width=frame_width,
                frame_height=frame_height,
            )
        return Text2D(
            coordinates=new_coordinates,
            coordinate_indices=self.coordinate_indices,
            time_index=self.time_index,
            start_time=self.start_time,
            frames_per_second=self.frames_per_second,
            num_frames=self.num_frames,
            text=self.text,
            color=self.color,
            alpha=self.alpha,
            horizontal_alignment=self.horizontal_alignment,
            vertical_alignment=self.vertical_alignment,
            id=self.id,
            source_type=self.source_type,
            source_id=self.source_id,
            source_name=self.source_name,
            object_type=self.object_type,
            object_id=self.object_id,
            object_name=self.object_name,
            frame_width=frame_width,
            frame_height=frame_height,
        )
