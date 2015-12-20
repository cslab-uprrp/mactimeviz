#!/usr/bin/python

import cgi
import cgitb

cgitb.enable()

print "Content-type: text/html"
print

form = cgi.FieldStorage()

fileitem = form["fileField"]

n = open("practiceFile.txt", "w+")
n.write(fileitem.file.read())

n.close

print """
	<html>
	<body>

	<script>
	var form = document.createElement("form");
	var theName = document.createElement("input"); 
    var yTag = document.createElement("input");
    var mTag = document.createElement("input");
    var dTag = document.createElement("input");
    var tTag = document.createElement("input");

	form.method = "POST";
    form.action = "dataMaker.cgi";

    theName.value = "practiceFile.txt";
   	theName.name = "fileName";

   	yTag.value = 'empty';
    yTag.name = "yTag";
    mTag.value = 'empty';
    mTag.name = "mTag";
    dTag.value = 'empty';
    dTag.name = "dTag";
    tTag.value = 'empty';
    tTag.name = "tTag";

    form.appendChild(theName);  
    form.appendChild(yTag);
    form.appendChild(mTag);
    form.appendChild(dTag);
    form.appendChild(tTag);

    document.body.appendChild(form);

    form.submit();
    </script>
    </body>
    </html>

"""