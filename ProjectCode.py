#Import statements
import nltk
import os
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from statistics import mean
import string
import warnings
warnings.filterwarnings("ignore")

#Getting the dataset and defining functions for cleaning it
os.chdir("C:\\Users\\15104\\Desktop\\Kavitha College\\Spring 2020\\Textmining\\Project")
f=open('Dataset.txt','r')
data=f.read().lower().strip("\n")
sent_tokens = nltk.sent_tokenize(data)
word_tokens = nltk.word_tokenize(data)
lemmer = nltk.stem.WordNetLemmatizer()
def lemtokenization(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct = dict((ord(punct), None) for punct in string.punctuation)
def lemnormalization(text):
    return lemtokenization(nltk.word_tokenize(text.lower().translate(remove_punct)))

#Code for greeting the user
f1=open('greetings.txt','r')
inputs = f1.readlines()
inputs = [x.strip('\n').lower() for x in inputs]
responses = ["hi", "hey", "hi there", "hello", "I am glad! You are talking to me"]
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in inputs:
            return random.choice(responses)
    
#Function for creating bot responses based on the user input    
def response(user_response):
    user_response=user_response.lower()
    bot_response=''
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            return("You are welcome..")
        else:
            if(greeting(user_response)!=None):
                return greeting(user_response) 
            else:
                sent_tokens.append(user_response)
                tfidfvec = TfidfVectorizer(tokenizer=lemnormalization, stop_words='english')
                tfidf = tfidfvec.fit_transform(sent_tokens)
                cosvals = cosine_similarity(tfidf[-1], tfidf)
                index = cosvals.argsort()[0][-2]
                flatval = cosvals.flatten()
                flatval.sort()
                req_tfidf = flatval[-2]
                if(req_tfidf==0):
                    sent_tokens.remove(user_response)
                    return ("I am sorry! I don't understand you !\nPlease visit Alaska airlines website (https://www.alaskaair.com/) for more details.")
                else:
                    sent_tokens.remove(user_response)
                    bot_response = bot_response+sent_tokens[index+1]
                    return bot_response 
    else:
        return("Bye! take care..")
        
#Creating a GUI with tkinter:
#Step 1: Create a window and set its title
from tkinter import NORMAL,INSERT,END,DISABLED,Tk,FALSE,Text,Scrollbar,Button
window = Tk()
window.title("ViraBot")
window.geometry("400x495")
window.resizable(width=FALSE, height=FALSE)

def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    if msg != '':
        with open('questions.txt', 'a') as f:
            f.write("{}\n".format(msg))
        ChatLog.config(state=NORMAL)
        ChatLog.tag_config('you',foreground="red", font=("Arial",9))
        ChatLog.tag_config('bot',foreground="#442265", font=("Arial",9))
        ChatLog.insert(END, "You: " + msg + '\n\n','you')
        res = response(msg)
        ChatLog.insert(END, "Vira: " + res + '\n\n','bot')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
        
#Create Chat window
ChatLog = Text(window, bd=0, bg="white", height="8", width="50", font="Arial")
ChatLog.insert(INSERT,"Vira: I am your chatbot! I'm still learning, so I may not be able to answer all your questions just yet! For now, I will answer your queries regarding Covid19 updates on Cancellation, Seating and Safety measures, Baggage policies, Lounge services, Onboard services and Regional travel restrictions\n\n")
ChatLog.config(state=DISABLED)
ChatLog.config(foreground="#442265", font=("Arial",9))
#Bind scrollbar to Chat window
scrollbar = Scrollbar(window, command=ChatLog.yview, cursor="arrow")
ChatLog['yscrollcommand'] = scrollbar.set
#Create Button to send message
SendButton = Button(window, font=("Arail",9,'bold'), text="Send", width="10", height=5,
                    bd=0, bg="light blue", activebackground="#3c9d9b",fg='black',
                    command= send )
#Create the box to enter message
EntryBox = Text(window, bd=0, bg="white",width="29", height="5", font="Arial")
#Place all components on the screen
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=415, width=370)
EntryBox.place(x=90, y=430, height=58, width=285)
SendButton.place(x=6, y=430, height=58)
window.mainloop()


