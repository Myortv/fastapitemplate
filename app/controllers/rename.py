from asyncpg import Connection

from app.schemas.rename import (
    RenameInDB,
)

from plugins.controllers import (
    DatabaseManager as DM,
    # select_q,
    # insert_q,
    # update_q,
    # delete_q,
)

# DM.acqure_connection passes conn parameter to function
# make sure to declare conn as "conn=None"
@DM.acqure_connection()
async def get_by_name(
    name: int,
    conn: Connection = None,
) -> RenameInDB:
    result = await conn.fetchrow(
        'select * from pg_user where usename = $1',
        name,
    )
    if not result:
        # do not raise exception here, return None instead and raise exception in router
        return
    rename = RenameInDB(**result)
    return rename
