# -*- coding: utf-8 -*-

import logging
import shutil
import tempfile
from pathlib import Path
from typing import List
from uuid import UUID

from arkindex_cli.commands.export.db import (
    Element,
    element_image,
    element_transcription,
    filter_folder_id,
    list_children,
    list_folders,
    recursive_element_transcriptions,
)
from arkindex_cli.commands.export.utils import (
    Ordering,
    bounding_box,
    bounding_box_arkindex,
    image_download,
)

try:
    from reportlab.lib import colors
    from reportlab.pdfbase.pdfmetrics import stringWidth
    from reportlab.pdfgen import canvas

    from PIL import Image
except ImportError:
    DEPS_AVAILABLE = False
else:
    DEPS_AVAILABLE = True


logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def add_pdf_parser(subcommands):
    pdf_parser = subcommands.add_parser(
        "pdf",
        description=(
            "Read data from an exported database and generate a PDF with selectable text. "
            "Due to the PDF structure, only elements of type <page-type> are rendered for the specified folders."
        ),
        help="Generates a PDF from an Arkindex export.",
    )
    pdf_parser.add_argument(
        "--folder-ids",
        type=UUID,
        help="Limit the export to one or more folders. Exports all folders corresponding to FOLDER_TYPE by default.",
        action="append",
    )
    pdf_parser.add_argument(
        "--folder-type",
        default="folder",
        type=str,
        help="Slug of an element type to use for folders. Defaults to `folder`.",
    )
    pdf_parser.add_argument(
        "--page-type",
        default="page",
        type=str,
        help="Slug of an element type to use for pages. Defaults to `page`.",
    )
    text_source = pdf_parser.add_mutually_exclusive_group()
    text_source.add_argument(
        "--use-page-transcriptions",
        action="store_true",
        help="Export page-level transcriptions on the specified page-type elements. Cannot be used conjointly with --line-type.",
    )
    text_source.add_argument(
        "--line-type",
        default="text_line",
        type=str,
        help="Slug of an element type to use for lines. Defaults to `text_line`. Cannot be used conjointly with --use-page-transcriptions.",
    )
    pdf_parser.add_argument(
        "--debug",
        action="store_true",
        help="Make bounding boxes and transcriptions visible.",
    )
    pdf_parser.add_argument(
        "-o",
        "--output",
        default=Path.cwd(),
        type=Path,
        help="Path to a directory where files will be exported to. Defaults to the current directory.",
        dest="output_path",
    )
    pdf_parser.add_argument(
        "--order-by-name",
        action="store_true",
        help="Order exported elements by name instead of the internal position on Arkindex.",
    )
    pdf_parser.add_argument(
        "--transcription-worker-version",
        type=UUID,
        help="Filter transcriptions by worker version.",
    )
    pdf_parser.set_defaults(func=run)


def image_draw(page: Element, image_path: str, c: "canvas", temp_dir: str) -> tuple:
    """
    Draw suitable image depending on crop if it is necessary
    """
    assert DEPS_AVAILABLE, "Missing PDF export dependencies"

    # opens existing image with PIL to get its size
    image = Image.open(image_path)

    # page Element must have a polygon
    assert page.polygon is not None

    # set default imageDraw function parameters
    pdf_image_width, pdf_image_height = image.width, image.height

    # getting dimensions of page bounding box
    page_box_dim = bounding_box(page.polygon)

    if (page_box_dim.width, page_box_dim.height) != image.size:

        # handling case when to crop image
        # PIL coordinates start from top-left corner,
        # crop method gets 4-tuple defining the left, upper, right, and
        # lower pixel coordinate.
        crop_parameters = (
            page_box_dim.x,
            # absolute value is to prevent cases where bounding_box
            # y coordinate is higher than box height
            abs(page_box_dim.height - page_box_dim.y),
            page_box_dim.x + page_box_dim.width,
            page_box_dim.y,
        )

        # saving cropped file in temp_dir to be called by drawImage
        image_path = temp_dir / f"{page.name}.jpg"

        image = image.crop(crop_parameters)
        image.save(image_path, format="JPEG")

        logger.info(f"saved cropped image at: {image_path}")

        # updating drawImage and pagesize parameters to bounding box
        pdf_image_width, pdf_image_height = page_box_dim.width, page_box_dim.height

    # sizes page to fit relevant image
    c.setPageSize(image.size)

    # drawing suitable image
    c.drawImage(image_path, 0, 0, pdf_image_width, pdf_image_height, mask=None)

    return image.size


