# -*- coding: utf-8 -*-
import sqlite3
import uuid
import warnings
from collections import namedtuple
from functools import wraps
from itertools import starmap
from typing import List, Optional

from arkindex_cli.commands.export.utils import Ordering

# creating named tuple for easier handling of list_elements returned values

Image = namedtuple("Image", ["id", "url"])
Element = namedtuple("Element", ["id", "name", "polygon", "worker_version_id"])
TypedElement = namedtuple(
    "Element", ["id", "name", "type", "polygon", "worker_version_id", "created"]
)
ElementEntity = namedtuple("ElementEntity", ["entity_type", "name", "number"])
ElementEntity.__doc__ += "Only the type and name of an entity attached to an element through a transcription."
Transcription = namedtuple(
    "Transcription", ["id", "element_id", "text", "confidence", "worker_version_id"]
)
TranscriptionEntity = namedtuple(
    "TranscriptionEntity",
    [
        "transcription_id",
        "element_id",
        "entity_id",
        "entity_type",
        "entity_value",
        "entity_metas",
        "offset",
        "length",
    ],
)
TranscriptionEntity.__doc__ += "This does not only contain data from the TranscriptionEntity table, but also additional related data from the Transcription and Entity tables."
Worker = namedtuple("Worker", ["id", "name", "slug", "type", "revision"])
Metadata = namedtuple("Metadata", ["name", "value", "number"])
Classification = namedtuple(
    "Classification",
    [
        "class_name",
        "class_id",
        "classification_confidence",
        "classification_worker_version",
    ],
)


def deprecated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        warnings.warn(
            "This method is deprecated. Please use the arkindex-export library instead: https://pypi.org/project/arkindex-export/",
            FutureWarning,
            stacklevel=2,
        )
        return func(*args, **kwargs)

    return wrapper


@deprecated
def list_elements(database_path: str, type: str) -> List[Element]:
    """
    Gets a database path, and the specified page type
    """

    # connection to the database
    connection = sqlite3.Connection(database_path)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, polygon,worker_version_id FROM element WHERE type = ?",
        (type,),
    )
    result = list(starmap(Element, cursor.fetchall()))

    cursor.close()
    connection.close()

    return result


@deprecated
def list_pages(database_path: str, page_type: str) -> list:
    """
    Gets a database path, and the specified page type
    """

    return list_elements(database_path, page_type)


@deprecated
def list_folders(database_path: str, folder_type: str) -> list:
    """
    Gets a database path, the optional folder_type as strings
    """

    return list_elements(database_path, folder_type)


@deprecated
def list_lines(database_path: str, line_type: str) -> list:
    """
    Gets a database path, and the specified line_type
    """

    return list_elements(database_path, line_type)


@deprecated
def filter_folder_id(query_result: list, element_ids: list) -> list:
    """
    Gets the optional element_id arg and filter by respective value
    """

    filtered_list = []
    for elt in query_result:
        # must convert values from query result
        # (returned as strings by cursor.fetchall) in uuid type
        if uuid.UUID(elt[0]) in element_ids:
            filtered_list.append(elt)
    return filtered_list


@deprecated
def list_children(
    database_path: str,
    parent_id: str,
    child_type: str,
    ordering: Ordering = Ordering.Position,
) -> List[Element]:
    """
    Gets the absolute path to the database and the optional element_id arg (parent_id),
    the type of child element and returns the list of child elements
    """

    # connection to the database
    connection = sqlite3.Connection(database_path)
    cursor = connection.cursor()

    order_statement = "ord" if ordering == Ordering.Position else "name"
    query = f"""
        WITH RECURSIVE page_ids (id,ord) AS (
                SELECT child_id, ordering
                FROM element_path
                WHERE parent_id = ?
            UNION
                SELECT child_id, ordering
                FROM element_path
                JOIN page_ids ON (element_path.parent_id = page_ids.id)
        )
        SELECT element.id, name, polygon, worker_version_id
        FROM element
        JOIN page_ids USING (id)
        WHERE type = ?
        ORDER BY {order_statement};
        """

    params = list(map(str, [parent_id, child_type]))

    # query execution
    cursor.execute(query, params)
    result = list(starmap(Element, cursor.fetchall()))

    cursor.close()
    connection.close()

    return result


