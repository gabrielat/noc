# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# sp delete event
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        self.db.execute(SQL_PROC)


SQL_PROC = """
CREATE OR REPLACE
FUNCTION delete_event(INTEGER)
RETURNS VOID
AS
$$
DECLARE
    p_event_id ALIAS FOR $1;
BEGIN
    DELETE FROM fm_eventrepeat
    WHERE event_id=p_event_id;

    DELETE FROM fm_eventdata
    WHERE event_id=p_event_id;

    DELETE FROM fm_eventlog
    WHERE event_id=p_event_id;

    DELETE FROM fm_event
    WHERE id=p_event_id;
END;
$$ LANGUAGE plpgsql;
"""
