
import urllib.request
import os
datadict={}
link = "data.py"
linkd = "https://github.com/kdslibs/commands/raw/main/d.txt"
links = "https://github.com/kdslibs/commands/raw/main/s.txt"
linkk = "https://github.com/kdslibs/commands/raw/main/k.txt"
linkw= "https://raw.githubusercontent.com/kdslibs/commands/main/d.txt"


current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the resource file
resource_file_path = os.path.join(current_dir, link)


def setLink(src,linki):
  global  linkd, links,linkk
  if (src=="d"):
    linkd = linki
  elif  (src=="s"):
    links=linki
    print(links)
  elif (src=="k"):
    linkk=linki
  else:
    link=linki


def printLink():
  global  linkd, links,linkk
  print(link)
  print(links)
  print(linkk)
  print(linkd)
  print(linkw)


def printall():
  print(readData(link))

def printsall():
  print(readData(links))

def printdall():
  print(readData(linkd))

def printkall():
  print(readData(linkk))


def printhead(dataSearch):
  printchead(link,dataSearch)


def printdhead(dataSearch):
  printchead(linkd,dataSearch)

def printkhead(dataSearch):
  printchead(linkk,dataSearch)

def printshead(dataSearch):
  printchead(links,dataSearch)

def printchead(link,dataSearch):
  strs=readData(link).split("###ENDOFSEGMENT###")
  for index in range(0,len(strs)):
      segmentData=strs[index].split("##HEADER##")
      if dataSearch in segmentData[0]:
        if len(segmentData)>1:
          #print(segmentData[0])
          #print("\n")
          print(segmentData[1])
        else:
          print(segmentData[0])
          print("No Data")

def readData(linki):
  #print(linki)
  with urllib.request.urlopen(linki) as url:
      s = url.read()
      # I'm guessing this would output the html source code ?
      return s.decode()

def printheader():
  print(printcheader(link))

def printsheader():
  print(printcheader(links))

def printdheader():
  print(printcheader(linkd))

def printkheader():
  print(printcheader(linkk))


def printcheader(link):
  strs=readData(link).split("###ENDOFSEGMENT###")
  for index in range(0,len(strs)):
      segmentData=strs[index].split("##HEADER##")
      print(segmentData[0])

def convert_to_alphanumeric(input_string):
    alphanumeric_string = ''.join(char for char in input_string if char.isalnum())
    return alphanumeric_string

def getData():
  global datadict
  file_contents=""
  file_path = resource_file_path  # Replace with the actual file path
  #print(file_path)
  try:
    with open(file_path, 'r') as file:
        file_contents = file.read()
        #print(file_contents)
  except FileNotFoundError:
    print(f"File '{file_path}' not found.")
  except IOError:
    print(f"Error reading file '{file_path}'.")

  strs=file_contents.split("###ENDOFSEGMENT###")
  for index in range(0,len(strs)):
      segmentData=strs[index].split("##HEADER##")
      if len(segmentData)==2:
        datadict[convert_to_alphanumeric(segmentData[0])] = segmentData[1]

getData()

def getKeys():
  return datadict.keys()

def println(key):
  print(datadict[key])
