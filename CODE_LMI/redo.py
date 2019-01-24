# coding=utf-8
import re
import time
import subprocess
from multiprocessing.dummy import Pool
from datetime import timedelta

R4 = range(1, 5)


def getCommands(filePath="/PGSDATA/FY4A/L2/LMIXX/BBB/t.txt"):
    with open(filePath) as files:
        for i in files:
            a = re.search(r"(_\d{14}_)", i).start()
            b = re.search(r"N\d{2}V1", i).start()
            starttime = i[a + 1:a + 15]
            endtime = i[a + 16:a + 30]
            subTackNum = i[b + 1:b + 3]
            subTackNum = subTackNum.zfill(3)
            yield "/PGSWORK/FY4A/PRODPROG/yanghz/lMI_test_20180930/LIO.e F4ALHstrengR_FY4A-_LMI---_LLV" \
                  "%s_1MIN_%s_R N_REGX_1047E %s %s" % (
                      starttime, subTackNum, starttime, endtime)


def do_one(cmd, timeout=1800):
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT, stdout=ofn)
    print cmd, p.pid
    timeBegin = time.time()
    timeout += timeBegin
    while p.poll() is None:
        if timeout < time.time():
            p.terminate()
    print cmd, 'done',p.wait()
    print >>out, cmd, '', p.wait(), timedelta((time.time() - timeBegin)/86400)
    out.flush()


if __name__ == "__main__":
    p = Pool(5)
    with open(r'/dev/null', 'w') as oo, \
            open(r"/PGSDATA/FY4A/L2/LMIXX/BBB/time.txt", "w") as out:
        ofn = oo.fileno()
        try:
            for i in getCommands():
                p.apply_async(do_one, args=(i,))
            p.close()
            p.join()
        except:
            p.terminate()
            p.join()
