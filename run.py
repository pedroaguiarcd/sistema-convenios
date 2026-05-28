from backend.database import criar_app_flask, db
from frontend.main import main
import flet as ft


def run_migrations():
    app = criar_app_flask()

    MIGRATIONS = [
        (
            "convenios",
            "nome",
            "ALTER TABLE convenios ADD COLUMN nome VARCHAR(100) NULL",
        ),
        (
            "empresas",
            "nome",
            "ALTER TABLE empresas ADD COLUMN nome VARCHAR(100) NULL",
        ),
    ]

    with app.app_context():
        conn = db.engine.connect()

        for table, column, sql in MIGRATIONS:
            result = conn.execute(
                db.text(
                    "SELECT COUNT(*) FROM information_schema.COLUMNS "
                    "WHERE TABLE_SCHEMA = DATABASE() "
                    "AND TABLE_NAME = :table "
                    "AND COLUMN_NAME = :column"
                ),
                {"table": table, "column": column},
            )
            exists = result.scalar() > 0

            if exists:
                print(f"  [skip]  {table}.{column} already exists.")
            else:
                conn.execute(db.text(sql))
                conn.commit()
                print(f"  [added] {table}.{column} created.")

        conn.close()
        print("\nMigration complete.")


if __name__ == "__main__":
    run_migrations()
    ft.run(
        main,
        assets_dir="uploads"
    )
