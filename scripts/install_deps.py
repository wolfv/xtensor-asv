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

def fetch_xtl():
    run_in_folder(get_dir(''), ['git', 'clone', 'https://github.com/QuantStack/xtl'])
    run_in_folder(get_dir('xtl'), ['git', 'fetch'])
    # vals, err, errcode = run_in_folder(get_dir('xtl'), )

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

    print(out)
    date_version = []
    for line in out.splitlines():
        date, version_tag = line.split('#')
        print(date, version_tag)
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
                print("this is not a correct tag?")

        if valid_version:
            date_version.append((xdate, version))
        else:
            print("Not a valid version tag: ", date, version_tag)

    for v in date_version:
        if v[0] < xtensor_date:
            print("Found {} {} for {}.".format(proj, v[1], xtensor_date))
            return v[1]

def checkout_install(folder, version):
    run_in_folder(get_dir(folder), ['git', 'checkout', version])
    build_folder = os.path.join(get_dir(folder), 'build')
    check_create_dir(build_folder)
    run_in_folder(build_folder, ['cmake', '..', '-DCMAKE_INSTALL_PREFIX={}'.format(env_dir)])
    run_in_folder(build_folder, ['make', 'install'])

def install_matching_xsimd_version():
    version = extract_xtensor_version()
    date = get_date_of_version(version)
    run_in_folder(get_dir(''), ['git', 'clone', 'https://github.com/QuantStack/xsimd'])
    run_in_folder(get_dir('xsimd'), ['git', 'fetch'])
    checkout_install('xsimd', get_version_before('xsimd', date))

def install_matching_xtl_version():
    version = extract_xtensor_version()
    date = get_date_of_version(version)
    run_in_folder(get_dir(''), ['git', 'clone', 'https://github.com/QuantStack/xtl'])
    run_in_folder(get_dir('xtl'), ['git', 'fetch'])
    checkout_install('xtl', get_version_before('xtl', date))

# try_remove_dir(os.path.join(env_dir, 'xtl'))
# try_remove_dir(os.path.join(env_dir, 'xsimd'))
# try_remove_dir(os.path.join(env_dir, 'lib64/xtl'))
# try_remove_dir(os.path.join(env_dir, 'lib64/xsimd'))

check_create_dir(deps_cache_dir)
install_matching_xsimd_version()
install_matching_xtl_version()