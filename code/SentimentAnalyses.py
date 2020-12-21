import sys
import os
import csv
import codecs
sys.path.append(os.path.join(os.getcwd(),'..'))
import watson_developer_cloud
import watson_developer_cloud.natural_language_understanding.features.v1 as features
nlu = watson_developer_cloud.NaturalLanguageUnderstandingV1(version='2017-02-27',
                                                            username='de3b2e7d-1112-47d9-b788-6015f6573ad9',
                                                            password='gfdSD4kzOHVK')

Channels = ["cityworld", "cnn", "dailytime", "empire", "foreignpolicy", "fox", "goneleft", "mutiny", "nbc",
            "news70", "newspolitics", "nytimes", "realnews", "truth", "usgreat", "webdaily", "whitehouse"]

#Two output files to title and content sentiments
Analyze_Files = ["SentimentTitle.csv", "SentimentContent.csv"]

#for channel in Channels:
# index at 1 and 3 is Title and Content in FullData.csv; we are toggling for them
#index = 1
index = 3
for value in Analyze_Files:
    #for each newspaper's fullData.csv content and title we are doing analyses
    with codecs.open("CleanData" + value, 'w', "utf-8-sig") as outputFile:

        writer = csv.writer(outputFile, dialect='excel')
        head = "Title"
        if index == 5: head = "Content"
        header_row = ["URL", head, "Sentiment Score", "Sentiment Label", "Sadness", "Joy", "Fear", "Disgust", "Anger"]
        writer.writerow(header_row)

        with codecs.open("cleandata.csv", 'r', "ISO-8859-1") as inputFile:
            reader = csv.reader(inputFile)
            firstline = True
            for row in reader:
                if firstline:
                    firstline = False
                    continue
                nluObject = {}

                #Sentiment analyses for each [row][index]
                try:
                    nluObject = nlu.analyze(text=row[index], features=[features.Sentiment(),
                                                                       features.Emotion()], language='en')
                except watson_developer_cloud.watson_developer_cloud_service.WatsonException:
                    pass

                #The nluObject structure is given in the IBM Site in the form of json
                try:
                    sentiment_score = nluObject['sentiment']['document']['score']
                    sentiment_label = nluObject['sentiment']['document']['label']
                    sadness_score = nluObject['emotion']['document']['emotion']['sadness']
                    joy_score = nluObject['emotion']['document']['emotion']['joy']
                    fear_score = nluObject['emotion']['document']['emotion']['fear']
                    disgust_score = nluObject['emotion']['document']['emotion']['disgust']
                    anger_score = nluObject['emotion']['document']['emotion']['anger']
                except KeyError:
                    output_row = [row[0],row[index], 0, "neutral", 0, 0, 0, 0, 0]
                    writer.writerow(output_row)
                    continue

                output_row = [row[0],row[index],sentiment_score, sentiment_label,
                              sadness_score, joy_score, fear_score, disgust_score, anger_score]
                writer.writerow(output_row)
    index = 5
