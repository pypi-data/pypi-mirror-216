# -*- coding: utf-8 -*-

import csv
import fnmatch
import logging
from datetime import datetime, timezone
from itertools import chain
from pathlib import Path
from typing import List, Optional
from uuid import UUID

from arkindex_cli.commands.export.db import (
    classes_columns,
    element_classes,
    element_entities,
    element_image,
    element_metadata,
    entity_type_columns,
    get_elements,
    metadata_columns,
)
from arkindex_cli.commands.export.utils import uuid_or_manual

logger = logging.getLogger(__name__)


def element_dict(
    database_path,
    item,
    with_classes=False,
    with_metadata=False,
    with_parent_metadata=False,
    with_entities=False,
    classes_columns=None,
    metadata_columns=None,
    entity_type_columns=None,
    classification_worker_version=None,
    entities_worker_version=None,
):
    assert (
        not with_metadata or metadata_columns is not None
    ), "Metadata columns are required to output element metadata"
    assert (
        not with_classes or classes_columns is not None
    ), "Classes columns are required to output element classifications"
    assert (
        not with_entities or entity_type_columns is not None
    ), "Entity type columns are required to output element entities"
    serialized_element = {
        "id": item.id,
        "name": item.name,
        "type": item.type,
        "image_id": None,
        "image_url": None,
        "polygon": item.polygon,
        "worker_version_id": item.worker_version_id,
        "created": datetime.fromtimestamp(item.created, tz=timezone.utc).isoformat(),
    }
    element_img = element_image(database_path, item.id)
    if element_img:
        serialized_element["image_id"] = element_img.id
        serialized_element["image_url"] = element_img.url
    if with_metadata:
        serialized_element = {
            **serialized_element,
            **{key: None for key in metadata_columns},
        }
        element_md = element_metadata(
            database_path, item.id, load_parents=with_parent_metadata
        )
        for metadata in element_md:
            # If metadata.name is in metadata_columns, it means that there is only ever
            # one metadata with this name in all the listed elements, no multiple values.
            if metadata.name in serialized_element:
                serialized_element[metadata.name] = metadata.value
            # If metadata.name is not in metadata_columns, iterate through the list of
            # values and assign them to {metadata.name}_1, {metadata.name}_2 etc.
            else:
                serialized_element[
                    f"{metadata.name}_{metadata.number}"
                ] = metadata.value
    if with_classes:
        classes = element_classes(database_path, item.id, classification_worker_version)
        if len(classes):
            for class_name in classes_columns:
                serialized_element[class_name] = next(
                    (
                        item.classification_confidence
                        for item in classes
                        if item.class_name == class_name
                    ),
                    None,
                )
    if with_entities:
        serialized_element = {
            **serialized_element,
            **{key: None for key in entity_type_columns},
        }
        entities = element_entities(database_path, item.id, entities_worker_version)
        for entity in entities:
            if f"entity_{entity.entity_type}" in serialized_element:
                serialized_element[f"entity_{entity.entity_type}"] = entity.name
            # If entity.entity_type is not in serialized_element, iterate through
            # the list of entity.name and assign them to entity_{entity.entity_type}_1,
            # entity_{entity.entity_type}_2 etc.
            else:
                serialized_element[
                    f"entity_{entity.entity_type}_{entity.number}"
                ] = entity.name

    return serialized_element


