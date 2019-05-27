import sys, os, subprocess, datetime, shutil

def run_in_folder(folder, pargs):
    cwd = os.getcwd()
    os.chdir(folder)
    proc = subprocess.Popen(pargs, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    errcode = proc.returncode
    os.chdir(cwd)
    if out: out = out.decode('utf-8')
    if err: err = err.decode('utf-8')
    return out, err, errcode

def parse_date(dt):
    return datetime.datetime.strptime(dt.strip(), '%Y-%m-%d %H:%M:%S %z')

def get_historical_tags(project, start_tag):
    procargs = ["git", "--no-pager", "log", "--no-walk", "--tags", "--simplify-by-decoration", "--pretty=format:%ai#%D"]
    out, err, errcode = run_in_folder(project, procargs)
    date_version = []
    for line in out.splitlines():
        date, version_tag = line.split('#')
        xdate = parse_date(date)
        valid_version = True
        tag_split = version_tag.split(',')
        for tag in tag_split:
            try:
                tgidx = tag.index('tag: ')
            except:
                continue
            version = tag[tgidx + 5:].strip()
        if not version:
            # print("No correct tag? ", version_tag)
            valid_version = False
        for c in version:
            if not (c.isdigit() or c == '.'):
                valid_version = False
                # print("this is not a correct tag?", version_tag)

        if valid_version:
            date_version.append(version)
        # else:
            # print("Not a valid version tag: ", date, version_tag)

    result = ''
    for v in date_version:
        if v < start_tag:
            break
        else:
            result += v + '^!\n'

    result = '\n'.join(result.splitlines()[::-1])

    print(result)

if __name__ == '__main__':
    get_historical_tags(sys.argv[1], sys.argv[2])