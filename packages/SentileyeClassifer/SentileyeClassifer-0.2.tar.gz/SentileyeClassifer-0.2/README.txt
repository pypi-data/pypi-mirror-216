Hello, you are welcome to SentiLEYE classifier

A sentiment lexicon algorithm to classify pidgin English and English text into positive, negative or neutral


To use this system, you can enter raw text or your document in a csv file format (for example, data.csv). You need to name the column as 'text'. 
The system creates new column for score and class.  You should expect the output as shown below. 

            text     score     class
the bank is good      2       positive


### How to use the packages

pip install SentileyeClassifer
from sentileye.polarity import result