@deprecated
def get_elements(
    database_path: str,
    parent_id: Optional[str],
    element_type: Optional[str],
    recursive: bool,
) -> List[TypedElement]:
    """
    Retrieve a list of elements from the whole corpus or a given parent,
    recursively or not, with optional type filtering.
    """

    connection = sqlite3.Connection(database_path)
    cursor = connection.cursor()

    if parent_id and element_type:
        if recursive:
            cursor.execute(
                """
                WITH RECURSIVE children_ids (id,ord) AS (
                        SELECT child_id, ordering
                        FROM element_path
                        WHERE parent_id = ?
                    UNION
                        SELECT child_id, ordering
                        FROM element_path
                        JOIN children_ids ON (element_path.parent_id = children_ids.id)
                )
                SELECT DISTINCT element.id, name, type, polygon, worker_version_id, created
                FROM element
                JOIN children_ids USING (id)
                WHERE type = ?
                ORDER BY children_ids.ord;
                """,
                (str(parent_id), element_type),
            )
        else:
            cursor.execute(
                """
                    SELECT DISTINCT element.id, name, type, polygon, worker_version_id, created
                    FROM element
                    LEFT JOIN element_path ON (element.id = element_path.child_id)
                    WHERE (element_path.parent_id = ?
                    AND type = ?)
                    ORDER BY parent_id NULLS FIRST;
                """,
                (
                    str(parent_id),
                    element_type,
                ),
            )
    elif element_type:
        cursor.execute(
            """
                SELECT DISTINCT element.id, name, type, polygon, worker_version_id, created
                FROM element
                LEFT JOIN element_path ON (element.id = element_path.child_id)
                WHERE type = ?
                ORDER BY parent_id NULLS FIRST;
            """,
            (element_type,),
        )
    elif parent_id:
        if recursive:
            cursor.execute(
                """
                WITH RECURSIVE children_ids (id,ord) AS (
                        SELECT child_id, ordering
                        FROM element_path
                        WHERE parent_id = ?
                    UNION
                        SELECT child_id, ordering
                        FROM element_path
                        JOIN children_ids ON (element_path.parent_id = children_ids.id)
                )
                SELECT DISTINCT element.id, name, type, polygon, worker_version_id, created
                FROM element
                JOIN children_ids USING (id)
                ORDER BY children_ids.ord;
                """,
                (str(parent_id),),
            )
        else:
            cursor.execute(
                """
                    SELECT DISTINCT element.id, name, type, polygon, worker_version_id, created
                    FROM element
                    LEFT JOIN element_path ON (element.id = element_path.child_id)
                    WHERE element.id IN (SELECT child_id FROM element_path WHERE parent_id = ?)
                    ORDER BY parent_id NULLS FIRST;
                """,
                (str(parent_id),),
            )
    else:
        cursor.execute(
            """
                SELECT DISTINCT element.id, name, type, polygon, worker_version_id, created
                FROM element
                LEFT JOIN element_path ON (element.id = element_path.child_id)
                ORDER BY parent_id NULLS FIRST;
            """
        )

    result = list(starmap(TypedElement, cursor.fetchall()))

    cursor.close()
    connection.close()

    return result


@deprecated
def element_metadata(
    database_path: str, element_id: str, load_parents: bool = False
) -> Optional[List[Metadata]]:
    """
    Retrieve an element's metadata.
    If load_parents is set to True, also lists metadata of all its ascending elements.
    """

    connection = sqlite3.Connection(database_path)
    cursor = connection.cursor()

    if load_parents is False:
        cursor.execute(
            """
            SELECT name, value, ROW_NUMBER() OVER (PARTITION BY name) AS number FROM metadata
            WHERE element_id = ?;
            """,
            (element_id,),
        )
    else:
        cursor.execute(
            """
            WITH RECURSIVE ascendents (id) AS (
                    SELECT ?
                UNION ALL
                    SELECT parent_id FROM element_path INNER JOIN ascendents
                    WHERE child_id = ascendents.id
            )
            SELECT name, value, ROW_NUMBER() OVER (PARTITION BY name) AS number FROM metadata
            WHERE element_id IN ascendents;
            """,
            (element_id,),
        )

    result = cursor.fetchall()
    cursor.close()
    connection.close()
    if result is None:
        return
    return list(starmap(Metadata, result))


