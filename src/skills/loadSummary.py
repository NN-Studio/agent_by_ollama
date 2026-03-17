#!/usr/bin/python3
# coding=utf-8

from os import getcwd, path, listdir


def loadSummary():
    skillsroot_full = path.join(getcwd(), "skills")

    # 所有技能列表
    skillnames = [
        name
        for name in listdir(skillsroot_full)
        if path.isdir(path.join(skillsroot_full, name))
    ]

    content = []
    for skillname in skillnames:
        with open(path.join(skillsroot_full, skillname, "SKILL.md"), "r") as file:
            hadBegin = False
            skillSummary = []
            for line in file:
                if line.strip() == "---":
                    if hadBegin:
                        break
                    else:
                        hadBegin = True
                else:
                    skillSummary.append(line.strip())

            content.append(
                """
""".join(
                    skillSummary
                )
            )

    summary = """
""".join(
        content
    )
    return {
        "role": "user",
        "content": f"""这是可以用的技能，每次处理的时候，首先判断这里的是否可以解决问题，如果可以解决问题，必须用这里的:

        {summary}""",
    }
