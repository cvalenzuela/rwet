#!/usr/bin/python
# http://www.leancrew.com/all-this/2013/03/combining-python-and-applescript/
# http://www.mactech.com/articles/mactech/Vol.23/23.01/2301applescript/index.html
# http://eastmanreference.com/complete-list-of-applescript-key-codes/

# AppleScripts

import subprocess

# run applescript
def asrun(ascript):
    "Run the given AppleScript and return the standard output and error."

    osa = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return osa.communicate(ascript)[0]

# prepare string to run in applescript
def asquote(astr):
    "Return the AppleScript equivalent of the given string."

    astr = astr.replace('"', '" & quote & "')
    return '"{}"'.format(astr)

# paste string
def paste_text(first):
    if len(first) > 2:
        return '''
        tell application "System Events"
         	keystroke {0}
        end tell
        '''.format(asquote(first))
    else:
        linebreak()

def linebreak():
    return '''
    tell application "System Events"
        key code 36 -- new lines
    end tell
    '''

#  get current text
current_text = '''
-- activate the app
tell application "Microsoft Word"
	activate
end tell

-- get selected text only
-- tell application "Microsoft Word" to set selectedText to content of text object of selection

-- get the current text
tell application "Microsoft Word"
	tell active document
		set currentText to content of text object
		return currentText
	end tell
end tell
'''
