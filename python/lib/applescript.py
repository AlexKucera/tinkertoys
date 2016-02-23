#!/usr/bin/env python
# encoding: utf-8
# Dr. Drang

# Description
"""

Release Notes:

http://www.leancrew.com/all-this/2013/03/combining-python-and-applescript/

Combining Python and AppleScript

March 6, 2013 at 10:34 PM by Dr. Drang

You may remember this post from last June, in which I had to rewrite a script that printed
out the current iTunes track. The original script was written in Python and used Hamish
Sanderson’s appscript library; the replacement was written in AppleScript.

I had to do the rewrite because an update to iTunes had broken the way appscript gets at
an application’s AppleScript dictionary. Hamish had stopped developing appscript because
Apple had deprecated the Carbon libraries he used to develop it and hadn’t replaced them
with Cocoa equivalents.

That post generated many thousands of words of commentary, most of it by Hamish and most
of the rest by Matt Neuburg. Although Matt came up with a clever workaround to
Ruby-appscript’s access to application dictionaries, and I thought seriously about
mimicking his work for Python-appscript, eventually I decided that I should just abandon
appscript. Because Apple has no proprietary interest in appscript, it will almost certainly
continue to make changes that undermine it.

Ferreting out all my appscript-using programs and changing them into pure AppleScript or
some Python/AppleScript hybrid wasn’t appealing, so I decided to just wait until a script
broke before rewriting it. Recently, my script for automatically generating invoice emails
broke, and I rewrote it into a combination of two AppleScripts and one Python script. It
worked, but I wasn’t happy with the results—it seemed both kludgy and fragile. What I
needed was a more general way to run AppleScript code from within my Python scripts.

I’ve touched on this topic before. Back then, I thought Kenneth Reitz’s envoy module was
the solution. I still like the idea of envoy, but the GitHub page has no real documentation,
and Kenneth’s own site seems to have been purged of most of his coding work in favor of
writing, photography, and music. Besides, envoy is a bit more general-purpose than I need.
Basically, I just want one or two wrapper functions around Python’s subprocess module that
will allow me to

Write an AppleScript as a Python string.
Run it from within my Python program.
Collect any output it generates.
With this, I’ll be able to keep all the code in one script instead of artificially breaking
it up into separate AppleScript and Python parts.

Here’s the module, applescript.py:

 1  #!/usr/bin/python
 2
 3  import subprocess
 4
 5  def asrun(ascript):
 6    "Run the given AppleScript and return the standard output and error."
 7
 8    osa = subprocess.Popen(['osascript', '-'],
 9                           stdin=subprocess.PIPE,
10                           stdout=subprocess.PIPE)
11    return osa.communicate(ascript)[0]
12
13  def asquote(astr):
14    "Return the AppleScript equivalent of the given string."
15
16    astr = astr.replace('"', '" & quote & "')
17    return '"{}"'.format(astr)

Without line numbers
There are just two functions: asrun, which takes the AppleScript string as its only
argument, runs it, and returns the output, if any; and asquote, which reconfigures any
string into a string that AppleScript can parse.

There’s not much to either one of these functions, but I can think of two things worth a
little explanation. You’ll note that the Popen in asrun doesn’t change the stderr parameter
from its default value of None. That’s because I wanted any AppleScript errors that arise
to propagate out into the surrounding script and get handled like any other Python
error—shutting the program down unless it’s in a try block. And instead of simply
backslash-escaping double quotes in asquote, I do the more verbose thing of splitting
the string at the double quotes and reconcatenating it with quotes. Doing it this way
seemed more AppleScripty, but maybe that’s just me. You could certainly change Line 16 to

16    astr = astr.replace('"', r'\"')

Without line numbers
if you think that’s better. The double backslash is necessary to get around Python’s
escaping rules. The raw string gets around Python’s escaping rules.

I have applescript.py saved in /Library/Python/2.7/site-packages so it’s available to all
my scripts. I have a feeling I’ll be changing it as I use it and find that it fails under
certain conditions. So far, though, it’s done what I want.

Here’s a short script using both asrun and asquote:

 1  #!/usr/bin/python
 2
 3  from applescript import asrun, asquote
 4
 5  subject = 'A new email'
 6
 7  body = '''This is the body of my "email."
 8  I hope it comes out right.
 9
10  Regards,
11  Dr. Drang
12  '''
13  ascript = '''
14  tell application "Mail"
15    activate
16    make new outgoing message with properties {{visible:true, subject:{0}, content:{1}}}
17  end tell
18  '''.format(asquote(subject), asquote(body))
19
20  print ascript
21  asrun(ascript)

Without line numbers
This does pretty much what you’d expect: after printing out the AppleScript source, it runs
it through osascript to create a new message in Mail with the Subject and Content fields
filled. Except for the format placeholders, and the doubled braces that format requires,
the AppleScript in Lines 14-17 is exactly as I’d write it in the AppleScript Editor. I
know Clark Goble will disagree, but I prefer this to the appscript syntax, which I found
awkward because it didn’t feel like real Python.

Since Hamish Sanderson and Matt Neuburg inadvertently contributed to this post, I should
recommend their AppleScript books. Hamish’s is the book I reach for now when I have an
AppleScript question; Matt’s is more concise and has excellent sections on the structure
and philosophy of AppleScript. And if you’re interested in scripting Mail, this tutorial
by Ben Waldie at MacTech is a great place to start and may well be where you finish.

"""

import subprocess


def asrun(ascript):
    "Run the given AppleScript and return the standard output and error."

    osa = subprocess.Popen(['osascript', '-'],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE)
    return osa.communicate(ascript)[0]


def asquote(astr):
    "Return the AppleScript equivalent of the given string."

    astr = astr.replace('"', '" & quote & "')
    return '"{}"'.format(astr)
