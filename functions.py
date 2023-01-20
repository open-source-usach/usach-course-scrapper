

def log(code, courses = []):
    if code == 0:
        print("[❌] NO DATA")

    if code == 1:
        print("[🐛] BUGGED/NON-TRUSTABLE DATA")

    if code == 2:
        courses = list(dict.fromkeys(courses))
        print(f"[🔎] FOUND {len(courses)}:")
        for course in courses:
            print(course)
