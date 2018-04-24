#Strip all url to retrieve the domain name only.
import string
import re
import os

dataFile = open('data.txt', 'r');
data = dataFile.read();

#strip protocol - http:// or https://
strippedData = data.replace("http://", "");
strippedData = strippedData.replace("https://", "");

#strip query - abc.com/files/abc.txt
strippedData = re.sub("\/[\w\/.]*", "", strippedData);

#strip quotes (and other details if needed)
strippedData = strippedData.replace("\"", "");
strippedData = strippedData.replace("\'", "");

#strip anything else after the domain that is not a line break
strippedData = re.sub(" ([^\n]{1,})", "", strippedData);


#finally, make format consistent by stripping all www. prefix
#strippedData = strippedData.replace("www.", "");

print(strippedData);


fh = open("stripped_data.txt","w");
fh.write(strippedData);
fh.close();
dataFile.close();

