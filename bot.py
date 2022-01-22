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
from converters import convert

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

def processSelfText(lines: List[str]):
    originals = []
    converted = []

    for line in lines:
        matches = measureRegEx.findall(line)
        convertedLine = line
        if (len(matches) > 0):
            for match in matches:
                originalText = str.join(' ', (match[0], match[1]))
                value = float(match[0])
                convertedText = convert(match[1], value)
                # print(str.join(' ', (originalText, 'converts to', convertedText)))
                convertedLine = convertedLine.replace(originalText, convertedText)
            converted += [convertedLine]
            originals += [line]

    print('{0:60s}{1}'.format('Original', 'Converted'))
    for index in range(len(originals)):
        print('{0:60s}{1:s}'.format(originals[index], str(converted[index])))

    return converted

if __name__ == "__main__":
    main()
