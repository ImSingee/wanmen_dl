import sys
import json
from config import CONFIG

if __name__ == '__main__':
    course_id = sys.argv[1]
    course_name = sys.argv[2]

    CONFIG['NameMap'][course_id] = course_name

    print(CONFIG)

    with open('config.json', 'r') as f:
        json.dump(CONFIG, f, indent=4, ensure_ascii=False)