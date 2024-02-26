from hazm import *
import nltk
import random
import tqdm
import re
import codecs
import time

class DIGITAL_PROPERTIES_EXTRACTOR:
    def __init__(self, text):
        self.normalizer = Normalizer()
        self.lemmatizer = Lemmatizer()
        self.stemmer = Stemmer()
        self.tagger = POSTagger(model='postagger.model')
        self.text = text
    
    def run(self, flag=True):
        dic = {}
        dic = dic | self.SPEED(flag)
        dic = dic | self.BATTERY(flag)
        dic = dic | self.QUALITY_(flag)
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
    
    
    def IS_RELATED_TO_DIGITAL(self, Sentence):
    
        pattern = (r'|رم|حافظه|کیبرد|موس|دوربین|هندزفری|پاور بانک|هارد|تب لت|لپ تاب|موبایل|گوشی|فلش|کنترل|تلویزیون|صفحه نمایش|آدابتور|هارد|باتری')
        if re.search(pattern, Sentence):
            return True
        else:
            return False 
    
    
    
    def SPEED(self, flag):
        RESULT_DICT = {}
        SIZE_KEYWORDS = r'\bسرعت|بالا|روشن می شود|کار می کند'
        SIZE_L = r'\b|تند|بالا|سریع'
        SIZE_M = r'\bخوب|معمولی|مناسب'
        SIZE_S = r'\bکند|آهسته|زور'
        flag_clothes = flag
        Sentences = self.text
        sentences = self.SENTENCE_TOKENIZER(Sentences)
        for i in sentences:
            if self.IS_RELATED_TO_DIGITAL(i):
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
                            RESULT_DICT['سرعت'] = [ 'سریع' ]
                        else:
                            RESULT_DICT['سرعت'] = [ 'متوسط' ]
    

                    elif re.search(SIZE_M, temp):
                        if len(verbs) == 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['سرعت'] = [ 'متوسط' ]
                        else:
                            RESULT_DICT['سرعت'] = [ 'سریع یا کند']


                    elif re.search(SIZE_S, temp):
                        if len(verbs) == 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':

                            RESULT_DICT['سرعت'] = [ 'کند' ]
                        else:
                            RESULT_DICT['سرعت'] = [ 'متوسظ' ]

                    elif len(adj) == 1 :
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['اندازه'] = adj
                        else:
                            RESULT_DICT['اندازه'] = [adj[0] + ' ' + verbs[0]]


        return RESULT_DICT
    
    def BATTERY(self, flag):
        RESULT_DICT = {}
        MATERIAL_KEYWORDS = r'\bباتری|شارژدهی|نگه داشتن|شارژ'
        MATERIAL_G = r'\bخوب|عالی|زیاد|طولانی'
        MATERIAL_A = r'\bمعمولی|متوسط|قابل تحمل|مناسب'
        MATERIAL_B = r'\bضعیف|بد|کم|کوتاه|'
        flag_clothes = flag
        Sentences = self.text
        sentences = self.SENTENCE_TOKENIZER(Sentences)
        for i in sentences:
            if self.IS_RELATED_TO_DIGITAL(i):
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
                            RESULT_DICT['باتری'] = ['خوب']

                        else:
                            RESULT_DICT['باتری'] = ['متوسظ']

                    elif re.search(MATERIAL_A, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['باتری'] = ['متوسط']

                        else:
                            RESULT_DICT['باتری'] = ['خوب']

                    elif re.search(MATERIAL_B, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['باتری'] = ['بد']

                        else:
                            RESULT_DICT['باتری'] = ['متوسط']

                    elif re.search(MATERIAL_G, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['باتری'] = ['خوب']

                        else:
                            RESULT_DICT['باتری'] = ['بد']

                    elif len(adj) == 1:
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['باتری'] = adj
                        else:
                            RESULT_DICT['باتری'] = [adj[0] + ' ' + verbs[0]]

        return RESULT_DICT
    
    
    def DESIGN_(self, flag):
        RESULT_DICT = {}
        DESIGN_KEYWORDS = r'\bطرح|دیزاین|نقش'
        DESIGN_G = r'\bخوب|عالی|فوق‌العاده|زیبا|شیک|خوشگل|خوشکل'
        DESIGN_A = r'\bمعمولی|متوسط|قابل تحمل'
        DESIGN_B = r'\bضعیف|بد|افتضاح|زشت'
        flag_clothes = flag
        Sentences = self.text
        sentences = self.SENTENCE_TOKENIZER(Sentences)
        for i in sentences:
            if self.IS_RELATED_TO_DIGITAL(i):
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

                    elif len(adj) == 1:
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['طرح'] = adj
                        else:
                            RESULT_DICT['طرح'] = [adj[0] + ' ' + verbs[0]]
        return RESULT_DICT
    
    
    
    def QUALITY_(self, flag):
        RESULT_DICT = {}
        QUALITY_KEYWORDS = r'\bکیفیت|کیفیت'
        QUALITY_G = r'\bخوب|عالی'
        QUALITY_A = r'\bمعمولی|متوسط|قابل تحمل'
        QUALITY_B = r'\bضعیف|بد|افتضاح'
        flag_clothes = flag
        Sentences = self.text
        sentences = self.SENTENCE_TOKENIZER(Sentences)
        for i in sentences:
            if self.IS_RELATED_TO_DIGITAL(i):
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
                            RESULT_DICT['کیفیت'] = ['خوب']

                        else:
                            RESULT_DICT['کیفیت'] = ['بد']

                    elif re.search(QUALITY_A, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            print('here moto')
                            RESULT_DICT['کیفیت'] = ['متوسط']

                        else:
                            RESULT_DICT['کیفیت'] = ['خوب']

                    elif re.search(QUALITY_B, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['کیفیت'] = ['بد']

                        else:
                            RESULT_DICT['کیفیت'] = ['معمولی']

                    elif re.search(QUALITY_G, temp):
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['کیفیت'] = ['خوب']

                        else:
                            RESULT_DICT['کیفیت'] = ['بد']

                    elif len(adj) == 1:
                        if len(verbs)== 0 or self.Is_Negative_Verb(verbs[0]) == False and verbs[0] != 'نیست':
                            RESULT_DICT['کیفیت'] = adj
                        else:
                            RESULT_DICT['کیفیت'] = [adj[0] + ' ' + verbs[0]]
        return RESULT_DICT
    