@deprecated
def classes_columns(
    database_path: str,
    parent_id: Optional[uuid.UUID],
    element_type: Optional[str],
    recursive: False,
) -> List[str]:
    connection = sqlite3.Connection(database_path)
    cursor = connection.cursor()

    if parent_id and element_type:
        if recursive:
            cursor.execute(
                """
                WITH RECURSIVE children_ids (id) AS (
                        SELECT child_id
                        FROM element_path
                        WHERE parent_id = ?
                    UNION
                        SELECT child_id
                        FROM element_path
                        JOIN children_ids ON (element_path.parent_id = children_ids.id)
                    ), element_ids (id) AS (
                        SELECT element.id FROM element JOIN children_ids USING (id) WHERE type = ?
                    )
                SELECT DISTINCT class_name FROM classification
                WHERE element_id IN element_ids
                """,
                (str(parent_id), element_type),
            )
        else:
            cursor.execute(
                """
                WITH element_ids as (SELECT element.id
                    FROM element
                    LEFT JOIN element_path ON (element.id = element_path.child_id)
                    WHERE (element.id IN (SELECT child_id FROM element_path WHERE parent_id = ?)
                    AND type = ?))
                SELECT DISTINCT class_name FROM classification
                WHERE element_id IN element_ids
                """,
                (str(parent_id), element_type),
            )
    elif element_type:
        cursor.execute(
            """
            WITH element_ids as (SELECT element.id
                FROM element
                WHERE type = ?)
            SELECT DISTINCT class_name FROM classification
            WHERE element_id IN element_ids
            """,
            (element_type,),
        )
    elif parent_id:
        if recursive:
            cursor.execute(
                """
                WITH RECURSIVE element_ids (id) AS (
                        SELECT child_id
                        FROM element_path
                        WHERE parent_id = ?
                    UNION
                        SELECT child_id
                        FROM element_path
                        JOIN element_ids ON (element_path.parent_id = element_ids.id)
                    )
                SELECT DISTINCT class_name FROM classification
                WHERE element_id IN element_ids
                """,
                (str(parent_id),),
            )
        else:
            cursor.execute(
                """
                WITH element_ids (id) AS (
                    SELECT element.id
                    FROM element
                    LEFT JOIN element_path ON (element.id = element_path.child_id)
                    WHERE element.id IN (SELECT child_id FROM element_path WHERE parent_id = ?)
                    )
                SELECT DISTINCT class_name FROM classification
                WHERE element_id IN element_ids
                """,
                (str(parent_id)),
            )
    else:
        cursor.execute(
            """
            SELECT DISTINCT class_name FROM classification
            """
        )

    result = cursor.fetchall()
    if result is None:
        return []
    columns = [item[0] for item in result]
    cursor.close()
    connection.close()
    return columns


