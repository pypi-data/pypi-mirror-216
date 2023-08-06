"""Function to parse gear config into gear args."""

import logging
import os
import pprint
import re
from pathlib import Path

from fw_gear_dcm2niix.utils.metadata import rename_infile

log = logging.getLogger(__name__)


def generate_gear_args(gear_context, FLAG):
    # pylint: disable=too-many-branches,too-many-statements
    """Generate gear arguments for different stages indicated by the FLAG."""
    log.info("%s", 100 * "-")
    log.info("Preparing arguments for gear stage >> %s", FLAG)

    if FLAG == "prepare":
        infile = gear_context.get_input_path("dcm2niix_input")
        try:
            with open(infile, "r", encoding="utf-8") as f:
                log.debug("%s opened from dcm2niix_input.", f)

        except FileNotFoundError:
            # Path separation in filename may cause downloaded filename to be altered
            filename = (
                gear_context.config_json.get("inputs", {})
                .get("dcm2niix_input", {})
                .get("location", {})
                .get("name")
            )
            try:
                if len(filename.split("/")) > 1:
                    infile = (
                        f"/flywheel/v0/input/dcm2niix_input/{filename.split('/')[-1]}"
                    )

                    with open(infile, "r", encoding="utf-8"):
                        log.debug(
                            "%s opened from path separated dcm2niix_input.", infile
                        )
            except (FileNotFoundError, AttributeError):
                log.info(
                    "Path to dcm2niix_input: %s",
                    gear_context.get_input_path("dcm2niix_input"),
                )
                log.error(
                    "Filename not understood from Gear context. Unable to open dcm2niix_input. Exiting."
                )
                os.sys.exit(1)

        except UnicodeEncodeError:
            log.info(
                "Path to dcm2niix_input: %s",
                gear_context.get_input_path("dcm2niix_input"),
            )
            log.error(
                "Filename not understood from Gear context. Unable to open dcm2niix_input. Exiting."
            )
            os.sys.exit(1)

        # Rename infile if outfile is using infile folder
        if (
            bool(re.search("%f", gear_context.config["filename"]))
            and gear_context.config["sanitize_filename"]
        ):
            infile = rename_infile(Path(infile))

        gear_args = {
            "infile": infile,
            "work_dir": gear_context.work_dir,
            "remove_incomplete_volumes": gear_context.config[
                "remove_incomplete_volumes"
            ],
            "decompress_dicoms": gear_context.config["decompress_dicoms"],
            "rec_infile": None,
        }

        if gear_context.get_input_path("rec_file_input"):
            rec_infile = Path(gear_context.get_input_path("rec_file_input"))
            if not rec_infile.is_file():
                log.error(
                    "Configuration for rec_infile_input is not a valid path. Exiting."
                )
                os.sys.exit(1)
            # else:
            gear_args["rec_infile"] = str(rec_infile)

    elif FLAG == "dcm2niix":
        # Notice the explicit 'y' for bids_sidecar, in order to capture metadata; the
        # user-defined config option setting wil be considered during the gear resolve
        # stage.
        filename = gear_context.config["filename"]
        # If filename is "%dicom%", use the dicom filename (without extension) as
        # output filename:
        if filename == "%dicom%":
            filename = Path(gear_context.get_input_path("dcm2niix_input")).stem
            # if there is still a ".dcm" extension, remove it:
            filename = filename.removesuffix(".dcm")
        filename = filename.replace(" ", "_")

        comment = gear_context.config["comment"]
        if len(comment) > 24:
            log.error(
                "The comment configuration option must be less than 25 characters. "
                "You have entered %d characters. Please edit and resubmit Gear. "
                "Exiting.",
                len(comment),
            )
            os.sys.exit(1)

        gear_args = {
            "anonymize_bids": gear_context.config["anonymize_bids"],
            "bids_sidecar": "y",
            "comment": comment,
            "compress_images": gear_context.config["compress_images"],
            "compression_level": gear_context.config["compression_level"],
            "convert_only_series": gear_context.config["convert_only_series"],
            "crop": gear_context.config["crop"],
            "filename": filename,
            "ignore_derived": gear_context.config["ignore_derived"],
            "ignore_errors": gear_context.config["ignore_errors"],
            "lossless_scaling": gear_context.config["lossless_scaling"],
            "merge2d": gear_context.config["merge2d"],
            "output_nrrd": gear_context.config["output_nrrd"],
            "philips_scaling": gear_context.config["philips_scaling"],
            "single_file_mode": gear_context.config["single_file_mode"],
            "text_notes_private": gear_context.config["text_notes_private"],
            "verbose": gear_context.config["dcm2niix_verbose"],
        }

    elif FLAG == "resolve":
        gear_args = {
            "ignore_errors": gear_context.config["ignore_errors"],
            "retain_sidecar": True,
            "retain_nifti": True,
            "output_nrrd": gear_context.config["output_nrrd"],
            "classification": None,
            "modality": None,
        }

        if (
            gear_context.config["bids_sidecar"] in ("n", "o")
            or gear_context.config["output_nrrd"]
        ):
            gear_args["retain_nifti"] = False

        try:
            classification = (
                gear_context.config_json.get("inputs", {})
                .get("dcm2niix_input", {})
                .get("object", {})
                .get("classification")
            )
            # If modality is set and classification is not set, classification returned as {'Custom':[]}
            # If modality and classification are not set, classification returned as {}
            if classification not in ({}, {"Custom": []}):
                gear_args["classification"] = classification
        except KeyError:
            log.info("Cannot determine classification from configuration.")

        try:
            gear_args["modality"] = (
                gear_context.config_json.get("inputs", {})
                .get("dcm2niix_input", {})
                .get("object", {})
                .get("modality")
            )
        except KeyError:
            log.info("Cannot determine modality from configuration.")

        tag = gear_context.config.get("tag", "")
        if tag != "":
            gear_args["tag"] = tag

    gear_args_formatted = pprint.pformat(gear_args)
    log.info("Prepared gear stage arguments: \n\n%s\n", gear_args_formatted)

    return gear_args
