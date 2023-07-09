#!/usr/bin/env python3
import os
import re
from re import findall
from os.path import isfile, join
from os import system as shell
from os import remove, makedirs, listdir
import shutil
from shutil import rmtree
import sys

from conf import EXTENSION

TEST_DIR = f"./sandbox/tests"
IN_FILES = TEST_DIR + "/in"
OUT_FILES = TEST_DIR + "/out"


def file_name_2_number(file_name):
    name = file_name.split(".")[0]
    number = findall(r"\d+", name)[-1]
    return int(number)


def get_last_file_number():
    files = [f for f in listdir(IN_FILES) if isfile(join(IN_FILES, f))]
    files.sort(key=file_name_2_number)
    last_file = files[-1] if len(files) > 0 else "input0.txt"  # empty
    last_num = file_name_2_number(last_file)
    return last_num


def closed_range(start, stop, step=1):
    offset = 1 if (step > 0) else -1
    return range(start, stop + offset, step)


def cmp_file(file_a, file_b):
    content_a = open(file_a, "r", encoding="UTF-8").read()
    content_b = open(file_b, "r", encoding="UTF-8").read()

    text1 = re.sub(r'\s+', ' ', content_a).strip()
    text2 = re.sub(r'\s+', ' ', content_b).strip()
    return text1 == text2


def execute_one_testcase(i: int, sol: str, validation=False):
    is_failed = False
    try:
        os.remove("./sandbox/sol")
        os.remove("./sandbox/sol.gcda")
        os.remove("./sandbox/sol.gcno")
    except FileNotFoundError:
        pass

    compile()
    inp = IN_FILES + f"/input{i}.txt"
    out = OUT_FILES + f"/output{i}.txt"

    out_chk = OUT_FILES + f"/output{i}.tmp"

    shell(f"cat {inp} | {sol} > {out_chk}")
    if validation:
        passed = isfile(out)
        passed = passed and cmp_file(out, out_chk)
        if not passed:
            print(f"error on test {i}")
            is_failed = True

    remove(out_chk)

    gcov_report(i)

    return is_failed


def execute_all_Tests(sol):
    all_failed = []
    end_index = get_last_file_number()
    for i in closed_range(1, end_index):
        is_failed = execute_one_testcase(i, sol, validation=True)
        if is_failed:
            all_failed.append(i)

    return all_failed


def compile():
    ret = shell(f"""cd ./sandbox && g++ \
                -O0 -g -w \
                -fprofile-arcs -ftest-coverage \
                 -fdump-tree-all-graph \
                ./sol{EXTENSION} \
                -o ./sol && cd ..
        """)
    assert ret == 0


def gcov_report(i):
    retcode = shell(""" cd sandbox && \
            gcovr --json --exclude-throw-branches \
            | jq '.files[0]' > gcov.json && \
            cd ..
          """)
    assert retcode == 0, "failed to call gcovr"
    shutil.move("./sandbox/gcov.json", f"./sandbox/gcov-{i}.json")


def main(qid):
    try:
        rmtree("./sandbox")
    except FileNotFoundError:
        pass
    makedirs("./sandbox/tests")
    shutil.copytree(f"./result/{qid}/in", "./sandbox/tests/in")
    shutil.copytree(f"./result/{qid}/out", "./sandbox/tests/out")
    shutil.copy(f"./result/{qid}/sol{EXTENSION}", "./sandbox/")
    compile()
    failed = execute_all_Tests("./sandbox/sol")
    with open(f"./result/{qid}/failed.txt", "w", encoding="UTF-8") as f:
        f.write("\n".join(map(str, failed)))
        f.write("\n")


if __name__ == "__main__":
    main(sys.argv[1])
