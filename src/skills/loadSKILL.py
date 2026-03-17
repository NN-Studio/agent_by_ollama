#!/usr/bin/python3
# coding=utf-8

from os import path
from tools.readFile import readFile


def loadSKILL(SKILLName):
    return readFile(path.join("../skills", SKILLName, "SKILL.md"))
