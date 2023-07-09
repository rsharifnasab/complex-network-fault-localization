#!/usr/bin/env python3

import os
from shutil import rmtree


from conf import *


def hot_cpp_questions(cur):
    cur.execute(
        """
SELECT
    problems.id,
    COUNT(DISTINCT testcases.id) AS testcase_count,
    COUNT(DISTINCT realfaultslocations_c_cpp.id) AS faulties_count
FROM
    problems
        JOIN
    source ON source.problems_id = problems.id
        JOIN
    languages ON source.languages_id = languages.id
        JOIN
    testcases ON testcases.problems_id = problems.id
        JOIN
    realfaultslocations_c_cpp ON realfaultslocations_c_cpp.subwrong = source.submission
WHERE
    languages.name = %s
        AND ((asimw > 70 AND wsima > 70)
        OR asimw > 90
        OR wsima > 90)
        AND matchlines > 20
        AND source.countLine > 20
        AND countfaults < 4
        AND source.verdicts_id = '2'
        AND testcases.isValid = 'pass'
GROUP BY problems.id
HAVING testcase_count > 19
    AND testcase_count < 60
    AND faulties_count > 1
ORDER BY faulties_count DESC
LIMIT 5
    """,
        (LANG, )
    )
    return [question[0] for question in cur]


def testcases(cur, question_id):
    cur.execute(
        """
        SELECT inputdata, expectedresult FROM testcases
        WHERE isValid = 'pass' AND problems_id = %s
        """,
        (question_id,)
    )
    res = [in_out for in_out in cur]
    return res


def main():
    db, cur = connect()
    questions = hot_cpp_questions(cur)
    try:
        rmtree(f"./result")
    except FileNotFoundError:
        pass
    os.mkdir(f"./result/")
    prob_file = open("./result/problems.txt", "w", encoding="UTF-8")
    for question_id in questions:
        t = testcases(cur, question_id)
        if len(t) < MIN_TEST_CASES:
            continue
        print(f"{question_id} -> have {len(t)} tests")
        prob_file.write(f"{question_id}\n")
        os.mkdir(f"./result/{question_id}")
        os.mkdir(f"./result/{question_id}/in")
        os.mkdir(f"./result/{question_id}/out")
        for i, (inp, out) in enumerate(t):
            f = open(f"./result/{question_id}/in/input{i+1}.txt", "w")
            f.write(str(inp))
            f.close()

            f = open(f"./result/{question_id}/out/output{i+1}.txt", "w")
            f.write(str(out))
            f.close()

    cur.close()
    db.close()
    prob_file.close()


if __name__ == "__main__":
    main()
