from __future__ import annotations

from copy import deepcopy
from typing import List, Tuple

from src.plugins.camera_settings.camera_settings_data import CameraSettingsData


class CameraSettingsMapper:
    """Converts between CameraSettingsData, flat dict (SettingsView), and JSON (repo)."""

    # ── flat dict ↔ SettingsView ───────────────────────────────────────────────

    @staticmethod
    def to_flat_dict(data: CameraSettingsData) -> dict:
        """All schema fields as a flat dict — brightness_area_points excluded."""
        return {
            "index":                   data.index,
            "width":                   data.width,
            "height":                  data.height,
            "skip_frames":             data.skip_frames,
            "capture_position_offset": data.capture_position_offset,
            "contour_detection":       data.contour_detection,
            "draw_contours":           data.draw_contours,
            "threshold":               data.threshold,
            "threshold_pickup_area":   data.threshold_pickup_area,
            "epsilon":                 data.epsilon,
            "min_contour_area":        data.min_contour_area,
            "max_contour_area":        data.max_contour_area,
            "gaussian_blur":           data.gaussian_blur,
            "blur_kernel_size":        data.blur_kernel_size,
            "threshold_type":          data.threshold_type,
            "dilate_enabled":          data.dilate_enabled,
            "dilate_kernel_size":      data.dilate_kernel_size,
            "dilate_iterations":       data.dilate_iterations,
            "erode_enabled":           data.erode_enabled,
            "erode_kernel_size":       data.erode_kernel_size,
            "erode_iterations":        data.erode_iterations,
            "chessboard_width":        data.chessboard_width,
            "chessboard_height":       data.chessboard_height,
            "square_size_mm":          data.square_size_mm,
            "calibration_skip_frames": data.calibration_skip_frames,
            "brightness_auto":         data.brightness_auto,
            "brightness_kp":           data.brightness_kp,
            "brightness_ki":           data.brightness_ki,
            "brightness_kd":           data.brightness_kd,
            "target_brightness":       data.target_brightness,
            "aruco_enabled":           data.aruco_enabled,
            "aruco_dictionary":        data.aruco_dictionary,
            "aruco_flip_image":        data.aruco_flip_image,
        }

    @staticmethod
    def from_flat_dict(flat: dict, base: CameraSettingsData) -> CameraSettingsData:
        """Merge flat dict from SettingsView into a copy of base (preserves brightness_area_points)."""
        d = deepcopy(base)
        g = flat.get

        d.index                   = int(g("index",                   d.index))
        d.width                   = int(g("width",                   d.width))
        d.height                  = int(g("height",                  d.height))
        d.skip_frames             = int(g("skip_frames",             d.skip_frames))
        d.capture_position_offset = int(g("capture_position_offset", d.capture_position_offset))

        d.contour_detection       = bool(g("contour_detection",      d.contour_detection))
        d.draw_contours           = bool(g("draw_contours",          d.draw_contours))
        d.threshold               = int(g("threshold",               d.threshold))
        d.threshold_pickup_area   = int(g("threshold_pickup_area",   d.threshold_pickup_area))
        d.epsilon                 = float(g("epsilon",               d.epsilon))
        d.min_contour_area        = float(g("min_contour_area",      d.min_contour_area))
        d.max_contour_area        = float(g("max_contour_area",      d.max_contour_area))

        d.gaussian_blur           = bool(g("gaussian_blur",          d.gaussian_blur))
        d.blur_kernel_size        = int(g("blur_kernel_size",        d.blur_kernel_size))
        d.threshold_type          = str(g("threshold_type",          d.threshold_type))
        d.dilate_enabled          = bool(g("dilate_enabled",         d.dilate_enabled))
        d.dilate_kernel_size      = int(g("dilate_kernel_size",      d.dilate_kernel_size))
        d.dilate_iterations       = int(g("dilate_iterations",       d.dilate_iterations))
        d.erode_enabled           = bool(g("erode_enabled",          d.erode_enabled))
        d.erode_kernel_size       = int(g("erode_kernel_size",       d.erode_kernel_size))
        d.erode_iterations        = int(g("erode_iterations",        d.erode_iterations))

        d.chessboard_width        = int(g("chessboard_width",        d.chessboard_width))
        d.chessboard_height       = int(g("chessboard_height",       d.chessboard_height))
        d.square_size_mm          = float(g("square_size_mm",        d.square_size_mm))
        d.calibration_skip_frames = int(g("calibration_skip_frames", d.calibration_skip_frames))

        d.brightness_auto         = bool(g("brightness_auto",        d.brightness_auto))
        d.brightness_kp           = float(g("brightness_kp",         d.brightness_kp))
        d.brightness_ki           = float(g("brightness_ki",         d.brightness_ki))
        d.brightness_kd           = float(g("brightness_kd",         d.brightness_kd))
        d.target_brightness       = float(g("target_brightness",     d.target_brightness))

        d.aruco_enabled           = bool(g("aruco_enabled",          d.aruco_enabled))
        d.aruco_dictionary        = str(g("aruco_dictionary",        d.aruco_dictionary))
        d.aruco_flip_image        = bool(g("aruco_flip_image",       d.aruco_flip_image))

        return d

    # ── nested JSON ↔ CameraSettingsData ──────────────────────────────────────

    @staticmethod
    def from_json(data: dict) -> CameraSettingsData:
        """Parse from the nested JSON format used by the repository."""
        pre   = data.get("Preprocessing",     {})
        cal   = data.get("Calibration",       {})
        bri   = data.get("Brightness Control", {})
        aruco = data.get("Aruco",             {})

        points: List[Tuple[int, int]] = []
        for i in range(1, 5):
            pt = bri.get(f"Brightness area point {i}")
            if pt:
                points.append((int(pt[0]), int(pt[1])))

        return CameraSettingsData(
            index                   = data.get("Index",                    0),
            width                   = data.get("Width",                    1280),
            height                  = data.get("Height",                   720),
            skip_frames             = data.get("Skip frames",              30),
            capture_position_offset = data.get("Capture position offset",  -4),
            contour_detection       = data.get("Contour detection",        True),
            draw_contours           = data.get("Draw contours",            True),
            threshold               = data.get("Threshold",                150),
            threshold_pickup_area   = data.get("Threshold pickup area",    200),
            epsilon                 = data.get("Epsilon",                  0.05),
            min_contour_area        = data.get("Min contour area",         1000.0),
            max_contour_area        = data.get("Max contour area",         10_000_000.0),
            gaussian_blur           = pre.get("Gaussian blur",             True),
            blur_kernel_size        = pre.get("Blur kernel size",          3),
            threshold_type          = pre.get("Threshold type",            "binary_inv"),
            dilate_enabled          = pre.get("Dilate enabled",            True),
            dilate_kernel_size      = pre.get("Dilate kernel size",        3),
            dilate_iterations       = pre.get("Dilate iterations",         2),
            erode_enabled           = pre.get("Erode enabled",             True),
            erode_kernel_size       = pre.get("Erode kernel size",         3),
            erode_iterations        = pre.get("Erode iterations",          4),
            chessboard_width        = cal.get("Chessboard width",          32),
            chessboard_height       = cal.get("Chessboard height",         20),
            square_size_mm          = cal.get("Square size (mm)",          25.0),
            calibration_skip_frames = cal.get("Skip frames",               30),
            brightness_auto         = bri.get("Enable auto adjust",        True),
            brightness_kp           = bri.get("Kp",                        0.0),
            brightness_ki           = bri.get("Ki",                        0.2),
            brightness_kd           = bri.get("Kd",                        0.05),
            target_brightness       = bri.get("Target brightness",         200.0),
            brightness_area_points  = points,
            aruco_enabled           = aruco.get("Enable detection",        False),
            aruco_dictionary        = aruco.get("Dictionary",              "DICT_4X4_1000"),
            aruco_flip_image        = aruco.get("Flip image",              False),
        )

    @staticmethod
    def to_json(data: CameraSettingsData) -> dict:
        """Serialize to the nested JSON format used by the repository."""
        bri: dict = {
            "Enable auto adjust": data.brightness_auto,
            "Kp":                 data.brightness_kp,
            "Ki":                 data.brightness_ki,
            "Kd":                 data.brightness_kd,
            "Target brightness":  data.target_brightness,
        }
        for i, pt in enumerate(data.brightness_area_points[:4], start=1):
            bri[f"Brightness area point {i}"] = list(pt)

        return {
            "Index":                   data.index,
            "Width":                   data.width,
            "Height":                  data.height,
            "Skip frames":             data.skip_frames,
            "Capture position offset": data.capture_position_offset,
            "Contour detection":       data.contour_detection,
            "Draw contours":           data.draw_contours,
            "Threshold":               data.threshold,
            "Threshold pickup area":   data.threshold_pickup_area,
            "Epsilon":                 data.epsilon,
            "Min contour area":        data.min_contour_area,
            "Max contour area":        data.max_contour_area,
            "Preprocessing": {
                "Gaussian blur":      data.gaussian_blur,
                "Blur kernel size":   data.blur_kernel_size,
                "Threshold type":     data.threshold_type,
                "Dilate enabled":     data.dilate_enabled,
                "Dilate kernel size": data.dilate_kernel_size,
                "Dilate iterations":  data.dilate_iterations,
                "Erode enabled":      data.erode_enabled,
                "Erode kernel size":  data.erode_kernel_size,
                "Erode iterations":   data.erode_iterations,
            },
            "Calibration": {
                "Chessboard width":  data.chessboard_width,
                "Chessboard height": data.chessboard_height,
                "Square size (mm)":  data.square_size_mm,
                "Skip frames":       data.calibration_skip_frames,
            },
            "Brightness Control": bri,
            "Aruco": {
                "Enable detection": data.aruco_enabled,
                "Dictionary":       data.aruco_dictionary,
                "Flip image":       data.aruco_flip_image,
            },
        }
