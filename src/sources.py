#!/usr/bin/env python3

import os
from shutil import rmtree


from conf import *


def sources(cur, problems_id, count=5):
    cur.execute(
        """
SELECT
    subwrong,
    faultlocations,
    sourceCode,
    languages.name
FROM
    code4bench.realfaultslocations_c_cpp
        JOIN
    source ON source.submission = realfaultslocations_c_cpp.subwrong
        JOIN
    languages ON languages.id = source.languages_id
WHERE
    ((asimw > 70 AND wsima > 70)
        OR asimw > 90
        OR wsima > 90)
        AND matchlines > 20
        AND source.countLine > 20
        AND countfaults < 4
        AND source.verdicts_id = '2'
        AND source.problems_id = %s
        AND languages.name = %s
LIMIT %s
""",
        (problems_id, LANG, count)
    )
    return [code for code in cur]


def persist(db_src, problem_id):
    sub_id, fault_locations, src, lang_name = db_src
    assert lang_name == LANG

    with open(f"./result/{problem_id}/sol{EXTENSION}", "w", encoding="UTF-8") as f:
        f.write(src)

    with open(f"./result/{problem_id}/sol_info.txt", "w", encoding="UTF-8") as f:
        print(f"sub id : {sub_id}")
        f.write(f"subid: {sub_id}\n")
        f.write(f"fault_locations: {fault_locations}\n")
        f.write(f"problem_id: {problem_id}\n")


def main():
    db, cur = connect()
    with open("./result/problems.txt", "r", encoding="UTF-8") as f:
        for problem_id in f:
            pid = int(problem_id.strip())
            srcs = sources(cur, pid)
            assert srcs, f"no source found for qid {problem_id}"

            persist(srcs[0], pid)
    cur.close()
    db.close()


if __name__ == "__main__":
    main()
