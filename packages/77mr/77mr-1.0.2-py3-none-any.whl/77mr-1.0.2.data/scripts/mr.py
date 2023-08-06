import subprocess
import sys
from datetime import datetime

if __name__ == '__main__':
    tmp_name = datetime.now().strftime("%Y%m%d%H%M")
    [ret, target_name] = subprocess.getstatusoutput("git branch --show-current")
    if ret != 0:
        sys.exit(-1)
    create_mr = "git push origin head:{} -o merge_request.target={} -o merge_request.create -o merge_request.remove_source_branch -f".format(tmp_name, target_name)
    [ret, msg] = subprocess.getstatusoutput(create_mr)
    print(msg)