# we need to write a custom script to install xtl & xsimd...
import sys, os, subprocess, datetime, shutil

env_dir, build_dir = sys.argv[1], sys.argv[2]

def extract_xtensor_version():
    # tag = 'git describe --exact-match --abbrev=0'
    with open(os.path.join(build_dir, "include/xtensor/xtensor_config.hpp")) as fi:
        for line in fi.readlines():
            if "XTENSOR_VERSION_MAJOR" in line:
                major = int(line.split(" ")[-1])
            if "XTENSOR_VERSION_MINOR" in line:
                minor = int(line.split(" ")[-1])
            if "XTENSOR_VERSION_PATCH" in line:
                patch = int(line.split(" ")[-1])
    return (major, minor, patch)

deps_cache_dir = os.path.join(env_dir, "deps_cache")

def check_create_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        return False
    else:
        return True

def try_remove_dir(dirname):
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
        return True
    else:
        return False

def get_dir(dirname):
    return os.path.join(env_dir, 'deps_cache', dirname)

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

def get_date_of_version(version):
    version_string = '.'.join([str(v) for v in version])
    out, err, errcode = run_in_folder(build_dir, 'git --no-pager log -1 --format=%ai'.split() + [version_string])
    xdate = parse_date(out)
    return xdate

def get_version_before(proj, xtensor_date):
    procargs = ["git", "--no-pager", "log", "--no-walk", "--tags", "--simplify-by-decoration", "--pretty=format:%ai#%D"]
    out, err, errcode = run_in_folder(get_dir(proj), procargs)

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
            print("No correct tag? ", version_tag)
            valid_version = False
        for c in version:
            if not (c.isdigit() or c == '.'):
                valid_version = False
                print("this is not a correct tag?", version_tag)

        if valid_version:
            date_version.append((xdate, version))
        else:
            print("Not a valid version tag: ", date, version_tag)

    for v in date_version:
        if v[0] < xtensor_date:
            print(f"Found {proj} {v[1]} for {xtensor_date}.")
            return v[1]

def checkout_install(folder, version):
    run_in_folder(get_dir(folder), ['git', 'checkout', version])
    build_folder = os.path.join(get_dir(folder), 'build')
    check_create_dir(build_folder)
    run_in_folder(build_folder, ['cmake', '..', '-DBUILD_TESTS=OFF', f'-DCMAKE_INSTALL_PREFIX={env_dir}'])
    run_in_folder(build_folder, ['make', 'install'])

def install_matching_version(proj):
    version = extract_xtensor_version()
    date = get_date_of_version(version)
    run_in_folder(get_dir(''), ['git', 'clone', f'https://github.com/QuantStack/{proj}'])
    run_in_folder(get_dir(proj), ['git', 'fetch'])
    checkout_install(proj, get_version_before(proj, date))

check_create_dir(deps_cache_dir)
install_matching_version('xsimd')
install_matching_version('xtl')
