from lecture import fetch_course

TO_DOWNLOAD_COURSE_ID = "5c187582e1c3b136b759c0b1"
TO_DOWNLOAD_COURSE_NAME = "趣味韩语零基础一月特训班"
DOWNLOAD_TO = "/volume1/Courses/万门"

if __name__ == '__main__':
    fetch_course(TO_DOWNLOAD_COURSE_ID, TO_DOWNLOAD_COURSE_NAME, DOWNLOAD_TO)
