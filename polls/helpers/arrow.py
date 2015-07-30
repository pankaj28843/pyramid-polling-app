from __future__ import absolute_import

from polls.settings import TIMEZONE


def format_arrow_object_datetime_string(arrow_obj):
    if arrow_obj is None:
        return ''

    return arrow_obj.to(TIMEZONE).format('DD-MM-YYYY hh:mm:ss A')
