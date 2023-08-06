from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    ArrayType,
    MapType
)

from .shapes import (
    get_point_schema,
    get_bbox_schema,
    get_polygon_schema,
    get_polyline_schema,
)
from .comment import get_video_comment_schema
from .tag import get_tag_schema


def get_instance_metadata_schema():
    return StructType([
        StructField("type", StringType(), True),
        StructField("className", StringType(), True),
        StructField("start", IntegerType(), True),
        StructField("end", IntegerType(), True),
        StructField("creationType", StringType, True)
    ])


def get_timestamp_schema():
    return StructType([
        StructField("timestamp", IntegerType(), True),
        StructField("bbox", get_bbox_schema(), True),
        StructField("polygon", get_polygon_schema()),
        StructField("polyline", get_polyline_schema(), True),
        StructField("point", get_point_schema(), True),
        StructField("attributes", ArrayType(MapType(StringType(),
                                                    StringType())),
                    True)
    ])


def get_instance_parameter_schema():
    return StructType([
        StructField("start", IntegerType(), True),
        StructField("end", IntegerType(), True),
        StructField("timestamp", get_timestamp_schema(), True)
    ])


def get_instance_schema():
    StructType([
        StructField("meta", get_instance_metadata_schema(), True),
        StructField("parameters", get_instance_parameter_schema(), True)
    ])


def get_video_schema():
    return StructType([
        StructField("video_height", IntegerType(), True),
        StructField("video_width", IntegerType(), True),
        StructField("video_name", StringType(), True),
        StructField("url", StringType(), True),
        StructField("projectId", IntegerType(), True),
        StructField("duration", IntegerType(), True),
        StructField("status", StringType(), True),
        StructField("annotatorEmail", StringType(), True),
        StructField("qaEmail", StringType(), True),
        StructField("instances", ArrayType(get_instance_schema()),
                    True),
        StructField("comments", ArrayType(get_video_comment_schema()), True),
        StructField("tags", ArrayType(get_tag_schema()), True)
    ])
