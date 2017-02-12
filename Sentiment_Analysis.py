from collections import defaultdict, Counter
from random import shuffle
from tkinter import Tk
from tkinter import ttk
from tkinter import messagebox


def fail_segamini(fail):  # Ajame algses failis olevad tweedid segamini
    f = open(fail, encoding="UTF-8")
    read = []
    for rida in f:
        read.append(rida)
    shuffle(read)
    g = open("tweedid_segamini.txt", "w", encoding="UTF8")
    for i in read:
        g.write(i)
    f.close()
    return  # Saime faili nimega "tweedid_segamini"


def tweedid_sonastikku(fail):  # Paneme kõik tweedid kolme erinevasse sõnastikku, mille võtmeteks "positive", "negative", "neutral", "irrelevant"
    f = open(fail, encoding="UTF-8")
    treenimissonastik = defaultdict(list)
    devsonastik = defaultdict(list)
    testsonastik = defaultdict(list)
    i = 0
    for rida in f:
        i += 1
        rida = rida.strip()
        lahku = rida.split('","')  # Listis on teisel kohal meeleolu ja viimasel kohal tweet ise (lõpus on jutumärk)
        if i <= 4500:
            treenimissonastik[lahku[1]].append(lahku[-1].split(" ")[:-1])  # Testsõnastikku lähevad esimesed 4500 tweeti
        if 4500 < i < 4901:
            devsonastik[lahku[1]].append(lahku[-1].split(" ")[:-1])  # Silumissõnastikku lähevad järgmised 400 tweeti
        if i > 4900:
            testsonastik[lahku[1]].append(lahku[-1].split(" ")[:-1])  # Testimissõnastikku lähevad ülejäänud 212 tweeti
    f.close()
    return treenimissonastik, devsonastik, testsonastik


def ngrammid(meeleolu_sonestatud):  # Teeme iga tweedi kohta n-grammid
    grammid = []
    yksgrammid = []
    kaksgrammid = []
    kolmgrammid = []
    neligrammid = []
    for a in range(len(meeleolu_sonestatud)):
        for i in range(len(meeleolu_sonestatud[a])):  # Teeme üksgrammid
            yksgrammid.append((meeleolu_sonestatud[a][i]))
        for i in range(len(meeleolu_sonestatud[a]) - 1):  # Teeme kaksgrammid
            kaksgrammid.append((meeleolu_sonestatud[a][i], meeleolu_sonestatud[a][i + 1]))
        for i in range(len(meeleolu_sonestatud[a]) - 2):  # Teeme kolmgrammid
            kolmgrammid.append((meeleolu_sonestatud[a][i], meeleolu_sonestatud[a][i + 1], meeleolu_sonestatud[a][i + 2]))
        for i in range(len(meeleolu_sonestatud[a]) - 3):  # Teeme neligrammid
            neligrammid.append((meeleolu_sonestatud[a][i], meeleolu_sonestatud[a][i + 1], meeleolu_sonestatud[a][i + 2], meeleolu_sonestatud[a][i + 3]))
    yksgrammid = list(Counter(yksgrammid).most_common(80))  # Enimlevinud n-grammid paneme listi nimega "grammid"
    for a in range(len(yksgrammid)):
        yksgrammid[a] = list(yksgrammid[a])
        grammid.append(yksgrammid[a])
    kaksgrammid = list(Counter(kaksgrammid).most_common(80))
    for a in range(len(kaksgrammid)):
        kaksgrammid[a] = list(kaksgrammid[a])
        grammid.append(kaksgrammid[a])
    kolmgrammid = list(Counter(kolmgrammid).most_common(40))
    for a in range(len(kolmgrammid)):
        kolmgrammid[a] = list(kolmgrammid[a])
        grammid.append(kolmgrammid[a])
    neligrammid = list(Counter(neligrammid).most_common(30))
    for a in range(len(neligrammid)):
        neligrammid[a] = list(neligrammid[a])
        grammid.append(neligrammid[a])
    return grammid  # Saame listi (igal programmi käivitamisel väärtused varieeruvad, sest sama sagedusega on mitu n-grammi)


