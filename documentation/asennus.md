# Paikalla-sovelluksen asentaminen

## Paikallinen asennus

1. Kloonaa sovellus GitHubista haluamaasi hakemistoon
```
~$ git clone git@github.com:artoh/paikalla.git
```

1. Luo sovellukselle Pythonin virtuaaliympäristö
```
~$ cd paikalla
~/paikalla$ python3 -m venv venv
```

1. Asenna sovelluksen vaatimat riippuvuudet
```
~/paikalla$ pip install -r requirements.txt
```

1. Ohjelma on valmis käynnistettäväksi!
```
~/paikalla$ source venv/bin/activate
(venv) ~/paikalla$ python run.py
```

1. Ensimmäisellä käynnistyskerralla sovellus opastaa sinua luomaan jäsenrekisterin hoitajan käyttäjätunnuksen

![Kuvaruutukaappaus käyttäjätunnuksen luomisesta](pic/aloita.png)

Tässä on kuvattu ohje sovelluksen asentamisesta kehitysympäristöön SQLite-tietokannalla. Ohjeita tuontantokäyttöön asentamisesta omalle Apache- tai nginx-palvelimella löytyy [Flaskin dokumentaatiosta](http://flask.palletsprojects.com/en/1.1.x/deploying/)

## Asentaminen Herokuun

Sovelluksena on valmiina Herokun vaatimat riippuvuudet.

Jatkaa edellä olevista paikalliseen käyttöön asentamisen ohjeista.

5. Luo sovellus Herokuun ja lisää versionhallintaan Heroku-yhteys
```
~/paikalla$ heroku create sovelluksen_nimi_Herokussa
~/paikalla$ git remote add heroku https://git.heroku.com/sovelluksen_nimi_Herokussa
```

6. Lisää Herokun tarvitsemat määritteet aikavyöhykkeestä, paikallistamisesta sekä PostgreSQL-tietokannasta
```
~/paikalla$ heroku config:set PRODUCTION=1
~/paikalla$ heroku config:set TZ="Europe/Helsinki"
~/paikalla$ heroku pq:psql
~/paikalla$ heroku addons:add heroku-postgresql:hobby-dev
~/paikalla$ heroku buildpacks:add https://github.com/heroku/heroku-buildpack-locale
```

7. Lähetä sovellus Herokuun
```
~/paikalla$ git push heroku master
```

8. Ensimmäisellä käynnistyskerralla sovellus opastaa sinua luomaan jäsenrekisterin hoitajan käyttäjätunnuksen.
