"""
Module containing processors which mask pixels
"""
import logging
from pathlib import Path

import numpy as np
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.wcs import WCS

from mirar.data import Image, ImageBatch
from mirar.paths import BASE_NAME_KEY, FITS_MASK_KEY, get_output_dir
from mirar.processors.base_processor import BaseImageProcessor

logger = logging.getLogger(__name__)

# MASK_VALUE = -99.
MASK_VALUE = np.nan


class BaseMask(BaseImageProcessor):
    """
    Base class for masking processors
    """

    def __init__(
        self,
        write_masked_pixels_to_file: bool = False,
        output_dir: str | Path = "mask",
        only_write_mask: bool = False,
    ):
        super().__init__()
        self.write_masked_pixels_to_file = write_masked_pixels_to_file
        self.output_dir = output_dir
        self.only_write_mask = only_write_mask

    def get_mask(self, image) -> np.ndarray:
        """
        Function to get the mask for a given image
        """
        raise NotImplementedError

    def _apply_to_images(
        self,
        batch: ImageBatch,
    ) -> ImageBatch:
        for image in batch:
            data = image.get_data()
            logger.debug(f"Masking {image[BASE_NAME_KEY]}")
            mask = self.get_mask(image)

            if not self.only_write_mask:
                data[mask] = MASK_VALUE
                image.set_data(data)

            logger.info(f"Masked {np.sum(mask)} pixels in {image[BASE_NAME_KEY]}")

            if self.write_masked_pixels_to_file:
                mask_directory = get_output_dir(self.output_dir, self.night_sub_dir)
                if not mask_directory.exists():
                    mask_directory.mkdir(parents=True)
                mask_file_path = mask_directory / f"{image[BASE_NAME_KEY]}_mask.fits"

                mask_image = Image(data=mask.astype(int), header=image.get_header())
                self.save_fits(mask_image, mask_file_path)

                image[FITS_MASK_KEY] = mask_file_path.as_posix()
        return batch


class MaskPixelsFromPath(BaseMask):
    """
    Processor to apply bias calibration
    """

    base_key = "maskfrompath"

    def __init__(
        self,
        mask_path: str | Path = None,
        mask_path_key: str = None,
        write_masked_pixels_to_file: bool = False,
        output_dir: str | Path = "mask",
        only_write_mask: bool = False,
    ):
        super().__init__(
            write_masked_pixels_to_file=write_masked_pixels_to_file,
            output_dir=output_dir,
            only_write_mask=only_write_mask,
        )
        self.mask = None
        self.mask_path = mask_path
        self.mask_path_key = mask_path_key
        if mask_path is None and mask_path_key is None:
            raise ValueError("Must specify either mask_path or mask_path_key")
        if mask_path is not None and mask_path_key is not None:
            raise ValueError("Must specify either mask_path or mask_path_key, not both")

    def __str__(self) -> str:
        return f"Processor to mask bad pixels using a pre-defined map: {self.mask_path}"

    def get_mask(self, image) -> np.ndarray:
        """
        loads mask if needed, and returns it

        :return: mask
        """
        # if self.mask is None: # why is this needed?
        if self.mask_path is not None:
            self.mask = self.open_fits(self.mask_path)
        elif self.mask_path_key is not None:
            logger.debug(f"Loading mask from {image[self.mask_path_key]}")
            self.mask = self.open_fits(image[self.mask_path_key])
        mask = self.mask.get_data()
        mask = mask != 0
        return mask


class MaskAboveThreshold(BaseMask):
    """
    Processor to mask pixels above a threshold
    """

    base_key = "maskthresh"

    def __init__(
        self,
        threshold: float = None,
        threshold_key: str = None,
        write_masked_pixels_to_file: bool = False,
        output_dir: str | Path = "mask",
        only_write_mask: bool = False,
    ):
        """
        :param threshold: threshold to mask above
        :param threshold_key: key to use to get threshold from image header
        """
        super().__init__(
            write_masked_pixels_to_file=write_masked_pixels_to_file,
            output_dir=output_dir,
            only_write_mask=only_write_mask,
        )
        self.threshold = threshold
        self.threshold_key = threshold_key
        self.write_masked_pixels_to_file = write_masked_pixels_to_file
        if threshold is None and threshold_key is None:
            raise ValueError("Must specify either threshold or threshold_key")
        if threshold is not None and threshold_key is not None:
            raise ValueError("Must specify either threshold or threshold_key, not both")

    def __str__(self) -> str:
        return f"Processor to mask pixels above a threshold: {self.threshold}"

    def get_mask(self, image) -> np.ndarray:
        """
        Returns a mask for pixels above a threshold

        :return: mask
        """
        if self.threshold is None:
            self.threshold = image.get_header()[self.threshold_key]
        mask = image.get_data() > self.threshold
        return mask


