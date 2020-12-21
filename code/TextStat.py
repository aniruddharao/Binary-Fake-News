import csv
import codecs
from textstat.textstat import textstat

syllable_score = 0
flesch_reading_score = 0
flesch_grade_score = 0
fog_score = 0
smog_score = 0
ari_score = 0
cli_score = 0
lwf_score = 0
dcrs_score = 0

Channels = ["cityworld", "cnn", "dailytime", "empire", "foreignpolicy", "fox", "goneleft", "mutiny", "nbc",
            "news70", "newspolitics", "nytimes", "realnews", "truth", "usgreat", "webdaily", "whitehouse"]

#for channel in Channels:

#for each newspaper's fullData.csv content we are doing analyses
with codecs.open("CleanDataTextStat.csv", 'w', "utf-8-sig") as outputFile:

    writer = csv.writer(outputFile, dialect='excel')
    header_row = ["URL", "Content",  "Words", "Sentences", "CharWoSpaces", "CharSpaces",
                  "Syllable", "Flesch Reading","Flesch Grade", "FOG",
                  "SMOG", "ARI", "CLI", "LWF", "DCRS"]
    writer.writerow(header_row)

    with codecs.open("cleandata.csv", 'r', "ISO-8859-1") as inputFile:
        reader = csv.reader(inputFile)
        firstline = True
        for row in reader:
            if firstline:
                firstline = False
                continue
            content = row[5]
            if not content:
                output_row = [row[0], content, 0,0,0,0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0]
                writer.writerow(output_row)
                continue

            #Analyses for each content
            number_words = len(content.split())
            number_of_sentences = content.count('.')
            number_of_chars_spaces = len(list(content))
            number_of_chars_wospaces = len(list(content.replace(' ', '')))
            syllable_score = textstat.syllable_count(content)
            flesch_reading_score = textstat.flesch_reading_ease(content)
            flesch_grade_score = textstat.flesch_kincaid_grade(content)
            fog_score = textstat.gunning_fog(content)
            smog_score = textstat.smog_index(content)
            ari_score = textstat.automated_readability_index(content)
            cli_score = textstat.coleman_liau_index(content)
            lwf_score = textstat.linsear_write_formula(content)
            dcrs_score = textstat.dale_chall_readability_score(content)

            output_row = [row[0], content, number_words,
                          number_of_sentences, number_of_chars_wospaces, number_of_chars_spaces,
                          syllable_score, flesch_reading_score, flesch_grade_score,
                          fog_score, smog_score, ari_score, cli_score, lwf_score, dcrs_score]
            writer.writerow(output_row)