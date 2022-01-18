from bs4 import BeautifulSoup
from requests_html import HTMLSession

def find_element(doc, parent, text_typ, element, selector, typ):
    liste = ""
    span = doc.find(text_typ, string=element)
    if span != None:
        results = span.find_parents(parent)
        for rs in results:
            if selector == '':
                elems = rs.find(typ)
            else:
                elems = rs.find(typ, class_=selector)
            liste += str(elems.text.strip())
    return liste

def find_ice_if_rc(doc, parent, title, tp, classe):
    liste = ""
    try:
        link = doc.find('a', attrs={"title": title})
        results = link.find_parents(parent)
        for rs in results:
            if classe == '':
                elems = rs.find(tp)
            else:
                elems = rs.find(tp, class_=classe)

            liste += str(elems.text.strip())
        return liste

    except:
        print("Impossible d'accéder de trouver :" + str(title))
        return None

def isNone(elem):
    if elem == None :
        elem = ""
        return elem
    else:
        return elem

def mon_lien(valeur):
    s = HTMLSession()
    url = f'https://maroc.welipro.com/recherche?q={valeur}&type=&rs=&cp=1&cp_max=2035272260000&et=&v='
    try:
        resultat = s.get(url)
        document = BeautifulSoup(resultat.text, "lxml")
        return document
    except:
        print("Impossible d'accéder au lien :" + str(url))
        return 0


def trouver_le_lien(valeur):
    liens = []
    dom = mon_lien(valeur)
    titles = dom.find_all("h3", {"class": "card-title"})
    if titles != None:
        for title in titles:
            lien = title.find("a")['href']
            liens.append(lien)
        return liens
    else:
        return None


def visitez_le_lien(valeur):
    resultat = []
    liens = []
    try:
        liens = trouver_le_lien(valeur)
        for lien in liens:
            x = HTMLSession()
            res = x.get(lien)
            res = BeautifulSoup(res.text, "lxml")
            resultat.append(res)
        return resultat
    except:
        print("Impossible d'accéder au lien :" + str(liens))
        return None


def recuperer_Societe(valeur):
    societe_list = []
    docs = visitez_le_lien(valeur)
    for doc in docs:
        if doc.text != None:
            Raison_social = doc.find("h1", {"class": "card-title"}).text
            Raison_social = isNone(Raison_social)
            try :
                Activ = doc.select_one(
                'body > div.d-flex.flex-column.flex-1.layout-boxed > div.page-content > div > div.content > div > div > div.card.mb-2 > div.card-body').text
            except:
                Activ = isNone(None)
            ICE_S = find_ice_if_rc(doc,'li', "C'est quoi l'ICE ?", 'div', 'ml-auto')
            ICE_S = isNone(ICE_S)
            IF_S = find_ice_if_rc(doc,'li', "C'est quoi l'IF ?", 'div', 'ml-auto')
            IF_S = isNone(IF_S)
            Num_RC = find_ice_if_rc(doc,'li', "C'est quoi le RC ?", 'div', 'ml-auto')
            Num_RC = isNone(Num_RC)
            try:
                Centre_RC = doc.select_one(
                'html > body > div > div:nth-of-type(2) > div > div:nth-of-type(2) > div > div > div:nth-of-type(2) > div > div:nth-of-type(1) > ul > li:nth-of-type(2) > div > a').text
            except:    
                Centre_RC = isNone(None)
            Capital = find_element(doc, 'li', "span", "Capital: ", 'ml-auto', 'div')
            Capital = isNone(Capital)
            siteweb = find_element(doc, 'li', "span", 'Site web:', 'ml-auto', 'div')
            siteweb = isNone(siteweb)
            Fj = find_ice_if_rc(doc,'li', "Types d’entreprises au Maroc selon leur statut juridique", 'div', 'ml-auto')
            Fj = isNone(Fj)
            date_crea = find_element(doc, 'li', "span", "Date de création: ", 'ml-auto', "div")
            date_crea = isNone(date_crea)
            Effectif = find_element(doc, 'li', "span", "Effectif: ", 'ml-auto', "div")
            Effectif = isNone(Effectif)
            try:
                adresse = doc.select_one(
                'html > body > div > div:nth-of-type(2) > div > div:nth-of-type(2) > div > div > div:nth-of-type(4) > div > div:nth-of-type(1) > ul > li:nth-of-type(1) > div').text
            except:
                adresse = isNone(None)
            Etat = find_element(doc, "li", 'span', "État: ", 'ml-auto', "div")
            Etat = isNone(Etat)
            Tel = find_element(doc, "li", 'span', "Téléphone:", 'ml-auto', "div")
            Tel = isNone(Tel)
            Fax = find_element(doc, "li", 'span', "Fax:", 'ml-auto', "div")
            Fax = isNone(Fax)
            Email = find_element(doc, 'li', "span", "Email:", '', "a")
        else:
            print('Pas de données disponibles')
        if Raison_social != "":
            societe = {
                'raison_social': Raison_social.strip(),
                'activite': Activ.strip(),
                'ice_s': ICE_S.strip(),
                'if_s': IF_S.strip(),
                'centre_rc': Centre_RC.strip(),
                'num_rc': Num_RC.strip(),
                'capital': Capital.strip(),
                'Forme_juridique': Fj.strip(),
                'date_creation': date_crea.strip(),
                'effectif': Effectif.strip(),
                'adresse': adresse.strip(),
                'Etat': Etat.strip(),
                'Tel': Tel.strip(),
                'Fax': Fax.strip(),
                'site_web':siteweb.strip(),
                'Emails':Email.strip()
            }
            
            societe_list.append(societe)
        else:
            print('error')
            continue
    return societe_list







	