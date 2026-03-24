from app.database import SessionLocal
from app.models.question import Question

def count_questions():
    db = SessionLocal()
    try:
        # Just count all, assuming all in DB are active since there is no is_active field
        total = db.query(Question).count()
        imco = db.query(Question).filter(Question.type == 'IMCO').count()
        fdac = db.query(Question).filter(Question.type == 'FDAC').count()
        
        print(f"Total Questions: {total}")
        print(f"IMCO Questions: {imco}")
        print(f"FDAC Questions: {fdac}")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    count_questions()
