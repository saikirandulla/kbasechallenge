from flask import Flask, render_template, request, Response, json
import urllib
import sys
import requests
import itertools
import string

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] =True

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/output', methods=['POST'])
def reassemble():
    _text =  request.form['inputText']
    if _text:
        return  Response(outputtext(_text),status=200)
    else:
        return json.dumps({'html':'<span>Enter the text</span>'})

def outputtext(_text):
    a=[]
    for line in _text.split('\n'):
        txt =urllib.unquote_plus(line.rstrip('\n').encode('ascii'))
        #txt = txt.replace("+"," ")
        a.append(txt[:-1])
    return assemble(a)
#Return the first fragment of a shuffled sequence
#if there is atleast one connecting fragment on the left continue
#checking for other fragment combinations
# if there is no connecting fragment on the left return frag1 as the
# first fragment of the sequence
def getFirstChunk(a):
	for frag1 in a:
		b=a[:]
		b.remove(frag1)
		lst=[]
		for frag2 in b:
			lst.append(findLeftOverlap(frag1,frag2))
		if True in lst:
			continue
		else:
			return frag1
#finds the overlap on the right side of a fragment
def findLeftOverlap(frag1, frag2):
    max_offset = len(frag2)  # can't overlap with greater size than len(b)
    found=False
    for i in reversed(range(3,max_offset)):
        # checks for equivalence of decreasing sized slices upto 3
        # characted chunks
        if frag2[-i:]==frag1[:i]:
        	found=True
        	break
    return found
#finds the overlap on the right side of a fragment
def findRightOverlap(frag1, frag2):
    max_offset = len(frag2)  # can't overlap with greater size than len(b)
    found=False
    for i in reversed(range(3,max_offset)):
        # checks for equivalence of decreasing sized slices
        if frag1[-i:]==frag2[:i]:
        	return frag2
#Given a fragment, returns the connecting fragment on the right
def getConnectingChunk(frag1,a):
	b=a[:]
	b.remove(frag1)
	lst=[]
	for frag2 in b:
		if findRightOverlap(frag1,frag2) == frag2:
			break
	return frag2
#Merge ordered fragments with overlapping characters
#check for overlap from max length of fragment2 to minimum overlap
#of 3 characters
def merge(frag1,frag2):
	max_offset = len(frag2)  # can't overlap with greater size than len(b)
	x=""
	for i in reversed(range(3,max_offset)):
		if frag1[-i:]==frag2[:i]:
			x= frag1 + frag2[i:]
			break
	return x
#main function that calls methods to find first fragment, then find the order
#of the sequence and then merge the fragments with overlapping characters
def assemble(a):
	ordered_text=[]
	ordered_text.append(getFirstChunk(a))
	ordered_text.append(getConnectingChunk(ordered_text[0],a))
	for i in range(len(a)):
		if getConnectingChunk(ordered_text[-1],a) in ordered_text:
			continue
		else:
			ordered_text.append(getConnectingChunk(ordered_text[-1],a))
	#Assemble the ordered fragments
	assembled_text=[]
	for i in range(len(ordered_text)-1):
		if len(assembled_text)==0:
			assembled_text.append(merge(ordered_text[i],ordered_text[i+1]))

		else:
			assembled_text.append(merge(assembled_text[i-1],ordered_text[i+1]))
	return ''.join(assembled_text[-1:])

if __name__ == "__main__":
    app.run()
