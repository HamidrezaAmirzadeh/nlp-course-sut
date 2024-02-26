import re
import codecs
from hazm import *

class BookPropertiesExtrator:
    def __init__(self):
        self.normalizer = Normalizer()
        self.lemmatizer = Lemmatizer()
        self.stemmer = Stemmer()
        self.tagger = POSTagger(model='postagger.model')


    #stopwords = [normalizer.normalize(x.strip()) for x in codecs.open('stopwords.txt','r','utf-8').readlines()]

    def rem_punc(self,text):
        res = ''
        for char in text:
            if char not in '! # $ % & \ ( ) * + , - ؛ < > » « . / : ; < = > ? @ [ \ ] ^ _ ` { | } ، ؟'.split():
                res += char
        return res

    def preprocess(self,comment):
        # Sentence tokenization
        comment_sents = sent_tokenize(comment)

        # Remove punctuations
        comment_sents_nopunc = [rem_punc(sent) for sent in comment_sents]

        # Word tokenization
        tokens = [[word_tokenize(word) for word in sent.split()] for sent in comment_sents_nopunc]

        # Normalization
        tokens_norm  = [[normalizer.normalize(token[0]) for token in ls] for ls in tokens]

        # Lemmatization
        tokens_lemm = [[lemmatizer.lemmatize(token) for token in ls] for ls in tokens_norm]

        # Removing stopwords
        tokens_nostop = [[token for token in ls if token not in stopwords] for ls in tokens_lemm]

        return tokens_nostop
    def Is_Negative_Verb(self,verb):

        lem_verb = self.lemmatizer.lemmatize(self.normalizer.normalize(verb))
        if verb.startswith('ن') and not lem_verb.startswith('ن') :
            return True
        if verb == 'نیست':
            return True
        return False
    def cost_extract(self,sentences, phrases):
        """ Output : one of three classes ['زیاد', 'مناسب', 'کم'] """

        for i,s in enumerate(sentences):
            for key in phrases:
                span = re.search(key,s)
                if span:
                    start = span.start()
                    sent = sentences[i][start:]

                 # neg_sent = False
                    tagger = POSTagger(model='postagger.model')
                    tags = tagger.tag(sent.split())
                    for tag in tags:
                        if tag[1] == 'V':
                            verb = tag[0]
                            neg_sent = self.Is_Negative_Verb(verb)
                        # if verb[0] == 'ن':
                        #     neg_sent = True
                
                    pattern_ziad = r'زیا+د | با+لا+ | گرا+ن | گرو+ن | بد'
                    if re.search(pattern_ziad, sent):
                        if neg_sent == False:
                            return {'زیاد' : 'قیمت'}
                        else:
                            return {'مناسب' : 'قیمت'}
                
                    pattern_monaseb = r'منا+سب | به صرفه | منطقی | متناسب | خوب'
                    if re.search(pattern_monaseb, sent):
                        if neg_sent == False:
                            return {'مناسب' : 'قیمت'}
                        else:
                            return {'زیاد' : 'قیمت'}

                    pattern_kam = r'کم | ارزا+ن | مفت | پایی+ن'
                    if re.search(pattern_kam, sent):
                        if neg_sent == False:
                            return {'کم' : 'قیمت'}
                        else:
                            return {'زیاد' : 'قیمت'}
                    break
            if span:
                break
            return {}
    def discount_extract(self,sentences, phrases):
        """ Output : one of two classes ['دارد', 'ندارد'] """

        for i,s in enumerate(sentences):
            for key in phrases:
                span = re.search(key,s)
                if span:
                    start = span.start()
                    sent = sentences[i][start:]
                
                    pattern_darad = r'خرید | گرفت | دارد | داشت'
                    if re.search(pattern_darad, sent):
                        return {'دارد' : 'تخفیف'}
                
                    pattern_nadarad = r'نداشت | ندارد | نداشت'
                    if re.search(pattern_nadarad, sent):
                        return {'ندارد' : 'تخفیف'}
                    break
            if span:
                break
        return {}
    def performance_extract(self,sentences, phrases):
        """ Output : one of two classes ['بد', 'خوب'] """

        for i,s in enumerate(sentences):
            for key in phrases:
                span = re.search(key,s)
                if span:
                    start = span.start()
                    sent = sentences[i][start:]
                
                    pattern_khob = r'میکند | می کند | دارد | داره | بالای* | خوبی? | عالی | طولانی | زیادی? | مناسبی?'
                    if re.search(pattern_khob, sent):
                        return {'خوب' : 'کارکرد'}
                
                    pattern_bad = r'نمیکند | نمی کند | ندارد | پایینی? | بدی? | افتضاحی? | کمی? '
                    if re.search(pattern_bad, sent):
                        return {'بد' : 'کارکرد'}
                    break
            if span:
                break
        return {}
    def material_extract(self,sentences, phrases_attr):
        """ Output : one of many classes of materials_attr.txt """

        for s in sentences:
            for key in phrases_attr:
                span = re.search(key,s)
                if span:
                    return {f'{key}' : 'جنس'}
            if span:
                break
        return {}
    def cover_extract(self,sentences, phrases_attr):
        """ Output : one of many classes of covers_attr.txt """

        for s in sentences:
            for key in phrases_attr:
                span = re.search(key,s)
                if span:
                    return {f'{key}' : 'نوع جلد'}
            if span:
                break
        return {}
    def format_extract(self,sentences, phrases_attr):
        """ Output : one of many classes of formats_attr.txt """

        for s in sentences:
            for key in phrases_attr:
                span = re.search(key,s)
                if span:
                    return {f'{key}' : 'قطع'}
            if span:
                break
        return {}
    def run(self,text):
        tagger = POSTagger(model='postagger.model')
        costs_phrases = list(phrase.strip() for phrase in codecs.open('costs.txt', encoding='utf-8', mode='rU').readlines())
        discounts_phrases = list(phrase.strip() for phrase in codecs.open('discounts.txt', encoding='utf-8', mode='rU').readlines())
        performance_phrases = list(phrase.strip() for phrase in codecs.open('performance.txt', encoding='utf-8', mode='rU').readlines())
        materials_attr = list(phrase.strip() for phrase in codecs.open('materials_attr.txt', encoding='utf-8', mode='rU').readlines())
        covers_attr = list(phrase.strip() for phrase in codecs.open('covers_attr.txt', encoding='utf-8', mode='rU').readlines())
        formats_attr = list(phrase.strip() for phrase in codecs.open('formats_attr.txt', encoding='utf-8', mode='rU').readlines())
        sentences = sent_tokenize(text)
        properties={}
        cost = self.cost_extract(sentences, costs_phrases) 
        discount = self.discount_extract(sentences, discounts_phrases)
        performance = self.performance_extract(sentences, performance_phrases)
        material = self.material_extract(sentences, materials_attr)
        cover = self.cover_extract(sentences, covers_attr)
        mformat = self.format_extract(sentences, formats_attr)
        properties.update(discount)
        properties.update(cost)
        properties.update(performance)
        properties.update(material)
        properties.update(cover)
        properties.update(mformat)
        return properties
