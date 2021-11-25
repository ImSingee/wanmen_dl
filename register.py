import sys
import json
from config import CONFIG

if __name__ == '__main__':
    course_id = sys.argv[1]
    
    if len(sys.argv) > 2:
        course_name = sys.argv[2]
    else:
        from names import names
        course_name = names[course_id]
        print(f"Course Name: {course_name}")

    CONFIG['NameMap'][course_id] = course_name

    print(CONFIG)

    with open('config.json', 'w') as f:
        json.dump(CONFIG, f, indent=4, ensure_ascii=False)
