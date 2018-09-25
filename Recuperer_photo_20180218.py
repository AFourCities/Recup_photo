import urllib.request, gzip, zlib, os, re, time
from colorama import init, Fore, Back, Style



#création fonction une fois qu'on a récupérer un lien URL du fichier que le user veut utiliser pour récupérer les images
def imagelignealigne (url, path, pathdossier, dirname):
   

   #on a passé en paramètre de la fonction le chemin d'un répertoire: on essaie de créer le répertoire qui va contenir les photos d'une des URL
   if not os.path.exists(pathdossier):
      os.makedirs(pathdossier)
   
   print (url)
   print ("to")
   print (pathdossier)

   #on teste si l'URL est valide sinon on indique que l'URL ne l'est pas
   try:
      request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip"})
   except ValueError:
      print (Back.RED + "URL incorrect")
      return
   
   #print (request)

   try:
      response = urllib.request.urlopen(request)
   except urllib.error.HTTPError:
      print (Back.RED + 'URL incorrect')
      return
   #except urllib.error.URLError:
    #  print ("Check Internet Connection")
   #return

   #on teste si l'URL à traiter est encodé en 'gzip'. Si ce n'est pas le cas on ne décompresse pas en 'gzip'
   try:
      result = gzip.decompress(response.read())
   except OSError:
      response = urllib.request.urlopen(url)
      result=response.read()

   
   #print(result)

   #on crée un fichier qui s'appelle titi2.txt dans le répertoire où se trouve le fichier texte dans lequel se trouve les URL à traiter
   #et on y copie le contenu html de l'URL. Puis on le ferme
   savedfile= open(path + "\\" + "titi2.txt", "w")
   savedfile.write(str(result))
   savedfile.close()

   #on rouvre le fichier et on attribue une variable à son contenu
   result = open(path + "\\" + "titi2.txt", "r").read()

   #on attribue une variable à la longueur du contenu html de l'URL
   longueur=len(result)
   #print (longueur)

   fullresult=""
   #fullresult=[]

   findw=0
   findjpeg=0

   #on définie une fonction qui a pour but d'enlever les URL de photos en double présent dans le html
   def remove_duplicates(fullresult):
      output=[]
      seen=set()
      for value in fullresult:
         if value not in seen:
            output.append(value)
            seen.add(value)
      return output

   #dans tout le contenu du fichier html, on cherche la partie qui commence par window.__VOG__ car on ne veut pas    
   #prendre en compte ce qui est après cette balise et on met à jour la longueur du fichier result
   for k in range (0, longueur):
      patternend = r"^window.__VOG__"
      testresultend=result[k:k+14]
      if re.match(patternend, testresultend):
         longueur=k
         #print(patternend)
         #print(testresultend)
         #print(k)
      #print (testresultstart)

   #dans tout le contenu du fichier html (réduit, donc avant "window.__VOG__" , on cherche les parties qui
   #commencent par "http://assets" et finissent par .jpg
   for i in range (0, longueur):
      patternstart = r"^https://assets"
      testresultstart=result[i:i+14]
      #print (testresultstart)
   
      if re.match(patternstart, testresultstart):
         #print(i)
         #print (testresultstart)
         #print (result[i+9:longueur])
         #on cherche en abaissant la case car il y a des URL photos qui ont '.JPG' au lieu de '.jpg'
         newresult=(result[i:longueur]).lower()
         #print(newresult)

         patternend=newresult.find("jpg")
         #print(patternend)

         #findw=result[i+10:i+10+patternend].find("w_")
         findjpeg=result[i:i+patternend].find("jpeg")
         #print(findw)
         #print(findjpeg)

         
         #on en prend que les résultats qui n'ont pas "jpeg" dedans
         #if findw<0:
         if findjpeg<0:
              fullresult=fullresult+result[i:i+patternend]+"jpg\n"
         #print(fullresult)

   #print(fullresult)

   #noduplicateresult = remove_duplicates(fullresult)
   #print(noduplicateresult)

   #on supprime le fichier titi2.txt et on crée le titi3.txt pour qui écrire lignes par lignes les URL photos trouvés à l'étape précédente   
   os.remove(path + "\\" +  "titi2.txt")
   savedfile2 = open(path + "\\" + "titi3.txt", "w")
   savedfile2.write(fullresult)
   savedfile2.close()

   #on rouvre le fichier titi3.txt pour prendre lignes à lignes les URL photos et récupérer les photos
   savedfile3 = open(path + "\\" + "titi3.txt", "r")
   array_cont=savedfile3.read().splitlines()
   array_cont=list(set(array_cont))
   #print (array_cont)
   for i in range(len(array_cont)):
      total_url=array_cont[i]
      if total_url != 'jpg':
         #print(total_url)
         #print(total_url[68:81])
         addressimage = urllib.request.urlopen(total_url)
         #print(total_url[0:69])
         #print(pathdossier + "\\" + total_url[68:81] + ".jpg")
         if dirname == "":
            #on cherche le dernier slash dans l'URL pour pouvoir récupérer la 1° position du nom du .jpg
            array_to_find_last_before_jpg = [n for n in range(len(total_url)) if total_url.find('/', n) == n]
            last_slash_position = max(array_to_find_last_before_jpg)+1
            #print (last_slash_position)
            #on cherche la position du 'g' du .jpg dans l'URL
            array_to_find_jpg = [n for n in range(len(total_url)) if total_url.find('.jpg', n) == n]
            last_jpg_position = max(array_to_find_jpg)+4
            #print (last_jpg_position)

            #on ouvre le répertoire et on crée le fichier dans le répertoire qui convient avec le nom qu'il faut
            #en utilisant le libéllé de l'image avant le .jpg
            #output = open(pathdossier + "\\" + total_url[68:81] + ".jpg","wb")
            output = open(pathdossier + "\\" + total_url[last_slash_position:last_jpg_position],"wb")
            #print(output)
         else:
            output = open(pathdossier + "\\" + dirname + "(" + str(i+1) + ")" + ".jpg","wb")
            #print(output)
         output.write(addressimage.read())
         output.close()
         print(str(i+1) + "/" + str(len(array_cont)))

   savedfile3.close()
   os.remove(path + "\\" + "titi3.txt")

   print ("Fini")

