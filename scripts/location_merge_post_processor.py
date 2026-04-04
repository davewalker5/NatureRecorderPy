import argparse
import sqlite3
from datetime import datetime
from pathlib import Path


def normalise_number(value):
    """
    For merge purposes:
    - NULL -> 1
    - 0    -> 1
    - n    -> n
    """
    if value is None or value == 0:
        return 1
    return value


def merge_gender(values):
    """
    Gender rules:
    - if any 1 and any 2 -> 3
    - elif any 1         -> 1
    - elif any 2         -> 2
    - else               -> 0
    """
    has_1 = any(v == 1 for v in values)
    has_2 = any(v == 2 for v in values)
    has_3 = any(v == 3 for v in values)

    if has_3:
        return 3
    if has_1 and has_2:
        return 3
    if has_1:
        return 1
    if has_2:
        return 2
    return 0


def merge_notes(rows):
    """
    Concatenate non-empty notes in Id order.
    Adjust the separator if you prefer something else.
    """
    notes = []
    for row in rows:
        note = row["Notes"]
        if note is not None:
            note = note.strip()
            if note:
                notes.append(note)

    return "\n\n".join(notes) if notes else None


def get_duplicate_groups(conn):
    """
    Return all duplicate groups based on Date + LocationId + SpeciesId.
    """
    sql = """
        SELECT
            Date,
            LocationId,
            SpeciesId,
            COUNT(*) AS RecordCount
        FROM Sightings
        GROUP BY Date, LocationId, SpeciesId
        HAVING COUNT(*) > 1
        ORDER BY COUNT(*) DESC, Date, LocationId, SpeciesId
    """
    return conn.execute(sql).fetchall()


def get_group_rows(conn, date_value, location_id, species_id):
    """
    Return all rows in a duplicate group, ordered so the first row is the keeper.
    """
    sql = """
        SELECT
            Id,
            LocationId,
            SpeciesId,
            Date,
            Number,
            WithYoung,
            Gender,
            Notes,
            Created_By,
            Updated_By,
            Date_Created,
            Date_Updated
        FROM Sightings
        WHERE Date = ?
          AND LocationId = ?
          AND SpeciesId = ?
        ORDER BY Id
    """
    return conn.execute(sql, (date_value, location_id, species_id)).fetchall()


def merge_group(conn, rows, apply_changes=False):
    """
    Merge one duplicate group into the first row.
    Returns a dict describing what happened.
    """
    keeper = rows[0]
    others = rows[1:]

    merged_with_young = 1 if any(row["WithYoung"] == 1 for row in rows) else 0
    merged_gender = merge_gender([row["Gender"] for row in rows])
    merged_notes = merge_notes(rows)
    merged_number = sum(normalise_number(row["Number"]) for row in rows)

    keeper_id = keeper["Id"]
    other_ids = [row["Id"] for row in others]

    result = {
        "keeper_id": keeper_id,
        "other_ids": other_ids,
        "date": keeper["Date"],
        "location_id": keeper["LocationId"],
        "species_id": keeper["SpeciesId"],
        "merged_number": merged_number,
        "merged_with_young": merged_with_young,
        "merged_gender": merged_gender,
        "merged_notes": merged_notes,
        "record_count": len(rows),
    }

    if apply_changes:
        update_sql = """
            UPDATE Sightings
            SET
                Number = ?,
                WithYoung = ?,
                Gender = ?,
                Notes = ?,
                Date_Updated = ?
            WHERE Id = ?
        """
        conn.execute(
            update_sql,
            (
                merged_number,
                merged_with_young,
                merged_gender,
                merged_notes,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                keeper_id,
            ),
        )

        delete_sql = f"""
            DELETE FROM Sightings
            WHERE Id IN ({",".join("?" for _ in other_ids)})
        """
        conn.execute(delete_sql, other_ids)

    return result


def process_duplicates(db_path, apply_changes=False, limit=None, record_id=None):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    try:
        duplicate_groups = get_duplicate_groups(conn)

        if record_id is not None:
            row = conn.execute(
                "SELECT Date, LocationId, SpeciesId FROM Sightings WHERE Id = ?",
                (record_id,),
            ).fetchone()

            if row is None:
                print(f"No record found with Id={record_id}")
                return

            duplicate_groups = [
                g for g in duplicate_groups
                if g["Date"] == row["Date"]
                and g["LocationId"] == row["LocationId"]
                and g["SpeciesId"] == row["SpeciesId"]
            ]

        if not duplicate_groups:
            print("No duplicate groups found.")
            return

        if limit is not None:
            duplicate_groups = duplicate_groups[:limit]

        print(f"Found {len(duplicate_groups)} duplicate group(s).")
        print("Mode:", "APPLY" if apply_changes else "DRY RUN")
        print()

        processed = 0
        deleted_rows = 0

        if apply_changes:
            conn.execute("BEGIN")

        for group in duplicate_groups:
            rows = get_group_rows(
                conn,
                group["Date"],
                group["LocationId"],
                group["SpeciesId"],
            )

            if len(rows) < 2:
                continue

            result = merge_group(conn, rows, apply_changes=apply_changes)

            processed += 1
            deleted_rows += len(result["other_ids"])

            print(
                f"Group {processed}: "
                f"Date={result['date']}, "
                f"LocationId={result['location_id']}, "
                f"SpeciesId={result['species_id']}, "
                f"records={result['record_count']}"
            )
            print(f"  Keeper Id: {result['keeper_id']}")
            print(f"  Delete Ids: {result['other_ids']}")
            print(f"  Merged Number: {result['merged_number']}")
            print(f"  Merged WithYoung: {result['merged_with_young']}")
            print(f"  Merged Gender: {result['merged_gender']}")
            if result["merged_notes"]:
                preview = result["merged_notes"].replace("\n", " | ")
                if len(preview) > 120:
                    preview = preview[:117] + "..."
                print(f"  Merged Notes: {preview}")
            else:
                print("  Merged Notes: <empty>")
            print()

        if apply_changes:
            conn.commit()
            print(
                f"Done. Processed {processed} group(s) and deleted {deleted_rows} duplicate row(s)."
            )
        else:
            print(
                f"Dry run complete. Would process {processed} group(s) and delete {deleted_rows} duplicate row(s)."
            )

    except Exception:
        if apply_changes:
            conn.rollback()
        raise
    finally:
        conn.close()


def main():
    # Determine the database path in the data folder
    project_folder = Path(__file__).parent.parent
    default_db_path = (project_folder / "data" / "naturerecorder.db").resolve()

    # Set up the command line parser
    parser = argparse.ArgumentParser(description="Roll up duplicate Sightings rows by Date + LocationId + SpeciesId.")
    parser.add_argument("-d", "--database", default=default_db_path, type=str, help="Path to the SQLite database file")
    parser.add_argument("-a", "--apply", action="store_true", help="Actually update/delete rows. Without this flag, the script only does a dry run.")
    parser.add_argument("-l", "--limit", type=int, default=None, help="Only process the first N duplicate groups (useful for testing).")
    parser.add_argument("-i", "--id", type=int, default=None, help="Only process the duplicate group containing the specified record ID.")
    args = parser.parse_args()

    if not Path(args.database).exists():
        raise FileNotFoundError(f"Database not found: {args.database}")

    process_duplicates(db_path=str(args.database), apply_changes=args.apply, limit=args.limit, record_id=args.id)


if __name__ == "__main__":
    main()