#Summary statistics:
#1.Word cloud
from nltk.corpus import stopwords
from wordcloud import WordCloud
import nltk
import matplotlib.pyplot as plt
stopwords=stopwords.words('english')
from nltk.stem import PorterStemmer
stemmer=PorterStemmer()
data=[stemmer.stem(x) for x in word_tokens]
data=' '.join([x for x in word_tokens if x.lower() not in stopwords and x.isalpha()])
wordcloud = WordCloud(max_font_size=60).generate(data) 
plt.imshow(wordcloud,interpolation="bilinear")
plt.show()

#2.Dispersion
from nltk.draw.dispersion import dispersion_plot
import nltk
text=nltk.word_tokenize(data)
dispersion_plot(text,['flight'])
dispersion_plot(text,['travel'])

#3.Distribution of questions based on topic and average number of words for questions in each topic
cancel=[];baggage=[];region=[];seatingsafety=[];lounge=[];onboard=[];greetings=[];others=[]
refund=[];cancellen=[];baglen=[];relen=[];reglen=[];slen=[];lonlen=[];onlen=[];greelen=[];olen=[]
with open('questions.txt','r') as f:
    lines=f.readlines()
    lines=[x.lower() for x in lines]
    for i in lines:
        if "cancel" in i or "changed" in i:
            cancel.append(i)
            cancellen.append(len(nltk.word_tokenize(i)))
        elif "refund" in i:
            refund.append(i)
            relen.append(len(nltk.word_tokenize(i)))
        elif "baggage" in i or "bags" in i:
            baggage.append(i)
            baglen.append(len(nltk.word_tokenize(i)))
        elif "region"in i or "travel" in i:
            region.append(i)
            reglen.append(len(nltk.word_tokenize(i)))
        elif "seating" in i or "safety" in i or "protect" in i or"social distancing" in i:
            seatingsafety.append(i)
            slen.append(len(nltk.word_tokenize(i)))
        elif "lounge" in i:
            lounge.append(i)
            lonlen.append(len(nltk.word_tokenize(i)))
        elif "onboard" in i or "food" in i or "beverage" in i or 'entertainment' in i:
            onboard.append(i)
            onlen.append(len(nltk.word_tokenize(i)))
        elif str(i).strip("\n") in inputs:
            greetings.append(i)
            greelen.append(len(nltk.word_tokenize(i)))
        else:
            others.append(i)
            olen.append(len(nltk.word_tokenize(i)))
            
z1 = round(mean(int(x) for x in cancellen))
z2 = round(mean(int(x) for x in slen))
z3 = round(mean(int(x) for x in reglen))
z4 = round(mean(int(x) for x in baglen))
z5 = round(mean(int(x) for x in lonlen))
z6 = round(mean(int(x) for x in onlen))
z7 = round(mean(int(x) for x in greelen))
z8 = round(mean(int(x) for x in olen))

from matplotlib import pyplot as plt
z = (z1,z2,z3,z4,z5,z6,z7,z8)
y = (len(cancel),len(seatingsafety),len(region),len(baggage),len(lounge),
     len(onboard),len(greetings),len(others))
x = ("Cancellation","Seating and Safety Measures","Regional advisories","Baggage",
     "Lounge Facilities","Onboard services","Greetings","Others")
plt.bar(x,y,align='center') # A bar char
plt.xlabel('Distribution of topics')
plt.xticks(rotation=90)
plt.ylabel('Number of questions asked')
plt.title("Distribution of different types of questions")
plt.show()

plt.bar(x,z,align='center') # A bar char
plt.xlabel('Distribution of topics')
plt.xticks(rotation=90)
plt.ylabel('Average length of questions')
plt.title('Average length of questions for each topic')
plt.show()