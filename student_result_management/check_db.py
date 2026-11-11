import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient

def run_check():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(env_path)
    uri = os.getenv('MONGO_URI')
    db_name = os.getenv('DB_NAME', 'student_result_db')

    print("=" * 60)
    print("MONGODB ATLAS HEALTH & FUNCTIONALITY CHECK")
    print("=" * 60)
    print(f"Target Database : {db_name}")
    print(f"URI Endpoint    : {uri[:35]}...")
    print("-" * 60)

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        
        # 1. Ping
        ping_res = client.admin.command('ping')
        print(f"✔ 1. Ping Check        : PASSED ({ping_res})")

        # 2. Database & Collections
        db = client[db_name]
        cols = db.list_collection_names()
        print(f"✔ 2. Collections Found : {cols}")

        # 3. Document Counts
        print("✔ 3. Document Counts   :")
        for c in ['users', 'students', 'subjects', 'examinations', 'results']:
            cnt = db[c].count_documents({})
            print(f"     - {c:<15}: {cnt} records")

        # 4. CRUD Test
        test_col = db['__health_check__']
        inserted_id = test_col.insert_one({'check': 'db_write', 'active': True}).inserted_id
        found = test_col.find_one({'_id': inserted_id})
        assert found['check'] == 'db_write', "Read verification failed"

        test_col.update_one({'_id': inserted_id}, {'$set': {'check': 'db_updated'}})
        updated = test_col.find_one({'_id': inserted_id})
        assert updated['check'] == 'db_updated', "Update verification failed"

        test_col.delete_one({'_id': inserted_id})
        assert test_col.find_one({'_id': inserted_id}) is None, "Delete verification failed"
        print("✔ 4. CRUD Lifecycle    : PASSED (Insert, Find, Update, Delete)")

        # 5. Data Integrity Samples
        print("✔ 5. Live Data Samples :")
        sample_student = db.students.find_one({}, {'_id': 0, 'student_name': 1, 'roll_number': 1, 'department': 1})
        sample_result = db.results.find_one({}, {'_id': 0, 'student_name': 1, 'subject_name': 1, 'marks_obtained': 1, 'grade': 1, 'status': 1})
        print(f"     - Sample Student  : {sample_student}")
        print(f"     - Sample Result   : {sample_result}")

        print("-" * 60)
        print("RESULT: Database is 100% ONLINE, RESPONSIVE & FUNCTIONAL!")
        print("=" * 60)
        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == '__main__':
    ok = run_check()
    sys.exit(0 if ok else 1)