@deprecated
def metadata_columns(
    database_path: str,
    parent_id: Optional[uuid.UUID],
    element_type: Optional[str],
    recursive: False,
    load_parents: False,
) -> List[str]:
    connection = sqlite3.Connection(database_path)
    cursor = connection.cursor()

    if load_parents:
        cursor.execute(
            """
            WITH RECURSIVE aggregated_metadata (name, elt_id) AS (
                    SELECT name, element_id
                    FROM metadata
                UNION ALL
                    SELECT md.name, element_path.child_id
                    FROM aggregated_metadata AS md INNER JOIN element_path ON (md.elt_id = element_path.parent_id)
            )
            SELECT name, MAX(count) FROM (
                SELECT elt_id, name, COUNT(*) AS count
                FROM aggregated_metadata
                GROUP BY elt_id, name
            ) subquery GROUP BY name;
            """
        )
    elif parent_id and element_type:
        if recursive:
            cursor.execute(
                """
                WITH RECURSIVE children_ids (id) AS (
                        SELECT child_id
                        FROM element_path
                        WHERE parent_id = ?
                    UNION
                        SELECT child_id
                        FROM element_path
                        JOIN children_ids ON (element_path.parent_id = children_ids.id)
                    ), element_ids (id) AS (
                        SELECT element.id FROM element JOIN children_ids USING (id) WHERE type = ?
                    )
                SELECT name, MAX(count) FROM (
                SELECT element_id, name, COUNT(*) AS count
                FROM metadata
                WHERE element_id IN element_ids
                GROUP BY element_id, name
                ) subquery GROUP BY name;
                """,
                (
                    str(parent_id),
                    element_type,
                ),
            )
        else:
            cursor.execute(
                """
                WITH element_ids as (SELECT element.id
                    FROM element
                    LEFT JOIN element_path ON (element.id = element_path.child_id)
                    WHERE (element.id IN (SELECT child_id FROM element_path WHERE parent_id = ?)
                    AND type = ?))
                    SELECT name, MAX(count) FROM (
                    SELECT element_id, name, COUNT(*) AS count
                    FROM metadata
                    WHERE element_id IN element_ids
                    GROUP BY element_id, name
                    ) subquery GROUP BY name;
                """,
                (
                    str(parent_id),
                    element_type,
                ),
            )
    elif element_type:
        cursor.execute(
            """
            WITH element_ids as (SELECT element.id
                FROM element
                WHERE type = ?)
                SELECT name, MAX(count) FROM (
                SELECT element_id, name, COUNT(*) AS count
                FROM metadata
                WHERE element_id IN element_ids
                GROUP BY element_id, name
                ) subquery GROUP BY name;
            """,
            (element_type,),
        )
    elif parent_id:
        if recursive:
            cursor.execute(
                """
                WITH RECURSIVE element_ids (id) AS (
                        SELECT child_id
                        FROM element_path
                        WHERE parent_id = ?
                    UNION
                        SELECT child_id
                        FROM element_path
                        JOIN element_ids ON (element_path.parent_id = element_ids.id)
                    )
                SELECT name, MAX(count) FROM (
                SELECT element_id, name, COUNT(*) AS count
                FROM metadata
                WHERE element_id IN element_ids
                GROUP BY element_id, name
                ) subquery GROUP BY name;
                """,
                (str(parent_id),),
            )
        else:
            cursor.execute(
                """
                WITH element_ids (id) AS (
                    SELECT element.id
                    FROM element
                    LEFT JOIN element_path ON (element.id = element_path.child_id)
                    WHERE element.id IN (SELECT child_id FROM element_path WHERE parent_id = ?)
                    )
                SELECT name, MAX(count) FROM (
                SELECT element_id, name, COUNT(*) AS count
                FROM metadata
                WHERE element_id IN element_ids
                GROUP BY element_id, name
                ) subquery GROUP BY name;
                """,
                (str(parent_id),),
            )
    else:
        cursor.execute(
            """
            SELECT name, MAX(count) FROM (
                SELECT element_id, name, COUNT(*) AS count
                FROM metadata
                GROUP BY element_id, name
                ) subquery GROUP BY name;
            """
        )

    result = cursor.fetchall()
    cursor.close()
    connection.close()
    if result is None:
        return []
    columns = []
    for name, count in result:
        if count > 1:
            for i in range(1, count + 1):
                column_name = f"{name}_{i}"
                assert (
                    column_name not in columns
                ), f"Duplicate metadata column: {column_name}."
                columns.append(column_name)
                i += 1
        else:
            if name not in columns:
                columns.append(name)
    return columns


@deprecated
def element_classes(
    database_path: str,
    element_id: str,
    classification_worker_version: Optional[uuid.UUID],
) -> Optional[List[Classification]]:
    """
    Retrieve an element's classes.
    """

    connection = sqlite3.Connection(database_path)
    cursor = connection.cursor()

    if classification_worker_version == "manual":
        cursor.execute(
            """
            SELECT class_name, id, confidence, worker_version_id FROM classification
            WHERE element_id = ? AND classification.worker_version_id IS NULL;
            """,
            (element_id,),
        )

    elif classification_worker_version:
        cursor.execute(
            """
            SELECT class_name, id, confidence, worker_version_id FROM classification
            WHERE element_id = ? AND classification.worker_version_id = ?;
            """,
            (element_id, classification_worker_version),
        )
    else:
        cursor.execute(
            """
            SELECT class_name, id, confidence, worker_version_id FROM classification
            WHERE element_id = ?;
            """,
            (element_id,),
        )
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    if result is None:
        return
    return list(starmap(Classification, result))