def run(
    database_path: Path,
    output_path: Path,
    profile_slug: Optional[str] = None,
    parent: Optional[UUID] = None,
    type: Optional[str] = None,
    recursive: Optional[bool] = False,
    with_classes: Optional[bool] = False,
    with_metadata: Optional[bool] = False,
    with_parent_metadata: Optional[bool] = False,
    with_entities: Optional[bool] = False,
    classification_worker_version: Optional[str] = None,
    entities_worker_version: Optional[str] = None,
    output_header: Optional[List[str]] = [],
):
    database_path = database_path.absolute()
    assert database_path.is_file(), f"Database at {database_path} not found"
    if with_parent_metadata:
        assert (
            with_metadata
        ), "The --with-parent-metadata option can only be used if --with-metadata is set."
    if entities_worker_version:
        assert (
            with_entities
        ), "The --entities-worker-version option can only be used if --with-entities is set."

    output_path = output_path.absolute()

    if recursive:
        assert (
            parent
        ), "The recursive option can only be used if a parent_element is given. If no parent_element is specified, element listing is recursive by default."

    elements = get_elements(database_path, parent, type, recursive)

    csv_header = [
        "id",
        "name",
        "type",
        "image_id",
        "image_url",
        "polygon",
        "worker_version_id",
        "created",
    ]
    cl_columns = None
    if with_classes:
        cl_columns = classes_columns(database_path, parent, type, recursive)
        csv_header = csv_header + cl_columns
    md_columns = None
    if with_metadata:
        # Fetch all the metadata keys to build one CSV column by key
        md_columns = metadata_columns(
            database_path, parent, type, recursive, load_parents=with_parent_metadata
        )
        csv_header = csv_header + md_columns
    et_columns = None
    if with_entities:
        et_columns = entity_type_columns(
            database_path,
            parent,
            type,
            entities_worker_version,
            recursive=recursive,
        )
        csv_header = csv_header + et_columns

    if output_header:
        filtered_header = list(
            chain(*[fnmatch.filter(csv_header, header) for header in output_header])
        )
        # Keep the initial order of the CSV columns
        csv_header = [header for header in csv_header if header in filtered_header]

    with open(output_path, "w", encoding="UTF8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=csv_header)
        writer.writeheader()
        for element in elements:
            serialized_element = {
                key: value
                for key, value in element_dict(
                    database_path,
                    element,
                    with_classes,
                    with_metadata,
                    with_parent_metadata,
                    with_entities,
                    classes_columns=cl_columns,
                    metadata_columns=md_columns,
                    entity_type_columns=et_columns,
                    classification_worker_version=classification_worker_version,
                    entities_worker_version=entities_worker_version,
                ).items()
                if key in csv_header
            }
            writer.writerow(serialized_element)
    logger.info(f"Exported elements successfully written to {output_path}.")


def add_csv_parser(subcommands):
    csv_parser = subcommands.add_parser(
        "csv",
        description="Read data from an exported database and generate a CSV file.",
        help="Generates a CSV file from an Arkindex export.",
    )
    csv_parser.add_argument(
        "--parent",
        type=UUID,
        help="Limit the export to the children of a given element.",
    )
    csv_parser.add_argument(
        "--type", type=str, help="Limit the export to elements of a given type."
    )
    csv_parser.add_argument(
        "--recursive", action="store_true", help="Get elements recursively."
    )
    csv_parser.add_argument(
        "--with-classes", action="store_true", help="Retrieve element classes."
    )
    csv_parser.add_argument(
        "--classification-worker-version",
        type=uuid_or_manual,
        help="The worker version that created the classifications that will be in the csv",
    )
    csv_parser.add_argument(
        "--with-metadata", action="store_true", help="Retrieve element metadata."
    )
    csv_parser.add_argument(
        "--with-parent-metadata",
        action="store_true",
        help="Recursively retrieve metadata of element ancestors.",
    )
    csv_parser.add_argument(
        "--with-entities", action="store_true", help="Retrieve element entities."
    )
    csv_parser.add_argument(
        "--entities-worker-version",
        type=uuid_or_manual,
        help="Only retrieve the entities created by a specific worker version.",
    )
    csv_parser.add_argument(
        "-o",
        "--output",
        default=Path.cwd() / "elements.csv",
        type=Path,
        help="Path to a CSV file where results will be outputted. Defaults to '<current_directory>/elements.csv'.",
        dest="output_path",
    )
    csv_parser.add_argument(
        "-f",
        "--field",
        nargs="+",
        type=str,
        help="Limit the CSV columns to the selected fields",
        dest="output_header",
    )
    csv_parser.set_defaults(func=run)