def sonastik_hulgaks(meeleolu_sagedused):  # Teeme sõnastikud hulgaks, et kiiremini leida unikaalsed parameetrid.
    hulk = set()
    for a in meeleolu_sagedused:
        hulk.add(a[0])
    return hulk


def kaalud(hulk):  # Lisame parameetrile kaalu
    kaaludega = []
    for i in hulk:
        if i == str(i):
            a = []
            a.append(i)
            a.append(1)  # Üksgrammid saavad kaalu 1, kaksgrammid kaalu 2 jne.
            kaaludega.append(a)
        elif len(i) == 2:
            a = []
            a.append(i)
            a.append(2)
            kaaludega.append(a)
        elif len(i) == 3:
            a = []
            a.append(i)
            a.append(3)
            kaaludega.append(a)
        elif len(i) == 4:
            a = []
            a.append(i)
            a.append(4)
            kaaludega.append(a)
    return kaaludega


def yks_ngrammiks(tweet):  # Teeme ühe tweedi n-grammideks, et saaksime parameetritega võrrelda
    yksgrammid = []
    kaksgrammid = []
    kolmgrammid = []
    neligrammid = []
    for i in range(len(tweet)):
        yksgrammid.append((tweet[i]))
    for i in range(len(tweet) - 1):
        kaksgrammid.append((tweet[i], tweet[i + 1]))
    for i in range(len(tweet) - 2):
        kolmgrammid.append((tweet[i], tweet[i + 1], tweet[i + 2]))
    for i in range(len(tweet) - 3):
        neligrammid.append((tweet[i], tweet[i + 1], tweet[i + 2], tweet[i + 3]))
    return yksgrammid, kaksgrammid, kolmgrammid, neligrammid


def kaalude_summa(tweet_grammidena, kaal):  # Määrame ühe tweedi väärtuse
    summa = 0
    for a in tweet_grammidena:
        for d in a:
            for b in kaal:
                if d in b:
                    summa += b[1]  # Liidame kokku tweedis olemasolevad parameetrite kaalud
    return summa


def tweetide_vaartused(tweet_grammidena, parameetrid):  # Teeme kaalude summadest listi.
    vaartused = []
    vaartused.append(kaalude_summa(tweet_grammidena, parameetrid["positive"]))
    vaartused.append(kaalude_summa(tweet_grammidena, parameetrid["negative"]))
    vaartused.append(kaalude_summa(tweet_grammidena, parameetrid["neutral"]))
    vaartused.append(kaalude_summa(tweet_grammidena, parameetrid["irrelevant"]))
    return suurim_kaal(vaartused)


def suurim_kaal(vaartused):  # Vaatame, milline summa oli kõige suurem. Selle järgi saame meelsuse
    meeleolud = ["positive", "negative", "neutral", "irrelevant"]
    maksimum = max(vaartused)
    meeleolu = meeleolud[vaartused.index(maksimum)]
    vaartused.remove(maksimum)
    if maksimum in vaartused:
        return "Cannot be determined with our parameters."
    else:
        return meeleolu


def moju_suurendamine(tweet_grammidena, parameetrid_votmega):  # Siin suurendame õigesti määranud parameetri kaalu
    for a in tweet_grammidena:
        for gramm in a:
            for ngramm in parameetrid_votmega:
                if gramm in ngramm:
                    ngramm[1] += 1
    return parameetrid_votmega


def valede_tweetide_eemaldamine(tweet_grammidena, parameetrid):  # Eemaldame sagedased valesti määranud parameetrid
    valed_ngrammid = []
    for grammide_list in tweet_grammidena:
        for n_grammid in grammide_list:
            for gramm in n_grammid:
                for voti in parameetrid:
                    for ngramm in parameetrid[voti]:
                        if gramm in ngramm:
                            valed_ngrammid.append(gramm)
                            break
    enim_levinud = list(Counter(valed_ngrammid).most_common(3))
    for gramm in enim_levinud:
        for voti in parameetrid:
            for ngramm in parameetrid[voti]:
                if gramm[0] in ngramm:
                    parameetrid[voti].remove(ngramm)
    return parameetrid