class MaskPixelsFromWCS(BaseMask):
    """
    Processor to mask pixels from a file where WCS coordinates of masked pixels are
    given
    """

    base_key = "maskwcs"

    def __init__(
        self,
        mask_pixels_ra: float | list[float] = None,
        mask_pixels_dec: float | list[float] = None,
        mask_file_key: str = FITS_MASK_KEY,
        write_masked_pixels_to_file: bool = False,
        output_dir: str | Path = "mask",
        only_write_mask: bool = False,
    ):
        super().__init__(
            write_masked_pixels_to_file=write_masked_pixels_to_file,
            output_dir=output_dir,
            only_write_mask=only_write_mask,
        )
        self.mask_pixels_ra = mask_pixels_ra
        self.mask_pixels_dec = mask_pixels_dec
        self.mask_file_key = mask_file_key

        if self.mask_pixels_ra is not None:
            self.mask_file_key = None

    def __str__(self) -> str:
        return "Processor to mask pixels using a  list of RA/Dec."

    def get_mask(self, image) -> np.ndarray:
        """
        loads mask if needed, and returns it

        :return: mask
        """
        wcs = WCS(image.get_header())
        if self.mask_file_key is not None:
            mask_file_path = image.get_header()[self.mask_file_key]
            with fits.open(mask_file_path) as mask_image:
                mask = mask_image[0].data
                mask_wcs = WCS(mask_image[0].header)

            masked_pixel_x, masked_pixel_y = np.where(mask)
            mask_pixel_coords = mask_wcs.pixel_to_world(masked_pixel_y, masked_pixel_x)
            mask_pixels_ra = mask_pixel_coords.ra.deg
            mask_pixels_dec = mask_pixel_coords.dec.deg
        else:
            mask_pixels_ra = self.mask_pixels_ra
            mask_pixels_dec = self.mask_pixels_dec
        logger.debug(f"Masking {mask_pixels_ra} ras and {mask_pixels_dec} decs")

        mask_pixel_coords = SkyCoord(mask_pixels_ra, mask_pixels_dec, unit="deg")
        mask_pixels_x, mask_pixels_y = wcs.world_to_pixel(mask_pixel_coords)
        mask_pixels_x = mask_pixels_x.astype(int)
        mask_pixels_y = mask_pixels_y.astype(int)
        mask = np.zeros(image.get_data().shape, dtype=bool)
        mask_in_image = np.logical_and(
            mask_pixels_x >= 0, mask_pixels_x < mask.shape[1]
        ) & np.logical_and(mask_pixels_y >= 0, mask_pixels_y < mask.shape[0])
        mask_pixels_x = mask_pixels_x[mask_in_image]
        mask_pixels_y = mask_pixels_y[mask_in_image]
        mask[mask_pixels_y, mask_pixels_x] = True
        return mask


class WriteMaskedCoordsToFile(BaseMask):
    """
    Processor to write masked coordinates to a file
    """

    base_key = "writemaskedcoords"

    def __init__(self, output_dir: str | Path = "mask", only_write_mask: bool = False):
        super().__init__(
            write_masked_pixels_to_file=True,
            output_dir=output_dir,
            only_write_mask=only_write_mask,
        )

    def get_mask(self, image) -> np.ndarray:
        mask = np.zeros(image.get_data().shape, dtype=bool)

        # For some reason, MASK_VALUE == np.nan returns False. Issue/Feature of numpy?
        # This is a workaround
        if np.isnan(MASK_VALUE):
            mask[np.isnan(image.get_data())] = True
        else:
            mask[image.get_data() == MASK_VALUE] = True
        return mask
