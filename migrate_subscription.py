from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    conn = db.engine.connect()

    # ── User table new columns ───────────────────────────────────────────────
    user_cols_to_add = [
        ("subscription_plan",  "VARCHAR(20) DEFAULT 'free'"),
        ("subscription_start", "DATE"),
        ("subscription_end",   "DATE"),
    ]

    # Get existing user columns from MySQL
    result = conn.execute(text("SHOW COLUMNS FROM user"))
    existing_user_cols = {row[0] for row in result}
    print("Existing user columns:", existing_user_cols)

    for col, definition in user_cols_to_add:
        if col not in existing_user_cols:
            conn.execute(text(f"ALTER TABLE user ADD COLUMN {col} {definition}"))
            conn.commit()
            print(f"  + Added user.{col}")
        else:
            print(f"  ~ user.{col} already exists, skipping")

    # ── Movie table new column ───────────────────────────────────────────────
    result = conn.execute(text("SHOW COLUMNS FROM movie"))
    existing_movie_cols = {row[0] for row in result}
    print("Existing movie columns:", existing_movie_cols)

    if "is_premium" not in existing_movie_cols:
        conn.execute(text("ALTER TABLE movie ADD COLUMN is_premium TINYINT(1) DEFAULT 0"))
        conn.commit()
        print("  + Added movie.is_premium")
    else:
        print("  ~ movie.is_premium already exists, skipping")

    # ── Enter default data into subscription_plan table ──────────────────────
    print("\nChecking subscription_plan table...")
    try:
        # Check if table has data
        result = conn.execute(text("SELECT COUNT(*) FROM subscription_plan"))
        count = result.scalar()
        
        if count == 0:
            print("Entering default plans (Basic, Premium)...")
            # Insert plans
            conn.execute(text("INSERT INTO subscription_plan (name, price, duration_days) VALUES ('Basic', 199.0, 30)"))
            conn.execute(text("INSERT INTO subscription_plan (name, price, duration_days) VALUES ('Premium', 499.0, 30)"))
            conn.commit()
            print("  + Plans added successfully.")
        else:
            print(f"  ~ Plans already exist ({count} records found).")
            
        # ── Standardize existing user records ────────────────────────────────
        print("\nStandardizing user data...")
        
        conn.execute(text("""
            UPDATE user SET 
                subscription_plan = 'premium',
                subscription_start = CURDATE(),
                subscription_end = DATE_ADD(CURDATE(), INTERVAL 30 DAY)
            WHERE is_subscribed = 1 AND subscription_plan = 'free'
        """))
        conn.commit()
        print("  + User plans updated based on subscription status.")
        
    except Exception as e:
        print(f"  ! Data entry failed (Ensure you ran run.py once first): {e}")

    conn.close()
    print("\nMigration and data entry complete! Restart the server with: python run.py")