def silumine(sonestatud_dev, parameetrid, votmeks):  # Silume parameetreid
    valed_tweedid = []
    for i in range(len(sonestatud_dev)):
        tweet_grammidena = yks_ngrammiks(sonestatud_dev[i])
        meeleolu = tweetide_vaartused(tweet_grammidena, parameetrid)
        if meeleolu == votmeks:  # Kui parameeter määras õigesti, siis suurendame selle kaalu
            moju_suurendamine(tweet_grammidena, parameetrid[votmeks])
        else:  # Kui aga valesti, siis paneme selle tweedi listi
            valed_tweedid.append(tweet_grammidena)
    valede_tweetide_eemaldamine(valed_tweedid, parameetrid)
    return


def testimine(meeleolu_sonestatud_test, meeleolu):  # F-score'i arvutamiseks loendame õigesti ja valesti määratud tweedid
    oigesti = 0
    valesti = 0
    for i in range(len(meeleolu_sonestatud_test)):
        tweet_grammidena = yks_ngrammiks(meeleolu_sonestatud_test[i])
        tweedi_meeleolu = tweetide_vaartused(tweet_grammidena, parameetrid)
        if tweedi_meeleolu == meeleolu:
            oigesti += 1
        else:
            valesti += 1
    return oigesti, valesti


def arvutamine(oiged, koik, valed):  # Arvutame f-score'i ehk programmi töö täpsuse
    precision = oiged/koik
    recall = oiged/(oiged + valed)
    tulemus = (2*((precision*recall)/(precision+recall)))*100
    return round(tulemus, 2)


treenimissonastik = tweedid_sonastikku("tweedid_segamini.txt")[0]  # Teeme treenimissõnastiku
devsonastik = tweedid_sonastikku("tweedid_segamini.txt")[1]  # Teeme silumissõnastiku
testsonastik = tweedid_sonastikku("tweedid_segamini.txt")[2]  # Teeme testsõnastiku
for voti in tweedid_sonastikku("tweedid_segamini.txt")[0]:
    treenimissonastik[voti] = ngrammid(treenimissonastik[voti])


def ngrammiga_hulgad():
    postiivsed_hulk = sonastik_hulgaks(treenimissonastik["positive"])
    negatiivsed_hulk = sonastik_hulgaks(treenimissonastik["negative"])
    neutraalsed_hulk = sonastik_hulgaks(treenimissonastik["neutral"])
    irrelevant_hulk = sonastik_hulgaks(treenimissonastik["irrelevant"])
    return postiivsed_hulk, negatiivsed_hulk, neutraalsed_hulk, irrelevant_hulk


def unikaalsed_parameetrid():
    positiivsed = ((ngrammiga_hulgad()[0] - ngrammiga_hulgad()[1]) - ngrammiga_hulgad()[2]) - ngrammiga_hulgad()[3]
    negatiivsed = ((ngrammiga_hulgad()[1] - ngrammiga_hulgad()[0]) - ngrammiga_hulgad()[2]) - ngrammiga_hulgad()[3]
    neutraalsed = ((ngrammiga_hulgad()[2] - ngrammiga_hulgad()[1]) - ngrammiga_hulgad()[0]) - ngrammiga_hulgad()[3]
    irrelevant = ((ngrammiga_hulgad()[3] - ngrammiga_hulgad()[1]) - ngrammiga_hulgad()[0]) - ngrammiga_hulgad()[2]
    return positiivsed, negatiivsed, neutraalsed, irrelevant


parameetrid = defaultdict(list)
parameetrid["positive"] = kaalud(unikaalsed_parameetrid()[0])
parameetrid["negative"] = kaalud(unikaalsed_parameetrid()[1])
parameetrid["neutral"] = kaalud(unikaalsed_parameetrid()[2])
parameetrid["irrelevant"] = kaalud(unikaalsed_parameetrid()[3])


