#!/usr/bin/env python3
"""Create the volunteer applications table in the configured database."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from __init__ import app, db
from model.volunteers import VolunteerApplication


def main():
    with app.app_context():
        engine = db.engine
        table = VolunteerApplication.__table__

        if db.inspect(engine).has_table(table.name):
            print(f"Table {table.name} already exists in the configured database.")
            return

        table.create(bind=engine, checkfirst=True)
        if not db.inspect(engine).has_table(table.name):
            raise RuntimeError(f"Failed to create table {table.name}.")

        print(f"Created table {table.name} in the configured {engine.dialect.name} database.")


if __name__ == "__main__":
    main()
