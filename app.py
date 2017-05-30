from flask import Flask, render_template, request, Response, json
import urllib
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
    b=[]
    for line in _text.split('\n'):
        txt =urllib.unquote_plus(line.rstrip('\n'))
        a.append(txt[:-1])
    d=[]
    i=0
    for i in range(len(a)-1):
        if len(d)==0:
            d.append(merge(a[i],a[i+1]))
        else:
            d.append(merge(d[i-1],a[i+1]))
    #print(d)
    k=d[-1:]
    print (k)
    for item in k:
        l=item.split('\n')
    #for item in l:
    #	print (item)
    return k

def merge(a, b):
    max_offset = len(b)  # can't overlap with greater size than len(b)
    j=3
    x=""
    for j in range(3, max_offset+1)[::-1]:
        # checks for equivalence of decreasing sized slices
        if a[-j:] == b[:j]:
            x=a+b[j:]
            break
        else:
            continue
    return a+b[j:]
if __name__ == "__main__":
    app.run()