def meeleolu_oiged(testsonastik, meeleolu):
    meeleolu_oiged = testimine(testsonastik[meeleolu], meeleolu)[0]
    return meeleolu_oiged


def meeleolu_koik(testsonastik, meeleolu):
    meeleolu_koik = testimine(testsonastik["positive"], meeleolu)[0] \
                    + testimine(testsonastik["negative"], meeleolu)[0] \
                    + testimine(testsonastik["neutral"], meeleolu)[0] \
                    + testimine(testsonastik["irrelevant"], meeleolu)[0]
    return meeleolu_koik


def meeleolu_valed(testsonastik, meeleolu):
    meeleolu_valed = testimine(testsonastik[meeleolu], meeleolu) [1]
    return meeleolu_valed


for el in range(3):  # Silume parameetreid silumissõnastikuga
    silumine(devsonastik["positive"], parameetrid, "positive")
    silumine(devsonastik["negative"], parameetrid, "negative")
    silumine(devsonastik["neutral"], parameetrid, "neutral")
    silumine(devsonastik["irrelevant"], parameetrid, "irrelevant")

# Arvutame f-score'i
print("Programm arvutab positiivseid tweete", arvutamine(meeleolu_oiged(testsonastik, "positive"),
                                                         meeleolu_koik(testsonastik, "positive"),
                                                         meeleolu_valed(testsonastik, "positive")), "protsendilise täpsusega.")
print("Programm arvutab negatiivseid tweete", arvutamine(meeleolu_oiged(testsonastik, "negative"),
                                                         meeleolu_koik(testsonastik, "negative"),
                                                         meeleolu_valed(testsonastik, "negative")), "protsendilise täpsusega.")
print("Programm arvutab neutraalseid tweete", arvutamine(meeleolu_oiged(testsonastik, "neutral"),
                                                         meeleolu_koik(testsonastik, "neutral"),
                                                         meeleolu_valed(testsonastik, "neutral")), "protsendilise täpsusega.")
print("Programm arvutab ebaolulisi või mitte ingliskeelseid tweete", arvutamine(meeleolu_oiged(testsonastik, "irrelevant"),
                                                                                meeleolu_koik(testsonastik, "irrelevant"),
                                                                                meeleolu_valed(testsonastik, "irrelevant")), "protsendilise täpsusega.")
test = []  # Teeme kaks listi, et konstruktsioon oleks sarnane algsele
laused = []


def jah():
    label.config(text="Would you like to enter more text?")
    if lause.get() != "":
        test.append(lause.get())
        lause.delete(0, "end")
        return test
    else:
        label.config(text="You didn't enter anything!")
        label.place(x=180, y=30)
        return


def ei():
    if lause.get() != "":
        test.append(lause.get())
    else:
        label.config(text="You didn't enter anything!")
        label.place(x=180, y=30)
        return
    for i in test:
        laused.append(i.split(" "))  # Sõnestame tweedi, tehes sellest listi
    sentiment = "The sentiments are:" + "\n" + "\n"
    for i in range(len(laused)):
        tweet_grammidena = yks_ngrammiks(laused[i])
        meeleolu = tweetide_vaartused(tweet_grammidena, parameetrid)
        sentiment += test[i] + "\n" + " * " + meeleolu + "\n" + "\n"
    messagebox.showinfo(message=sentiment)
    frame.destroy()
    return laused


frame = Tk()
frame.title("Sentiment Analysis")  # Teeme kasutajaliidese tkinteriga
frame.geometry("500x100")
label = ttk.Label(frame, text="Enter text:")
label.place(x=11, y=5)
lause = ttk.Entry(frame)
lause.place(x=70, y=5, width=360)
label = ttk.Label(frame, text="Would you like to enter more text?")
label.place(x=160, y=30)
yesButton = ttk.Button(frame, text="Yes", command=jah)
yesButton.place(x=90, y=50, width=150)
noButton = ttk.Button(frame, text="No", command=ei)
noButton.place(x=260, y=50, width=150)
frame.mainloop()