init(convert=True, autoreset=True)   
#on demande au user de rentrer le chemin du fichier dans lequel il a mis tous les URL pour lesquels il faut récupérer les photos
print("Lien du fichier sur votre ordinateur. Une ligne par URL et chaque URL peut être suivi de ; + Nom répertoire sans espace après (optionel)")
pathbeforetransformation=input()
path2=pathbeforetransformation
pathbeforetransformation=pathbeforetransformation+'\\'
path=pathbeforetransformation[2:].replace("\\", "/")

#on essaie d'ouvrir le fichier du chemin donnée par le user
try:
   file=open(path2, "r")
   array_cont=file.read().splitlines()
   for i in range(len(array_cont)):
      findurl=array_cont[i].find(";")
      #print(findurl)
      #print (len(array_cont[i][findurl+1:]))
      #on cherche à voir si le user a indiqué un nom de répertoire à créer
      #après un ; Sinon on en créée un avec un horodatage
      if findurl < 0 or len(array_cont[i][findurl+1:])==0:
         url=array_cont[i]
         url=url.replace(";", "")
         cwd=os.path.dirname(path2)
         pathdossier=cwd+"\Dossier"+str(i)+'_'+str((time.localtime().tm_year))+str((time.localtime().tm_mon))+str((time.localtime().tm_mday))+str((time.localtime().tm_hour))+str((time.localtime().tm_min))+str((time.localtime().tm_sec))
         dirname=""
      else:
         url=array_cont[i][:findurl]
         #print (url)
         cwd=os.path.dirname(path2)
         dirname=array_cont[i][findurl+1:]
         print(path2)
         #on enlève les blancs après le nom du dossier au cas
         #où le user en a mis
         dirname=dirname.rstrip()
         #print(dirname)
         #dirname=dirname.replace(" ", "")
         cwd=cwd+"\ "
         cwd=cwd.replace(" ", "")
         cwd=cwd+array_cont[i][findurl+1:]
         #on enlève les blancs après le nom du dossier au cas
         #où le user en a mis
         cwd=cwd.rstrip()
         #cwd=cwd.replace(" ", "")
         pathdossier=cwd
         #pathdossier=cwd+"\Dossier"+str(i)+'_'+str((time.localtime().tm_year))+str((time.localtime().tm_mon))+str((time.localtime().tm_mday))+str((time.localtime().tm_hour))+str((time.localtime().tm_min))+str((time.localtime().tm_sec))
         #print (dirname)
         #print (range(len(array_cont)))
      if i == max(range(len(array_cont))):
         file.close()
         imagelignealigne(url, cwd, pathdossier, dirname)
      else:
         imagelignealigne(url, cwd, pathdossier, dirname)
except OSError:
   print("Something wrong in your path or in your file. Check spelling or special characters")
except FileNotFoundError:
   print("Not a valid path")
   get_user_choice() 
   






           
