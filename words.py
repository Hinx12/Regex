#!/usr/bin/python3
# Nathan Lewis 201239940
# Assignment 3

import cgi, cgitb, os, re, sys, codecs, urllib.request
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
cgitb.enable()

#GLOBAL VARIABLES
wordDict = {}
count = 0

#Function to check whether URL/text meets conditions
def checkWords(text):
  
  global wordDict
  global count
  
  #Prints document entered by user
  print("<br><b style=color:#4CAF50;>Document Processed:</b>", text, "<br>")
   
  #Converts text to lower case
  newtext = text.lower()
  
  #Strips text of HTML markup
  newtext1 = re.sub(r'<[^<]+?>', '', newtext)
  
  #Stripping the text of quotation marks, graves and single grave
  newtext1 = re.sub(r'[\`\"]', '', newtext1)
  
  #Splitting text into possible words 
  word_list = re.split(r'\s|[!@#$%^&*.=+]|---|--|[-](\s|$)', newtext1)
  
  #For loop interating over each word in list
  #Searches for the correct words as conditions stated
  #Adds to dictionary
  for word in word_list:
    if not isinstance(word, str):
      continue        
    m = re.search(r'^(?P<group>(\`|\`\`|\"))?[A-Za-z][A-Za-z0-9]*((\'|\_|\-)[A-Za-z0-9]+)?(s\')?(?P=group)?$', word)
    if m:
      wordDict[word] = wordDict.get(word, 0) + 1
      count += 1
  
  #If length of dict > 1 then it contains "words" and calls outputTables
  #Elif length of dict = 1 it contains a "word" and calls outputTables
  #Else the dict must not contain any words therefore we don't print a table
  if len(wordDict) > 1:
    print("<br><b style=color:#4CAF50;>This Document contains ", count, "words</b><br>")
    outputTables(wordDict)
  elif len(wordDict) == 1:
    print("<br><b style=color:#4CAF50;>This Document contains 1 word</b><br>")
    outputTables(wordDict)
  else:
    print("<br><b style=color:red;>This Document contains 0 words</b><br>")
  
#Function to outputTables
def outputTables(myDict):
  
  #Sorts values(occurrances) by most frequent
  most_freq = sorted(wordDict.items(), key=lambda wordDict: wordDict[1],reverse=True)
  #Sorts values(occurrances) by least frequent
  least_freq = sorted(wordDict.items(), key=lambda wordDict: wordDict[1]) 
  
  #Prints start of table 1
  print('''
    <br><table border=1 style=text-align:center;float:left;width:300px;>
      <caption>10 Most Occurring Words </caption>
        <thead>
          <tr><th>No of Occurrences</th><th>Word</th>
          </tr>
        </thead>
        <tbody>''')
  
  #Iterates over keys and values up to a max of 10 then prints rows
  for key, value in most_freq[:10]:
    print("<tr><td>", value, "</td><td>", key, "</td></tr>") 
  
  #Closes table 1
  print('''
      </tbody>
    </table>''')
   
  #Prints start of table 2     
  print('''
    <table border=1 style=text-align:center;float:left;width:300px;>
      <caption>10 Least Occurring Words </caption>
        <thead>
          <tr><th>No of Occurrences</th><th>Word</th>
          </tr>
        </thead>
        <tbody>''')
  
  #Iterates over keys and values up to a max of 10 then prints rows
  for key, value in least_freq[:10]:
    print("<tr><td>", value, "</td><td>", key, "</td></tr>")
    
  #Closes table 2
  print('''
      </tbody>
    </table>''')                

#Checks if URL is valid
#Decodes and calls checkWords function passing the text
#If it can't the URL was not valid
def checkUrl(url):
  try:
    response = urllib.request.urlopen(url)
    text = response.read().decode('utf-8')
    print("<br><b style=color:#4CAF50;>URL Entered: </b>", url, "<br>")
    checkWords(text)
  except:
    print("<b style=color:red;>Could not retrieve URL, please try again</b>")
    
#Prints start of html   
print('''\
Content-type: text/html

<!DOCTYPE html>
<html style=align:center;>
  <head>
    <meta charset="utf-8">
    <title>CGI Python Script</title>
  </head>
  <body style = font-family:calibri;>''')

#Creates instance for FieldStorage
inputs = cgi.FieldStorage()

#Prints Heading
print('''<h1 style="color:#4CAF50;font-size:30px;text-align:center;">WORD COUNT PYTHON SCRIPT</h1>''')

#Function displays form
def formOutput():
  print('''\
	<form action="" method="post">
		<br><label>Enter your URL:</label><br>
			<input style=width:500px; type="text" name="URL"><br><br>
	  
		<label>Enter your Text:</label><br>
			 <textarea name="Words" rows="10" cols="70"></textarea><br><br>
		<input type="submit" value="Submit">
	  </form></section>''')

#Calling formOutput function	
formOutput()

#Checks the validity of the input from user
def inputValidation():
  if 'URL' in inputs and 'Words' in inputs:                         #Can't have both URL and text entered
    print("<h3 style=color:red;>Error Please only enter a URL or a piece of text, NOT BOTH!</h3>")
  elif 'Words' in inputs:                                           #If text entered in text box then it retrieves text and calls checkWords()
    checkWords(inputs.getvalue('Words'))
  elif 'URL' in inputs:                                             #If URL entered it retrieves URL and calls checkUrl()
    checkUrl(inputs.getfirst('URL'))
  else:                                                             #Else both fields must be empty
    print("<br><b>Please enter either a URL or a piece of Text</b>")
    
#Calls inputValidation function   
inputValidation()

#Ends HTML
print('''</body>\n</html>''')

