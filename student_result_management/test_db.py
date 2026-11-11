from database import check_connection
from config import Config

def main():
    print("=" * 60)
    print("Student Result Management System - MongoDB Atlas Test")
    print("=" * 60)
    print(f"Target Database : {Config.DB_NAME}")
    print(f"Connection URI  : {Config.MONGO_URI[:35]}...")
    print("-" * 60)
    print("Testing connection...")
    ok, msg = check_connection()
    if ok:
        print("[SUCCESS]", msg)
    else:
        print("[FAILED] Could not connect to MongoDB Atlas:")
        print(msg)
        print("\nPlease update your MONGO_URI in .env file.")

if __name__ == '__main__':
    main()
