import subprocess


def md5sum_dir(directory):
    # this sure is ugly.
    # BUG - figure out why the tars keep generating different shas for the same content
    proc = subprocess.Popen("find \"{}\" -type f ! -name '*.tar.gz' -exec md5sum {{}} \; | sort -k 2 | md5sum".format(directory.decode('utf-8')),
                            shell=True,
                            stdout=subprocess.PIPE)
    raw_stdout = proc.stdout.read()
    return raw_stdout.split()[0].decode('utf-8')