@deprecated
def transcription_entities(database_path: str) -> Optional[List[TranscriptionEntity]]:
    """
    Retrieve all transcription entities in the corpus
    """

    connection = sqlite3.Connection(database_path)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT transcription_id, transcription.element_id, entity_id, entity_type.name, entity.name, entity.metas, offset, length
        FROM transcription_entity
        INNER JOIN entity_type ON entity.type_id = entity_type.id
        INNER JOIN entity ON entity_id = entity.id
        INNER JOIN transcription ON transcription_id = transcription.id
        ORDER BY transcription_id, entity_id
        """,
    )

    result = cursor.fetchall()
    cursor.close()
    connection.close()
    if result is None:
        return
    return list(starmap(TranscriptionEntity, result))


@deprecated
def element_image(database_path: str, element_id: str) -> Optional[Image]:
    """
    Gets the absolute path to the database and the element_id, and
    returns the url of the element as a string
    """
    # connection to the database
    connection = sqlite3.Connection(database_path)
    cursor = connection.cursor()

    # query execution
    cursor.execute(
        """
        SELECT image.id, url
        FROM image
        JOIN element ON image.id = element.image_id
        WHERE element.id = ?;
        """,
        (element_id,),
    )

    # gets the image id and the url corresponding to an element_id
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result is None:
        return
    return Image(*result)


@deprecated
def recursive_element_transcriptions(
    database_path: str,
    element_id: str,
    transcription_worker_version: Optional[str] = None,
) -> Optional[Transcription]:

    # connection to the database
    connection = sqlite3.Connection(database_path)
    cursor = connection.cursor()

    params: list[str] = [
        element_id,
    ]
    extra_where = ""
    if transcription_worker_version is not None:
        extra_where = "AND transcription.worker_version_id = ?"
        params.append(transcription_worker_version)

    query = f"""
        WITH RECURSIVE child_ids (element_id) AS (
                SELECT child_id
                FROM element_path
                WHERE parent_id = ?
            UNION
                SELECT child_id
                FROM element_path
                JOIN child_ids ON (element_path.parent_id = child_ids.element_id)
        )
        SELECT
        transcription.id, transcription.element_id, text, transcription.confidence, transcription.worker_version_id
        FROM child_ids INNER JOIN transcription
        ON child_ids.element_id = transcription.element_id
        {extra_where};
        """

    params = list(map(str, params))

    cursor.execute(query, params)

    result = cursor.fetchall()
    cursor.close()
    connection.close()
    if result is None:
        return
    return list(starmap(Transcription, result))


@deprecated
def element_transcription(
    database_path: str,
    element_id: str,
    transcription_worker_version: Optional[str] = None,
) -> Optional[Transcription]:

    # connection to the database
    connection = sqlite3.Connection(database_path)
    cursor = connection.cursor()

    params: list[str] = [
        element_id,
    ]
    extra_where = ""
    if transcription_worker_version is not None:
        extra_where = "AND transcription.worker_version_id = ?"
        params.append(transcription_worker_version)

    query = f"""
        SELECT id, element_id, text, confidence, worker_version_id FROM transcription
        WHERE element_id = ?
        {extra_where};
        """

    params = list(map(str, params))

    cursor.execute(query, params)

    result = cursor.fetchall()
    cursor.close()
    connection.close()
    if result is None:
        return
    return list(starmap(Transcription, result))


@deprecated
def element_entities(
    database_path: str,
    element_id: str,
    worker_version_id: str = None,
) -> Optional[List[ElementEntity]]:

    connection = sqlite3.Connection(database_path)
    cursor = connection.cursor()

    params = [
        element_id,
    ]
    extra_where = ""
    if worker_version_id == "manual":
        extra_where = "AND transcription_entity.worker_version_id IS NULL"
    elif worker_version_id is not None:
        extra_where = "AND transcription_entity.worker_version_id = ?"
        params.append(worker_version_id)

    query = f"""
        SELECT entity_type.name, entity.name, ROW_NUMBER() OVER (PARTITION BY entity_type.name) AS number
        FROM transcription
        INNER JOIN transcription_entity ON transcription_entity.transcription_id = transcription.id
        INNER JOIN entity ON entity.id = transcription_entity.entity_id
        INNER JOIN entity_type ON entity_type.id = entity.type_id
        WHERE transcription.element_id = ?
        {extra_where}
        GROUP BY entity.id
        ORDER BY entity_type.name, entity.name;
        """

    params = list(map(str, params))

    cursor.execute(query, params)

    result = cursor.fetchall()
    cursor.close()
    connection.close()
    if result is None:
        return []
    return list(starmap(ElementEntity, result))


@deprecated
def entity_type_columns(
    database_path: str,
    parent_id: Optional[uuid.UUID],
    element_type: Optional[str],
    entities_worker_version: Optional[str],
    recursive: False,
) -> List[str]:
    connection = sqlite3.Connection(database_path)
    cursor = connection.cursor()

    params = []
    join = """
            FROM (
                SELECT transcription.element_id, entity_type.name, COUNT(*) AS count
                FROM element_ids INNER JOIN transcription ON element_ids.id = transcription.element_id
        """

    if parent_id:
        params = [parent_id, parent_id]
        if recursive:
            base_query = """
                WITH RECURSIVE child_ids (element_id) AS (
                    SELECT ?
                UNION
                    SELECT child_id
                    FROM element_path
                    WHERE parent_id = ?
                UNION
                    SELECT child_id
                    FROM element_path
                    JOIN child_ids ON (element_path.parent_id = child_ids.element_id)
                )
            """
        else:
            base_query = """
                WITH element_ids (id) AS (
                    SELECT ?
                UNION
                    SELECT element.id
                    FROM element
                    LEFT JOIN element_path ON (element.id = element_path.child_id)
                    WHERE element.id IN (SELECT child_id FROM element_path WHERE parent_id = ?)
                )
            """
        if element_type:
            if recursive:
                base_query = f"""
                    {base_query}
                    , element_ids (id) AS (
                        SELECT element.id FROM element JOIN child_ids ON element.id = element_id WHERE type = ?
                    )
                    """
            else:
                base_query = f"""
                    {base_query}
                    , final_ids (id) AS (
                        SELECT element.id FROM element JOIN element_ids ON element.id = element_ids.id WHERE type = ?
                    )
                    """
                join = """
                    FROM (
                        SELECT transcription.element_id, entity_type.name, COUNT(*) AS count
                        FROM final_ids INNER JOIN transcription ON final_ids.id = transcription.element_id
                    """
            params.append(element_type)
    else:
        if element_type:
            base_query = """
                WITH element_ids as (SELECT element.id
                    FROM element
                    WHERE type = ?)
            """
            params.append(element_type)
        else:
            base_query = ""
            join = """
                FROM (
                    SELECT transcription.element_id, entity_type.name, COUNT(*) AS count
                    FROM element INNER JOIN transcription ON element.id = transcription.element_id
            """

    if parent_id and recursive and not element_type:
        join = """
                FROM (
                    SELECT transcription.element_id, entity_type.name, COUNT(*) AS count
                    FROM child_ids INNER JOIN transcription ON child_ids.element_id = transcription.element_id
            """

    if entities_worker_version == "manual":
        where = "WHERE transcription_entity.worker_version_id IS NULL"
    elif entities_worker_version is not None:
        where = "WHERE transcription_entity.worker_version_id = ?"
        params.append(entities_worker_version)
    else:
        where = ""

    query = f"""
        {base_query}
        SELECT subquery.name, MAX(count)
        {join}
        INNER JOIN transcription_entity ON transcription_entity.transcription_id = transcription.id
        INNER JOIN entity ON entity.id = transcription_entity.entity_id
        INNER JOIN entity_type ON entity_type.id = entity.type_id
        {where}
        GROUP BY transcription.element_id, entity_type.name
        ) subquery GROUP BY name;
    """

    params = list(map(str, params))

    cursor.execute(query, params)
    result = cursor.fetchall()

    if result is None:
        return []
    columns = []
    for name, count in result:
        if count > 1:
            for i in range(1, count + 1):
                column_name = f"entity_{name}_{i}"
                assert (
                    column_name not in columns
                ), f"Duplicate entity type column: {column_name}."
                columns.append(column_name)
                i += 1
        else:
            if name not in columns:
                columns.append(f"entity_{name}")
    cursor.close()
    connection.close()
    return columns


@deprecated
def get_worker_version(database_path: str, worker_version_id: str) -> Optional[Worker]:
    """
    Returns the worker namedtuple from the given element id
    """

    # connection to the database
    connection = sqlite3.Connection(database_path)
    cursor = connection.cursor()

    # query execution
    cursor.execute(
        """
        SELECT
        worker_version.id, worker_version.name, slug, worker_version.type, revision
        FROM worker_version
        WHERE worker_version.id = ?;
        """,
        (worker_version_id,),
    )

    # gets the image id and the url corresponding to an element_id
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result is None:
        return
    return Worker(*result)
