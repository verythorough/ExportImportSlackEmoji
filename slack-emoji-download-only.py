import requests
import json
import re
import os
from os import walk

# --------------------------------------
# Set these 2 values then run the script 
# -------------------------------------
sourceSlackOrgCookie = ''
sourceSlackOrgToken = ''

emojiDownloadFolder = 'slackEmoji'
sourceSlackOrgHeaders = {'cookie': sourceSlackOrgCookie, 'Authorization' : f'Bearer {sourceSlackOrgToken}'}

if not os.path.exists(emojiDownloadFolder):
    os.makedirs(emojiDownloadFolder)

existingEmojiFileNames = []
for (dirpath, dirnames, filenames) in walk(emojiDownloadFolder):
    existingEmojiFileNames.extend(filenames)
    break

def getEmojiNameToUrlDict(headers):
    url = 'https://slack.com/api/emoji.list'
    response = requests.get(url, headers=headers)

    responseJson = json.loads(response.content)
    emojiNameToUrlDict = responseJson["emoji"]

    return emojiNameToUrlDict

# ----------------
# Do the downloading
# ----------------

emojiNameToUrlDict = getEmojiNameToUrlDict(sourceSlackOrgHeaders)

for emojiName in emojiNameToUrlDict:
     
    emojiUrl = emojiNameToUrlDict[emojiName]
    if not emojiUrl.startswith('alias:'):
        
        emojiFileExtension = re.search('\.\w+$', emojiUrl).group()

        emojiFileName = f'{emojiName}{emojiFileExtension}'

        if emojiFileName in existingEmojiFileNames:
            print(f'Emoji {emojiName}{emojiFileExtension} already downloaded, skipping download')
            continue

        response = requests.get(emojiUrl)

        # Write the resposne to a file
        invalidFileNameCharatersRegex = ':|;'
        emojiFileName = re.sub(invalidFileNameCharatersRegex, '_', emojiFileName)
        emojiFilePath = f'{emojiDownloadFolder}/{emojiName}{emojiFileExtension}'
        open(emojiFilePath, 'wb').write(response.content)

        print(f'Saved {emojiFilePath}')