#!/usr/bin/env python3
from ntpath import join
from pprint import pprint
from random import sample
import string
from tokenize import String
from typing import List
from urllib.parse import quote_plus
import re
import praw

def main():
    reddit = praw.Reddit("converterbot", config_interpolation="basic")

    # sampleSubmission = "https://www.reddit.com/r/ForzaOpenTunes/comments/s6elrn/2003_porsche_carrera_gt_my_competitive_purist_tune/"
    sampleSubmission = "https://www.reddit.com/r/ForzaOpenTunes/comments/s5mmcx/2005_vauxhall_monaro_this_build_is_probably_shit/" # "https://www.reddit.com/r/ForzaOpenTunes/comments/s66dk3/1999_lotus_elise_190_acceleration_focused_sprint/"

    submission = reddit.submission(url=sampleSubmission)
    convertedLines = processSelfText(submission.selftext.split('\n'))

    # if convertedLines != submission.selftext:
    #     submission.reply('\n'.join(convertedLines))

    # subreddit = reddit.subreddit("ForzaOpenTunes")
    # for submission in subreddit.stream.submissions():
    #     process_submission(submission)

complexMeasureRegEx = re.compile('(?P<value1>\d+\.?\d*)? ?(?P<measure>lb\/in|n\/mm|kgf\/mm|psi|bar).(?P<value2>\d+\.?\d*)', re.IGNORECASE & re.MULTILINE)
measureRegEx = re.compile('(\d+\.?\d*)\s*(lb\/in|n\/mm|kgf\/mm|kgf|psi|bar|cm|in)', re.IGNORECASE)

conversions = {
    'n/mm to lb/in': 0.5710147163,
    'n/mm to kgf': 0.1019716213,
    'psi to bar': 0.0689476,
}

def newtonsToKgf(value: float):
    return value * conversions["n/mm to kgf"]

def newtonsToLbs(value: float):
    return value * conversions["n/mm to lb/in"]

def kgfToNewtons(value:float):
    return value / conversions["n/mm to kgf"]

def lbsToNewtons(value: float):
    return value / conversions["n/mm to lb/in"]

def convertNewtons(value: float):
    return '{:.2f} lb/in, {:.2f} kgf'.format(newtonsToLbs(value), newtonsToKgf(value))

def convertPoundsPerInch(value: float):
    newtons = lbsToNewtons(value)
    return '{:.2f} n/mm, {:.2f} kgf'.format(newtons, newtonsToKgf(newtons))

def convertKgf(value: float):
    newtons = kgfToNewtons(value)
    return '{:.2f} n/mm, {:.2f} lb/in'.format(newtons, newtonsToLbs(newtons))

def psiToBar(value: float):
    return value * conversions["psi to bar"]

def barToPsi(value: float):
    return value / conversions["psi to bar"]

def convertPsi(value: float):
    return '{:.2f} bar'.format(psiToBar(value))

def convertBar(value: float):
    return '{:.2f} psi'.format(barToPsi(value))

def convertCm(value: float):
    return '{:.1f} in'.format(value * 0.393701)

def convertInch(value: float):
    return '{:.1f} cm'.format(value / 0.393701)

convertMap = {
    'lb/in': convertPoundsPerInch,
    'lbin': convertPoundsPerInch,
    'n/mm': convertNewtons,
    'kgf': convertKgf,
    'kgf/mm': convertKgf,
    'psi': convertPsi,
    'bar': convertBar,
    'cm': convertCm,
    'in': convertInch,
}

def processSelfText(lines: List[str]):
    converted = []

    for line in lines:
        matches = measureRegEx.findall(line)
        convertedLine = line
        if (len(matches) > 0):
            for match in matches:
                originalText = str.join(' ', (match[0], match[1]))
                value = float(match[0])
                converter = convertMap[match[1].lower()]
                if converter:
                    convertedText = converter(value)
                    # print(str.join(' ', (originalText, 'converts to', convertedText)))
                    convertedLine = convertedLine.replace(originalText, convertedText)
        converted += [convertedLine]

    print('{0:60s}{1}'.format('Original', 'Converted'))
    for index in range(len(lines)):
        print('{0:60s}{1:s}'.format(lines[index], str(converted[index])))

    return converted

if __name__ == "__main__":
    main()
