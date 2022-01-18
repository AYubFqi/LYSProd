from ICEPeek.settings import BASE_DIR
from .models import Param_Societe
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import re
import time
import datetime
from .BSSc import recuperer_Societe
def isnull(champs, valeur_sinull):
    if champs is None:
        return valeur_sinull
    elif champs == "":
        return valeur_sinull
    else:
        return champs
        
@api_view(['POST'])
# @permission_classes((permissions.IsAuthenticated,))
def enregistrer_paramSociete(request, pk=''):   
    t1 = datetime.datetime.now()
    nb=0
    nb_ice =0
    nb_if = 0
    nb_error =0
    nb_db = 0
    retour ={} 
    pattern_ice = re.compile("^\d?\d{3,16}$")
    pattern_if = re.compile("^\d?\d{3,8}$")
    ident = 0
    for lig in request.data["liste"] :

            nb+=1
            if bool(pattern_ice.match(lig["ice"])):
                ident = int(float(lig["ice"]))
                if ident == 0 or len(str(ident))<4:
                    nb_error+=1
                    retour["ice_" + str(ident)] = {"result":"Erreur format ICE", "rs" : "None", "ice" : "None", "if" : "None", "centre_rc": "None", "rc" : "None", "adresse" : "None", "activite" : "None"}  
                    continue
                time.sleep(1)
                societes = recuperer_Societe(ident)
                for societe in societes :
                    try:              
                        data_societe = Param_Societe.objects.get(raison_social=societe.raison_social)
                        if data_societe != None:
                            nb_db+=1
                            retour["ice_" + str(ident)] = {"result":"Résultat direct","raison_social" : data_societe.raison_social, "ice_s" : data_societe.ice_s, "if_s" : data_societe.if_s, "centre_rc": data_societe.centre_rc, "num_rc" : data_societe.num_rc, "adresse" : data_societe.adresse, "activite" : data_societe.activite
                            , "capital" : data_societe.capital, "Forme_juridique" : data_societe.Forme_juridique, "date_creation" : data_societe.date_creation, "effectif" : data_societe.effectif, "Etat" : data_societe.Etat, "Tel" : data_societe.Tel
                            , "Fax" : data_societe.Fax,"Emails" : data_societe.Emails, "site_web" : data_societe.site_web}
                            continue

                    except :
                        if societe != None:
                            if  societe["ice_s"] == str(ident) and  societe["if_s"] != '-':
                                retour["ice_" + str(ident)] = {"result":"Réponse DGI","raison_social" : societe["raison_social"], "ice_s" : societe["ice_s"], "if_s" : societe["if_s"], "centre_rc": societe["centre_rc"], "num_rc" : societe["num_rc"], "adresse" : societe["adresse"], "activite" : societe["activite"]
                                , "capital" : societe["capital"], "Forme_juridique" : societe["Forme_juridique"], "date_creation" : societe["date_creation"], "effectif" : societe["effectif"], "Etat" : societe["Etat"]
                                , "Tel" : societe["Tel"], "Fax" : societe["Fax"],"Emails" :societe["Emails"], "site_web" : societe["site_web"]}
                            soc = Param_Societe(raison_social=societe["raison_social"], activite= societe["activite"], ice_s=societe["ice_s"],  if_s= societe["if_s"], centre_rc=societe["centre_rc"], num_rc=societe["num_rc"], adresse=societe["adresse"],
                            capital=societe["capital"],Forme_juridique=societe["Forme_juridique"],date_creation=societe["date_creation"],effectif=societe["effectif"],Etat=societe["Etat"],
                            Tel=societe["Tel"],Fax=societe["Fax"],Emails=societe["Emails"], site_web=societe["site_web"])
                            soc.save()
                            nb_ice+=1
                            continue   
                        else:
                            nb_error+=1
                            retour["ice_" + str(ident)] = {"result":"Aucun retour de la DGI","rs" : "None", "ice" : "None", "if" : "None", "centre_rc": "None", "rc" : "None", "adresse" : "None", "activite" : "None"}  
                            continue  
            if bool(pattern_if.match(lig["if"])):
                ident = int(float(lig["if"]))
                if ident == 0 or len(str(ident))<4:
                    nb_error+=1
                    retour["if_" + str(ident)] = {"result":"Erreur format IF","rs" : "None", "ice" : "None", "if" : "None", "centre_rc": "None", "rc" : "None", "adresse" : "None", "activite" : "None"}  
                    continue 
                time.sleep(1)
                societes = recuperer_Societe(ident)
                for societe in societes :
                    try:
                        data_societe = Param_Societe.objects.get(raison_social=societe.raison_social)
                        if data_societe != None and data_societe.ice_s != '-' and  data_societe.if_s != '-':
                            nb_db+=1
                            retour["if_" + str(ident)] = {"result":"Résultat direct","raison_social" : data_societe.raison_social, "ice_s" : data_societe.ice_s, "if_s" : data_societe.if_s, "centre_rc": data_societe.centre_rc, "num_rc" : data_societe.num_rc, "adresse" : data_societe.adresse, "activite" : data_societe.activite
                            , "capital" : data_societe.capital, "Forme_juridique" : data_societe.Forme_juridique, "date_creation" : data_societe.date_creation, "effectif" : data_societe.effectif, "Etat" : data_societe.Etat, "Tel" : data_societe.Tel
                            , "Fax" : data_societe.Fax, "Emails" : data_societe.Emails, "site_web" : data_societe.site_web}
                            continue
                        
                    except:
                        if societe != None:
                            if  societe["ice_s"] != '-' and  societe["if_s"] == str(ident):
                                retour["if_" + str(ident)] = {"result":"Réponse DGI","rs" : societe["raison_social"], "if_s" : societe["if_s"], "ice_s" : societe["ice_s"], "centre_rc": societe["centre_rc"], "num_rc" : societe["num_rc"], "adresse" : societe["adresse"], "activite" : societe["activite"]
                                , "capital" : societe["capital"], "Forme_juridique" : societe["Forme_juridique"], "date_creation" : societe["date_creation"], "effectif" : societe["effectif"], "Etat" : societe["Etat"]
                                , "Tel" : societe["Tel"], "Fax" : societe["Fax"],"Emails" : societe["Emails"], "site_web" : societe["site_web"]}
                            soc = Param_Societe(raison_social=societe["raison_social"], activite= societe["activite"], if_s=societe["if_s"],  ice_s= societe["ice_s"], centre_rc=societe["centre_rc"], num_rc=societe["num_rc"], adresse=societe["adresse"],
                            capital=societe["capital"],Forme_juridique=societe["Forme_juridique"],date_creation=societe["date_creation"],effectif=societe["effectif"],Etat=societe["Etat"],
                            Tel=societe["Tel"],Fax=societe["Fax"],Emails=societe["Emails"], site_web=societe["site_web"])
                            soc.save()
                            nb_if+=1
                            continue                             
                        else:
                            nb_error+=1
                            retour["if_" + str(ident)] = {"result":"Aucun retour de la DGI","rs" : "None", "ice" : "None", "if" : "None", "centre_rc": "None", "rc" : "None", "adresse" : "None", "activite" : "None"}  
                            continue                
            else:
                    nb_error+=1
                    retour["ice_" + str(ident)] = {"result":"Aucun retour de la DGI ICE et IF","rs" : "None", "ice" : "None", "if" : "None", "centre_rc": "None", "rc" : "None", "adresse" : "None", "activite" : "None"}  
                    continue 
                             
    
    t2 = datetime.datetime.now()
    retour["duree"]=(t2-t1).total_seconds()
    retour["nb"]=nb
    retour["nb_db"]=nb_db
    retour["nb_ice"]=nb_ice
    retour["nb_if"]=nb_if
    retour["nb_error"]=nb_error
    print(retour)
    return Response({"data" : retour}, status=status.HTTP_201_CREATED)


