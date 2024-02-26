from hazm import *
import nltk
import random
import tqdm
import re
import codecs
import time

class CLOTHES_PROPERTIES_EXTRACTOR:
    def __init__(self, text):
        self.normalizer = Normalizer()
        self.lemmatizer = Lemmatizer()
        self.stemmer = Stemmer()
        self.tagger = POSTagger(model='postagger.model')
        self.text = text
    
    def run(self, flag=True):
        dic = {}
        dic = dic | self.SIZE_(flag)
        dic = dic | self.MATERIAL_(flag)
        dic = dic | self.QUALITY_(flag)
        dic = dic | self.MODEL_(flag)
        dic = dic | self.DESIGN_(flag)
        return dic
    
    def Is_Negative_Verb(self, verb):
        lem_verb = self.lemmatizer.lemmatize(verb)
        if verb.startswith('ن') and not lem_verb.startswith('ن') :
            return True
        elif verb.startswith('م') and not lem_verb.startswith('م') :
            return True

        return False
    
    
    def SENTENCE_TOKENIZER(self, Sentences):
        stopwords = [self.normalizer.normalize(x.strip()) for x in codecs.open('stopwords.dat','r','utf-8').readlines()]
        sentences = [[self.normalizer.normalize(i)for i in word_tokenize(sent) if i not in stopwords] for sent in sent_tokenize(Sentences)]
        sente=[]
        for sent in sentences:
            sente.append(' '.join(sent))
        return sente
    
    
    def POS_(self, Sentence):
        return self.tagger.tag(word_tokenize(Sentence))
    
    
    def VERB_IN_SENTENCE(self, Sentence_POS):
        verbs = []
        for j in range(len(Sentence_POS)):    
            if Sentence_POS[j][1] == 'V':
                verbs.append(Sentence_POS[j][0])
        return verbs
    
    
    def AJ_IN_SENTENCE(self, Sentence_POS):
        adjs = []
        for j in range(len(Sentence_POS)):

            if Sentence_POS[j][1] in ['AJ', 'AJe'] :
                adjs.append(Sentence_POS[j][0])
        return adjs
    
    
    def IS_RELATED_TO_CLOTHES(self, Sentence):
    
        pattern = (r'پیراهن|بلوز|شلوار|تی‌شرت|ژاکت|کاپشن|کت|جلیقه|هودی|شرت|شلوارک|کفش|پوش|لباس')
        if re.search(pattern, Sentence):
            return True
        else:
            return False 
    
    
    
    def SIZE_(self, flag):
        RESULT_DICT = {}
        SIZE_KEYWORDS = r'\bسایز|اندازه|قد'
        SIZE_L = r'\bلارج|ایکس لارج|دوایکس لارج|[X|x]*[L|l]|بزرگ'
        SIZE_M = r'\bمدیوم|متوسط|[M|m]'
        SIZE_S = r'\bاسمال|کوچی?ک|[S|s]'
        SIZE_NUM = r'\b[۱-۹][۱-۹]'
        flag_clothes = flag
        Sentences = self.text
        sentences = self.SENTENCE_TOKENIZER(Sentences)
        for i in sentences:
            if self.IS_RELATED_TO_CLOTHES(i):
                flag_clothes = True
        if flag_clothes :
            for sent in sentences:
                sent_POS = self.POS_(sent)
                if re.search(SIZE_KEYWORDS, sent):
                    span = re.search(SIZE_KEYWORDS, sent).span()
                    temp = sent[span[1]:]
                    temp_POS = self.POS_(temp)
                    verbs = self.VERB_IN_SENTENCE(temp_POS)
                    adj = self.AJ_IN_SENTENCE(sent_POS)

                    if re.search(SIZE_L, temp):
                        if  len(verbs) == 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['اندازه'] = [ 'بزرگ ' ]
                        else:
                            RESULT_DICT['اندازه'] = [ 'متوسط ' ]
    

                    elif re.search(SIZE_M, temp):
                        if len(verbs) == 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['اندازه'] = [ 'متوسط ' ]
                        else:
                            RESULT_DICT['اندازه'] = [ 'بزرگ یا کوچک ']


                    elif re.search(SIZE_S, temp):
                        if len(verbs) == 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':

                            RESULT_DICT['اندازه'] = [ 'کوچک ' ]
                        else:
                            RESULT_DICT['اندازه'] = [ 'متوسط ' ]

                    elif len(adj) == 1 :
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['اندازه'] = adj
                        else:
                            RESULT_DICT['اندازه'] = [adj[0] + ' ' + verbs[0]]


        return RESULT_DICT
    
    def MATERIAL_(self, flag):
        RESULT_DICT = {}
        MATERIAL_KEYWORDS = r'\bجنس'
        MATERIAL_G = r'\bخوب|عالی'
        MATERIAL_A = r'\bمعمولی|متوسط|قابل تحمل'
        MATERIAL_B = r'\bضعیف|بد|افتضاح'
        MATERIAL_S = r'\bنخی|پلاستیکی|پلی‌استر'
        flag_clothes = flag
        Sentences = self.text
        sentences = self.SENTENCE_TOKENIZER(Sentences)
        for i in sentences:
            if self.IS_RELATED_TO_CLOTHES(i):
                flag_clothes = True
        if flag_clothes :
            for sent in sentences:
                sent_POS = self.POS_(sent)
                if re.search(MATERIAL_KEYWORDS, sent):
                    span = re.search(MATERIAL_KEYWORDS, sent).span()
                    temp = sent[span[1]:]
                    temp_POS = self.POS_(temp)
                    verbs = self.VERB_IN_SENTENCE(temp_POS)
                    adj = self.AJ_IN_SENTENCE(sent_POS)
                    if re.search(MATERIAL_G, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['جنس'] = ['خوب']

                        else:
                            RESULT_DICT['جنس'] = ['بد']

                    elif re.search(MATERIAL_A, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['جنس'] = ['متوسط']

                        else:
                            RESULT_DICT['جنس'] = ['خوب']

                    elif re.search(MATERIAL_B, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['جنس'] = ['بد']

                        else:
                            RESULT_DICT['جنس'] = ['معمولی']

                    elif re.search(MATERIAL_G, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['جنس'] = ['خوب']

                        else:
                            RESULT_DICT['جنس'] = ['بد']

                    elif re.search(MATERIAL_S, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['جنس'] = [sent[span[0]:span[1]]]

                        else:
                            RESULT_DICT['جنس'] = ['معمولی']

                    elif len(adj) == 1:
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['جنس'] = adj
                        else:
                            RESULT_DICT['جنس'] = [adj[0] + ' ' + verbs[0]]
                            
        return RESULT_DICT
    
    
    def DESIGN_(self, flag):
        RESULT_DICT = {}
        DESIGN_KEYWORDS = r'\bطرح|دیزاین|نقش'
        DESIGN_G = r'\bخوب|عالی|فوق‌العاده|زیبا|شیک|خوشگل|خوشکل'
        DESIGN_A = r'\bمعمولی|متوسط|قابل تحمل'
        DESIGN_B = r'\bضعیف|بد|افتضاح|زشت'
        DESIGN_S = r'\bنخی|پلاستیکی|پلی‌استر'
        flag_clothes = flag
        Sentences = self.text
        sentences = self.SENTENCE_TOKENIZER(Sentences)
        for i in sentences:
            if self.IS_RELATED_TO_CLOTHES(i):
                flag_clothes = True
        if flag_clothes :
            for sent in sentences:
                sent_POS = self.POS_(sent)
                if re.search(DESIGN_KEYWORDS, sent):
                    span = re.search(DESIGN_KEYWORDS, sent).span()
                    temp = sent[span[1]:]
                    temp_POS = self.POS_(temp)
                    verbs = self.VERB_IN_SENTENCE(temp_POS)
                    adj = self.AJ_IN_SENTENCE(sent_POS)
                    if re.search(DESIGN_G, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['طرح'] = ['خوب']

                        else:
                            RESULT_DICT['طرح'] = ['بد']

                    elif re.search(DESIGN_A, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['طرح'] = ['متوسط']

                        else:
                            RESULT_DICT['طرح'] = ['خوب']

                    elif re.search(DESIGN_B, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['طرح'] = ['بد']

                        else:
                            RESULT_DICT['طرح'] = ['معمولی']

                    elif re.search(DESIGN_G, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['طرح'] = ['خوب']

                        else:
                            RESULT_DICT['طرح'] = ['بد']

                    elif re.search(DESIGN_S, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['طرح'] = [sent[span[0]:span[1]]]

                        else:
                            RESULT_DICT['طرح'] = ['معمولی']

                    elif len(adj) == 1:
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['طرح'] = adj
                        else:
                            RESULT_DICT['طرح'] = [adj[0] + ' ' + verbs[0]]
        return RESULT_DICT
    
    
    
    def QUALITY_(self, flag):
        RESULT_DICT = {}
        QUALITY_KEYWORDS = r'\bکیفیت دوخت|کیفیت'
        QUALITY_G = r'\bخوب|عالی'
        QUALITY_A = r'\bمعمولی|متوسط|قابل تحمل'
        QUALITY_B = r'\bضعیف|بد|افتضاح'
        QUALITY_S = r'\bخاص|سردوز'
        flag_clothes = flag
        Sentences = self.text
        sentences = self.SENTENCE_TOKENIZER(Sentences)
        for i in sentences:
            if self.IS_RELATED_TO_CLOTHES(i):
                flag_clothes = True
        if flag_clothes :
            for sent in sentences:
                sent_POS = self.POS_(sent)
                if re.search(QUALITY_KEYWORDS, sent):
                    span = re.search(QUALITY_KEYWORDS, sent).span()
                    temp = sent[span[1]:]
                    temp_POS = self.POS_(temp)
                    verbs = self.VERB_IN_SENTENCE(temp_POS)
                    adj = self.AJ_IN_SENTENCE(sent_POS)
                    if re.search(QUALITY_G, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['کیفیت دوخت'] = ['خوب']

                        else:
                            RESULT_DICT['کیفیت دوخت'] = ['بد']

                    elif re.search(QUALITY_A, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            print('here moto')
                            RESULT_DICT['کیفیت دوخت'] = ['متوسط']

                        else:
                            RESULT_DICT['کیفیت دوخت'] = ['خوب']

                    elif re.search(QUALITY_B, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['کیفیت دوخت'] = ['بد']

                        else:
                            RESULT_DICT['کیفیت دوخت'] = ['معمولی']

                    elif re.search(QUALITY_G, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['کیفیت دوخت'] = ['خوب']

                        else:
                            RESULT_DICT['کیفیت دوخت'] = ['بد']

                    elif re.search(QUALITY_S, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['کیفیت دوخت'] = [sent[span[0]:span[1]]]

                        else:
                            RESULT_DICT['کیفیت دوخت'] = ['معمولی']

                    elif len(adj) == 1:
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['کیفیت دوخت'] = adj
                        else:
                            RESULT_DICT['کیفیت دوخت'] = [adj[0] + ' ' + verbs[0]]
        return RESULT_DICT
    
    
    def MODEL_(self, flag):
        RESULT_DICT = {}
        MODEL_KEYWORDS = r'\bمدل|نوع'
        MODEL_G = r'\bچسبان|چسبون|تنگ'
        MODEL_A = r'\bگشاد|باز|آزاد|ازاد'
        flag_clothes = flag
        Sentences = self.text
        sentences = self.SENTENCE_TOKENIZER(Sentences)
        for i in sentences:
            if self.IS_RELATED_TO_CLOTHES(i):
                flag_clothes = True
        if flag_clothes :
            for sent in sentences:
                sent_POS = self.POS_(sent)
                if re.search(MODEL_KEYWORDS, sent):
                    span = re.search(MODEL_KEYWORDS, sent).span()
                    temp = sent[span[1]:]
                    temp_POS = self.POS_(temp)
                    verbs = self.VERB_IN_SENTENCE(temp_POS)
                    adj = self.AJ_IN_SENTENCE(sent_POS)
                    if re.search(MODEL_G, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['مدل'] = ['تنگ']

                        else:
                            RESULT_DICT['مدل'] = ['گشاد']

                    elif re.search(MODEL_A, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['مدل'] = ['گشاد']

                        else:
                            RESULT_DICT['مدل'] = ['تنگ']

                    elif len(adj) == 1:
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['مدل'] = adj
                        else:
                            RESULT_DICT['مدل'] = [adj[0] +' '+ verbs[0]]

        return RESULT_DICT