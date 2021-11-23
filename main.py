import sys
from lecture import fetch_course
from config import CONFIG

if __name__ == '__main__':
    course_id = sys.argv[1]

    if len(sys.argv) > 2:
        course_name = sys.argv[2]
    else:
        course_name = CONFIG['NameMap'][course_id]

    fetch_course(course_id, course_name, CONFIG['DownloadTo'])
