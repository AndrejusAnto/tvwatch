Python'o script'as, kuris jama serialų info iš IMDB ir pateikia sąrašą serialų ir jų epizodus, kurie bus rodomi nuo dabartinė datos. Kol kas reikia atsidaryti failą ir savo serialus sudėti į watchseries list'ą. Priklausomai nuo serialų kiekio, gali užtrukti, nes duomenų paėmimas iš imdb lėtokas.

Linux: naudojimui geriausia naudoti Anaconda (https://www.anaconda.com/distribution/). Jei nenorit daug nereikalingų package'ų, naudokit miniconda (https://docs.conda.io/en/latest/miniconda.html) ir tada naudojant conda env bus suinstaliuota minimalus package'ų kiekis.

Kai jau turit conda:

conda create -n (jūsų env pavadinimas) python=3.8

conda activate (jūsų env pavadinimas)

ir tada:
pip install IMDbPY
* pip install, nes nors conda ir turi daug package'ų, bet neturi normalios IMDbPY versijos, todėl reikia instaliuot per pip

Kol kas reikia faile series.py į watchseries list'ą sudėti savo serialų pavadinimus. Galiausiai per terminalą: python series.py. Bus sukurtas json failas, kur bus išsaugomi duomenys ir tada informacija bus atprint'a terminale.