def pdf_gen(
    folder: Element,
    database_path,
    output_path,
    page_type,
    use_page_transcriptions,
    line_type,
    debug,
    order_by_name,
    transcription_worker_version,
    **kwargs,
) -> None:
    """
    Gets the database path, argument from cli, path to the generated pdf and the
    temporary directory where to find downloaded images
    """

    assert (
        DEPS_AVAILABLE
    ), "Missing PDF export dependencies. Run `pip install arkindex-cli[export]` to install them."

    # creating temporary directory
    temp_dir = Path(tempfile.mkdtemp())
    logger.info(f"created temporary directory: {temp_dir}")

    # chooses color depending on debug option
    selected_color = colors.transparent

    if debug:
        selected_color = colors.fuchsia

    # Trigger name ordering if required
    ordering = Ordering.Name if order_by_name else Ordering.Position

    try:
        # canvas requires the input path as string
        c = canvas.Canvas(str(Path(output_path) / f"{folder.name}.pdf"))
        for page in list_children(
            database_path, folder.id, page_type, ordering=ordering
        ):
            logger.info(f"Processing page {page}")
            # handling case where no url is returned
            page_image = element_image(database_path, page.id)

            page_bbox = bounding_box_arkindex(page.polygon)
            if page_image is None:
                logger.warning(f"no image for page {page.name} ({page.id})")
                continue

            # downloading existing image
            existing_image = image_download(page_image.url, page_image.id, temp_dir)

            # running reportlab drawing actions through image_draw and
            # returning updated image dimensions for the next steps
            image_width, image_height = image_draw(page, existing_image, c, temp_dir)

            if use_page_transcriptions:
                # Only export page-level transcriptions
                page_transcriptions = element_transcription(
                    database_path, page.id, str(transcription_worker_version)
                )
                if not len(page_transcriptions):
                    logger.warning(
                        f"No page-level transcription for {page_type} {page.id}."
                    )
                for transcription in page_transcriptions:
                    c.setFillColor(selected_color)
                    textobject = c.beginText(0, image_height)
                    for line in transcription.text.splitlines(False):
                        textobject.textLine(line.rstrip())
                    c.drawText(textobject)

            else:
                # getting the list of Transcriptions namedtuples for each page
                page_transcriptions = recursive_element_transcriptions(
                    database_path, page.id, str(transcription_worker_version)
                )

                # creating a dictionary where keys are lines ids and values are
                # relative line transcriptions
                transcriptions_dict = {
                    transcription.element_id: transcription
                    for transcription in page_transcriptions
                }

                lines = list_children(database_path, page.id, line_type)
                if not lines:
                    logger.warning(f"no {line_type!r} in page {page.name} ({page.id})")

                for line in lines:

                    # handling case where no polygon is returned
                    if line.polygon is None:
                        logger.warning(f"no polygon for line {line.name} ({line.id})")
                    # getting bounding box dimensions
                    line_box_dim = bounding_box(
                        line.polygon, offset_x=page_bbox.x, offset_y=page_bbox.y
                    )

                    # drawing line polygon bounding box
                    # as the y axis is inverted, y origin point is "height - max_y"

                    # drawing line polygon bounding box
                    c.rect(
                        # Remove page offset
                        line_box_dim.x,
                        image_height - line_box_dim.y,
                        line_box_dim.width,
                        line_box_dim.height,
                        # linebox visible according to debug value
                        stroke=debug,
                    )

                    # handling case where line image is different from page image
                    line_image = element_image(database_path, line.id)
                    if line_image.url != page_image.url:
                        logger.warning(
                            f"""
                            {line.name} ({line.id}) image different from {page.name}
                            ({page.id}) image
                            """
                        )
                        continue

                    # handling case where no transcription for a textline

                    if line.id not in transcriptions_dict:
                        logger.warning(f"no transcription for {line.name} ({line.id})")
                        continue

                    else:
                        text_to_draw = transcriptions_dict[line.id].text

                        c.setFillColor(selected_color)

                        # get the width of a single character, arbitrarily first one
                        # Font is set to MONOSPACE one such as Courier,
                        # fontsize is arbitrarily set to 10
                        char_width = stringWidth(text_to_draw[0], "Courier", 10)

                        # calculating ratio between character height and character
                        # width to adjust fontsize, character height has been set to
                        # 10
                        char_ratio = 10 / char_width

                        # character width so the fontsize match with the line_box_width
                        # corresponds to line box width divided by total number
                        # of characters in the string
                        font_width = line_box_dim.width / len(text_to_draw)

                        # adjusts the font size to match line box width
                        c.setFont("Courier", font_width * char_ratio)
                        # as the y axis is inverted, y origin point is "height - max_y"
                        c.drawString(
                            line_box_dim.x, image_height - line_box_dim.y, text_to_draw
                        )

            # save state and prepared new possible insertion within a page
            # (force PageBreak)
            c.showPage()

        # saving the whole canvas
        c.save()
        # change the name
        logger.info(f"{folder.name} generated at {output_path}")
    finally:
        shutil.rmtree(temp_dir)


def run(
    database_path: Path,
    output_path: Path,
    folder_type: str,
    folder_ids: List[UUID] = [],
    **kwargs,
):
    database_path = database_path.absolute()
    assert database_path.is_file(), f"Database at {database_path} not found"

    output_path = output_path.absolute()
    assert output_path.is_dir(), f"Output path {output_path} is not a valid directory"

    folders = list_folders(database_path, folder_type)
    if folder_ids is not None:
        folders = filter_folder_id(folders, folder_ids)

    assert folders, f"No '{folder_type}' folders were found"

    for folder in folders:
        pdf_gen(
            folder,
            database_path=database_path,
            output_path=output_path,
            **kwargs,
        )
