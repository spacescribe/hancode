import sqlite3
from datetime import datetime, timedelta
from db.vocab_db import db_path

def update_quiz_stats(word, correct):
    """Update performance tracking for each word."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO quiz_stats(word, attempts, correct, last_tested)
            VALUES(?, 1, ?, ?)
            ON CONFLICT(word) DO UPDATE SET
                attempts=attempts+1,
                correct = correct + ?,
                last_tested = excluded.last_tested
        """, (word, int(correct), datetime.now().isoformat(), int(correct)))
        conn.commit()

def get_recent_words(days=7):
    """Fetch words learned in `days` days"""
    since = (datetime.now()-timedelta(days=days)).isoformat()
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("""
            SELECT word, pinyin, english, example, english_translation, date_learned
            FROM vocab
            WHERE date_learned>=?
            ORDER BY date_learned DESC
        """, (since,))

        return cursor.fetchall()

def show_recent(days=7):
    fetched = get_recent_words(days)
    if not fetched:
        print("No vocabulary found for this period")
        return
    print(f"=== Words learned int the last {days} days ===")
    for w, p, e, ex, et, d in fetched:
        print(f"\n{p} - {e}")
        print(f"Example: {ex}")
        print(f"English Translation: {et}")
    
    print("===========================================")

def quiz_mode():
    """Simple interactive quiz"""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("""
            SELECT word, pinyin, english FROM vocab ORDER BY RANDOM() LIMIT 5
        """)
        questions = cursor.fetchall()

    if not questions:
        print("==== No Words learnt yet. Learn more first ...")
        return 
    
    print("\n🧠 Quiz Time! Translate the following words:\n")
    score = 0
    
    for word, pinyin, english in questions:
        answer = input(f"{word} ({pinyin}): ").strip()
        correct = (answer == english.lower())
        update_quiz_stats(word, correct)
        if correct:
            print("✅ Correct!")
            score+=1
        else:
            print(f"❌ Incorrect. It means: {english}")
    
    print(f"Your score: {score}/{len(questions)}")

def main():
    print("=== HanCode: Review mode ===")
    print("1. Show words learnt today")
    print("2. Show words learnt this week")
    print("3. Start quiz")
    print("4. Exit")

    while True:
        choice = input("\nSelect an option (1-4): ").strip()
        if choice == "1":
            show_recent(1)
        elif choice == "2":
            show_recent(7)
        elif choice == "3":
            quiz_mode()
        elif choice == "4":
            print("Goodbye! Keep practicing ✨")
            break
        else:
            print("Invalid choice. Try again.")

if __name__=="__main__":
    main()