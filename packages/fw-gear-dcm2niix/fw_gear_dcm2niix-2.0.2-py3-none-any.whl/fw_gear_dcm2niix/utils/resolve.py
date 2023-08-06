"""Functions to resolve dcm2niix gear outputs."""

import logging
import os
import shutil

from fw_gear_dcm2niix.utils import metadata

log = logging.getLogger(__name__)


def setup(
    output_image_files,
    output_sidecar_files,
    work_dir,
    dcm2niix_input_dir,
    output_dir,
    ignore_errors=False,
    retain_sidecar=False,
    retain_nifti=True,
    output_nrrd=False,
    classification=None,
    modality=None,
):
    # pylint: disable=too-many-arguments,too-many-locals
    """Orchestrate resolution of gear, including metadata capture and file retention.

    Args:
        output_image_files (list): The absolute paths to converted image files to resolve.
            Typically these are NIfTI files, but can be the two files constituting the
            NRRD format (i.e., ".raw" and ".nhdr") or the NRRD format (i.e., ".nrrd").
            Also contains ".bval", ".bvec", and ".mvec" files, if applicable.
        output_sidecar_files (list): The absolute paths to the sidecar files to be
            used as metadata on all files in the output_image_files input list.
        work_dir (str): The absolute path to the output directory of dcm2niix and where
            the metadata file generated is written to.
        dcm2niix_input_dir (str): The absolute path to the input directory to dcm2niix.
        retain_sidecar (bool): If true, sidecar is retained in final output.
        retain_nifti (bool): If true, NIfTI is retained in final output.
        output_nrrd (bool): If true, export as NRRD instead of NIfTI.
        classification (dict): File classification, typically from gear config.
        modality (str): File modality, typically from gear config.

    Returns:
        None

    """
    # Ignoring errors configuration option; move all files from work_dir to output_dir
    if ignore_errors is True:
        log.warning("Applying Expert Option (ignore_errors).")

        if output_image_files is not None:
            # Capture metadata
            _ = metadata.generate(
                output_image_files,
                output_sidecar_files,
                work_dir,
                dcm2niix_input_dir,
                retain_sidecar=True,
                retain_nifti=True,
                output_nrrd=False,
                classification=classification,
                modality=modality,
            )

        for item in os.listdir(work_dir):
            item_path = os.path.join(work_dir, item)
            if not os.path.isdir(item_path):
                shutil.move(item_path, output_dir)
                log.info("Moving %s to output directory for upload to Flywheel.", item)

    else:
        # Capture metadata
        # pylint: disable=duplicate-code
        metadata_file = metadata.generate(
            output_image_files,
            output_sidecar_files,
            work_dir,
            dcm2niix_input_dir,
            retain_sidecar=retain_sidecar,
            retain_nifti=retain_nifti,
            output_nrrd=output_nrrd,
            classification=classification,
            modality=modality,
        )
        # pylint: enable=duplicate-code

        # Retain gear outputs
        retain_gear_outputs(
            output_image_files,
            output_sidecar_files,
            metadata_file,
            output_dir,
            retain_sidecar=retain_sidecar,
            retain_nifti=retain_nifti,
            output_nrrd=output_nrrd,
        )


def retain_gear_outputs(
    output_image_files,
    output_sidecar_files,
    metadata_file,
    output_dir,
    retain_sidecar=True,
    retain_nifti=True,
    output_nrrd=False,
):
    # pylint: disable=too-many-arguments
    """Move selected gear outputs to the output directory.

    Args:
        output_image_files (list): The absolute paths to converted image files to resolve.
            Typically these are NIfTI files, but can be the two files constituting the
            NRRD format (i.e., ".raw" and ".nhdr") or the NRRD format (i.e., ".nrrd").
            Also contains ".bval", ".bvec", and ".mvec" files, if applicable.
        output_sidecar_files (list): The absolute paths to the sidecar files to be
            used as metadata on all files in the output_image_files input list.
        metadata_file (str): The absolute path to the metadata file.
        work_dir (str): The absolute path to the output directory of dcm2niix and
            where the generated metadata file is.
        output_dir (str): The absolute path to the gear output directory.
        retain_sidecar (bool): If true, sidecar is retained in final output.
        retain_nifti (bool): If true, NIfTI is retained in final output.
        output_nrrd (bool): If true, export as NRRD instead of NIfTI.

    Returns:
        None

    """
    log.info("Resolving gear outputs.")

    if (retain_nifti and output_nrrd) or (
        not retain_nifti and not output_nrrd and not retain_sidecar
    ):
        log.critical(
            "Function arguments retain_nifti and output_nrrd are exclusive. "
            "Gear config logic is broken. Exiting."
        )
        os.sys.exit(1)

    for sidecar in output_sidecar_files:
        # Move bids json sidecar file, if indicated
        if retain_sidecar:
            shutil.move(sidecar, output_dir)
            log.info("Moving %s to output directory.", sidecar)

        # Move data files, if indicated
        # Split sidecar into the "root" name by removing .json suffix
        stem = sidecar.split(".json")[0]
        for file in output_image_files:
            # pylint: disable=duplicate-code
            # Split image name by "root" name from sidecar
            substr = file.split(stem)
            # If the "root" name of sidecar is not a substring of image file
            #   We don't care about this image file.
            if len(substr) < 2:
                continue
            # Get "root" and what's "left" over after splitting of "root" name
            #   from sidecar
            _, left = substr
            # pylint: enable=duplicate-code

            if retain_nifti:
                # If "left" over is simply the extension, this image matches
                #   the current sidecar, move to output.
                if left in [".nii.gz", ".nii", ".bval", ".bvec", ".mvec"]:
                    log.info("Moving %s to output directory.", file)
                    shutil.move(file, output_dir)

            if output_nrrd:
                # If "left" over is simply the extension, this image matches
                #   the current sidecar, move to output.
                if left in [".raw.gz", ".nhdr", ".nrrd"]:
                    log.info("Moving %s to output directory.", file)
                    shutil.move(file, output_dir)

    # Move metadata file
    shutil.move(metadata_file, output_dir)
    log.info("Moving %s to output directory.", metadata_file)

    log.info("Gear outputs resolved.")
