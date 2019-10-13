# Käyttötapaukset tietokantakyselyineen

<!-- TOC depthFrom:2 depthTo:3 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Sisäänkirjautuminen ja käyttöoikeuksien tarkastus](#sisäänkirjautuminen-ja-käyttöoikeuksien-tarkastus)
	- [Sisäänkirjautuminen](#sisäänkirjautuminen)
- [Käyttäjähallinta](#käyttäjähallinta)
	- [Käyttäjän lisääminen](#käyttäjän-lisääminen)
	- [Huoltajan tai huollettavan liittäminen](#huoltajan-tai-huollettavan-liittäminen)
	- [Henkilötietojen katsominen](#henkilötietojen-katsominen)
	- [Henkilötietojen muokkaaminen](#henkilötietojen-muokkaaminen)
	- [Salasanan vaihtaminen](#salasanan-vaihtaminen)
- [Ilmoittautumiset](#ilmoittautumiset)
	- [Ilmoittautumisten selaaminen](#ilmoittautumisten-selaaminen)
	- [Uusi ilmoittautuminen](#uusi-ilmoittautuminen)
	- [Ilmoittautumisten poistaminen](#ilmoittautumisten-poistaminen)
- [Kalenteri](#kalenteri)
- [Ryhmien hallinta](#ryhmien-hallinta)
	- [Ryhmän lisääminen](#ryhmän-lisääminen)
	- [Ryhmän poistaminen](#ryhmän-poistaminen)
	- [Ryhmän tietojen muokkaaminen](#ryhmän-tietojen-muokkaaminen)
- [Kokousten hallinta](#kokousten-hallinta)
	- [Kokousten lisääminen](#kokousten-lisääminen)
	- [Kokousten muokkaaminen](#kokousten-muokkaaminen)
	- [Kokouksen poistaminen](#kokouksen-poistaminen)
	- [Läsnäolleiden merkitseminen](#läsnäolleiden-merkitseminen)
- [Tilastot](#tilastot)

<!-- /TOC -->

## Sisäänkirjautuminen ja käyttöoikeuksien tarkastus

### Sisäänkirjautuminen

Sisään kirjauduttaessa haetaan henkilön tiedot. Näihin liittyviä huoltajuus- ja ryhmätietoja haetaan silloin, kun tarkastellaan onko henkilöllä oikeus käsitellä tietoja huoltajana tai ryhmän ohjaajana.

#### Kyselyt

```sql
# Henkilötiedot
SELECT henkilo.id, henkilo.etunimi, henkilo.sukunimi, henkilo.puhelin,
	henkilo.email, henkilo.salasana, henkilo.syntymaaika, henkilo.toimihenkilo,
  henkilo.varotieto, henkilo.jasenyysalkoi, henkilo.jasenyyspaattyi
FROM henkilo
WHERE henkilo.email = ?

#Huoltajan autorisaatio
SELECT henkilo.id  
FROM henkilo, huoltajuus
WHERE ? = huoltajuus.huollettava AND henkilo.id = huoltajuus.huoltaja

#Ryhmänohjaajan autorisaatio
SELECT id FROM ryhmassa WHERE ryhmaid=:ryhmaid AND henkiloid=:henkiloid AND ohjaaja

```
## Käyttäjähallinta

### Käyttäjän lisääminen

#### Roolit

- [x] Aikuinen luo tunnuksen itselleen jäsenenä
- [x] Aikuinen luo itselleen tunnuksen huoltajana
- [x] Huoltaja ilmoittaa lapsensa jäseneksi
- [x] Toimihenkilö lisää jäsenen
- [x] Toimihenkilö lisää huoltajan, joka ei ole jäsen

#### Kysely

```sql
INSERT INTO henkilo (etunimi, sukunimi, puhelin, email, salasana, syntymaaika, toimihenkilo,
    varotieto, jasenyysalkoi, jasenyyspaattyi)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
```

Jos vanhempi lisää lapsensa, suoritetaan välittömästi myös huoltajuuden liittäminen (katso seuraava)

### Huoltajan tai huollettavan liittäminen

#### Roolit

- [x] Huoltaja liittää lapselleen toisen huoltajan
- [x] Toimihenkilö yhdistää lapselle huoltajan
- [x] Toimihenkilö poistaa lapselta huoltajan

#### Kysely

```sql
INSERT INTO huoltajuus (huoltaja, huollettava) VALUES (?, ?)
```

### Henkilötietojen katsominen

#### Roolit

- [x] Aikuinen näkee omat henkilötietonsa
- [x] Aikuinen näkee lastensa henkilötiedot
- [x] Lapsi näkee omat henkilötietonsa
- [x] Ryhmänohjaaja näkee ryhmänsä jäsenten tiedot
- [x] Ryhmänohjaaja näkee ryhmänsä lasten huoltajien yhteystiedot
- [x] Toimihenkilö näkee kaikkien jäsenten tiedot

#### Kyselyt

```sql
# Omat henkilötiedot
SELECT id, etunimi, sukunimi,puhelin, email, salasana,syntymaaika, toimihenkilo,
    varotieto, jasenyysalkoi, jasenyyspaattyi
FROM henkilo
WHERE henkilo.id = ?

# Huollettavien henkilötiedot
SELECT henkilo.id, henkilo.etunimi, henkilo.sukunimi, henkilo.puhelin,
		henkilo.email, henkilo.salasana, henkilo.syntymaaika, henkilo.toimihenkilo,
    henkilo.varotieto, henkilo.jasenyysalkoi, henkilo.jasenyyspaattyi
FROM henkilo, huoltajuus
WHERE ? = huoltajuus.huoltaja AND henkilo.id = huoltajuus.huollettava

#Huoltajan henkilötiedot
SELECT henkilo.id, henkilo.etunimi, henkilo.sukunimi, henkilo.puhelin,
henkilo.email, henkilo.salasana, henkilo.syntymaaika, henkilo.toimihenkilo,
henkilo.varotieto, henkilo.jasenyysalkoi, henkilo.jasenyyspaattyi
FROM henkilo, huoltajuus
WHERE ? = huoltajuus.huollettava AND henkilo.id=huoltajuus.huoltaja
```

### Henkilötietojen muokkaaminen

#### Roolit

- [x] Aikuinen päivittää omia henkilötietojaan
- [x] Aikuinen päivittää lastensa henkilötietoja
- [x] Toimihenkilö muokkaa jäsenen tietoja
- [x] Toimihenkilö merkitsee jäsenen eronneeksi
- [x] Toimihenkilö merkitsee jäsenen toimihenkilöksi

#### Kysely

```sql
UPDATE henkilo SET etunimi=?, sukunimi=?, puhelin=?, syntymaaika=?,
email=?, varotieto=? WHERE henkilo.id = ?


```

### Salasanan vaihtaminen

#### Roolit

- [x] Aikuinen vaihtaa oman salasanasa
- [x] Huoltaja vaihtaa lapsensa salasanan
- [x] Lapsi vaihtaa oman salasanansa
- [x] Toimihenkilö vaihtaa jäsenen salasanan

#### Kyselyt

```sql
UPDATE henkilo SET salasana=? WHERE henkilo.id = ?
```

## Ilmoittautumiset

### Ilmoittautumisten selaaminen

#### Roolit

 - [x] Aikuinen näkee ilmoittautumisensa
 - [x] Aikuinen näkee lastensa ilmoittautumiseet
 - [x] Lapsi näkee omat ilmoittautumisensa


#### Kysely

 ```sql
 SELECT ryhma.id, ryhma.nimi, ryhmassa.ohjaaja,kokous.alkaa, kokous.sijainti,
 	kokous.kuvaus, kokous.paattyy
 FROM ryhmassa JOIN ryhma ON ryhmassa.ryhmaid=ryhma.id
 LEFT OUTER JOIN Kokous ON Kokous.ryhmaid = ryhma.id AND Kokous.alkaa =
 (SELECT MIN(kokous.alkaa) FROM kokous WHERE kokous.alkaa > ? AND kokous.ryhmaid = ryhma.id)
 WHERE ryhmassa.henkiloid=? AND NOT ryhma.paattynyt AND ryhmassa.paattyen IS NULL ORDER BY nimi
 ```

### Uusi ilmoittautuminen

#### Roolit

- [x] Aikuinen ilmoittautuu ryhmään
- [x] Aikuinen ilmoittaa lapsensa ryhmään
- [x] Ryhmänohjaaja lisää jäseniä ryhmäänsä
- [x] Toimihenkilö lisää jäsenen ryhmään

#### Kyselyt

##### Mahdollisten ryhmien selaaminen

```sql
SELECT ryhma.id,nimi,paikkoja,kuvaus,a.lkm, ikavahintaan, ikaenintaan  
FROM ryhma LEFT OUTER JOIN
(SELECT ryhmaid, COUNT(id) AS lkm FROM ryhmassa
	WHERE NOT ohjaaja AND  paattyen IS NULL GROUP BY ryhmaid)
AS a ON ryhma.id=a.ryhmaid
WHERE ilmoittautuminenalkaa <= :tanaan AND ilmoittautuminenpaattyy >= :tanaan
AND ikavahintaan <= :ika AND ikaenintaan >= :ika
AND ryhma.id NOT IN (SELECT ryhmaid FROM ryhmassa WHERE henkiloid=:henkiloid)
AND NOT ryhma.paattynyt
ORDER BY nimi
```

Kyselyissä nykyinen päivämäärä sijoitetaan Pythonissa :pvm-kenttään sen sijaan että käytettäisiin SQL:n *CURRENT_DATE*:a jotta palvelimen PostgreSQL:n aikavyöhyke ei vaikuttaisi hakuihin.

(Yritin muokata tätä kyselyä muotoon, jossa ei olisi alikyselyitä, mutta siinä tapauksessa en saanut mukaan ryhmiä, joissa ei ollut vielä yhtään ilmoittautumista)

##### Ryhmän tietojen näyttäminen

```sql
# Ryhmän tiedot
SELECT ryhma.id AS ryhma_id, ryhma.nimi AS ryhma_nimi, ryhma.paikkoja AS ryhma_paikkoja,
ryhma.ilmoittautuminenalkaa AS ryhma_ilmoittautuminenalkaa,
ryhma.ilmoittautuminenpaattyy AS ryhma_ilmoittautuminenpaattyy,
ryhma.ikavahintaan AS ryhma_ikavahintaan, ryhma.ikaenintaan AS ryhma_ikaenintaan,
ryhma.kuvaus AS ryhma_kuvaus, ryhma.paattynyt AS ryhma_paattynyt
FROM ryhma
WHERE ryhma.id = ?

# Ohjaajat
SELECT etunimi, sukunimi, puhelin, email
FROM ryhmassa JOIN henkilo
ON ryhmassa.henkiloid=henkilo.id WHERE ryhmaid=? AND ohjaaja ORDER BY sukunimi

# Kokoontumiset
SELECT kokous.id, kokous.alkaa, kokous.paattyy, kokous.sijainti, kokous.kuvaus
FROM kokous WHERE ryhmaid=? AND kokous.paattyy > ? ORDER BY kokous.alkaa

```

##### Ryhmään ilmoittautuminene

```sql
INSERT INTO ryhmassa (ryhmaid, henkiloid, ohjaaja, alkaen, paattyen) VALUES (?, ?, ?, ?, ?)
```


### Ilmoittautumisten poistaminen

#### Roolit

- [x] Ryhmänohjaaja poistaa jäseniä ryhmästään
- [x] Toimihenkilö poistaa jäsenen ryhmästä

#### Kysely

```sql
UPDATE ryhmassa SET paattyen=? WHERE ryhmassa.id = ?
```

Jäsenyystietoa ei siis poisteta, vaan ryhmän jäsenyys merkitään päättymään. Näin ei koidu viite-eheyden ongelmia länsnäolotietoja tarkasteltaessa tai tilastoja laskettaessa.

## Kalenteri

#### Roolit

- [x] Aikuinen näkee kalenterissa omat ja lastensa kokoukset
- [x] Lapsi näkee kanterissa omat kokouksensa

##### Kysely

```sql
SELECT henkilo.etunimi, ryhma.nimi, kokous.alkaa, kokous.paattyy,
kokous.sijainti, kokous.kuvaus, kokous.id, ryhmassa.ohjaaja, Henkilo.id
FROM henkilo
JOIN ryhmassa ON henkilo.id=ryhmassa.henkiloid
JOIN ryhma ON ryhmassa.ryhmaid=ryhma.id
JOIN kokous ON kokous.ryhmaid=ryhma.id
WHERE (ryhmassa.henkiloid=?
  OR ryhmassa.henkiloid in (SELECT huollettava FROM huoltajuus WHERE huoltaja=?))
AND kokous.paattyy >= ? ORDER BY kokous.alkaa

```

## Ryhmien hallinta

### Ryhmän lisääminen

#### Roolit
- [x] Toimihenkilö luo uuden ryhmän

#### Kysely

```sql
INSERT INTO ryhma (nimi, paikkoja, ilmoittautuminenalkaa, ilmoittautuminenpaattyy,
	ikavahintaan, ikaenintaan, kuvaus, paattynyt) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
```

### Ryhmän poistaminen

#### Roolit
- [x] Toimihenkilö poistaa ryhmän

#### Kysely

```sql
DELETE FROM ryhma WHERE ryhma.id = ?
```

### Ryhmän tietojen muokkaaminen

#### Roolit
- [x] Ryhmänohjaaja muokkaa ryhmänsä tietoja
- [x] Toimihenkilö muokkaa ryhmän tietoja

#### Kysely

```sql
UPDATE ryhma SET nimi=?, paikkoja=?, ilmoittautuminenalkaa=?, ilmoittautuminenpaattyy=?,
ikavahintaan=?, ikaenintaan=?, kuvaus=?, paattynyt=? WHERE ryhma.id = ?
```


## Kokousten hallinta

### Kokousten lisääminen

#### Roolit
- [x] Ryhmänohjaaja lisää kokouksen (kokoussarjan) ryhmälleen
- [x] Toimihenkilö lisää kokouksen (kokoussarjan)

#### Kysely

```sql
INSERT INTO kokous (ryhmaid, alkaa, paattyy, sijainti, kuvaus, memo)
VALUES (?, ?, ?, ?, ?, ?)
```


### Kokousten muokkaaminen

#### Roolit
- [x] Ryhmänohjaaja muokkaa ryhmänsä kokouksen tietoja
- [x] Toimihenkilö muokkaa kokouksen tietoja

#### Kysely

```sql
UPDATE kokous SET alkaa=?, paattyy=?, sijainti=?, kuvaus=? WHERE kokous.id = ?
```


### Kokouksen poistaminen

#### Roolit
- [x] Ryhmänohjaaja peruu (poistaa) kokouksen  
- [x] Toimihenkilö peruu (poistaa) kokouksen

#### Kysely

```sql
DELETE FROM kokous WHERE kokous.id = ?
```


### Läsnäolleiden merkitseminen

#### Roolit
- [x] Ryhmänohjaaja merkitsee kokouksessa läsnäolleet
- [x] Toimihenkilö merkitsee kokouksessa läsnäolleet

#### Kysely

##### Menneiden kokousten luettelon näyttäminen

```sql
SELECT kokous.id, kokous.alkaa, kokous.sijainti, kokous.kuvaus, count(lasnaolo.ryhmassa) FROM kokous
LEFT OUTER JOIN lasnaolo on kokous.id=lasnaolo.kokous
WHERE ryhmaid=? AND kokous.alkaa < ?
GROUP BY kokous.id, kokous.alkaa, kokous.sijainti, kokous.kuvaus
ORDER BY kokous.alkaa DESC

```

##### Läsnäololistan hakeminen

```sql
SELECT etunimi, sukunimi, ryhmassa.id, lasnaolo.ryhmassa, henkilo.varotieto,
	ryhmassa.ohjaaja FROM ryhmassa
JOIN henkilo ON ryhmassa.henkiloid=henkilo.id
LEFT OUTER JOIN lasnaolo ON ryhmassa.id=lasnaolo.ryhmassa AND lasnaolo.kokous=?
WHERE ryhmassa.ryhmaid=? ORDER BY sukunimi,etunimi
```

##### Läsnäolleiden merkitseminen

```sql
INSERT INTO lasnaolo (ryhmassa, kokous) VALUES (?, ?)
```


## Tilastot

### Yksittäisen ryhmän tilasto

Tilaston yhteydessä näytetään ryhmän läsnäolotiedot.

#### Roolit

- [x] Ryhmänohjaaja näkee oman ryhmänsä läsnäolotilastot
- [x] Toimihenkilö näkee yksittäisen ryhmän tilaston

#### Kyselyt

##### Ryhmän yhteenvetotilasto
```sql
SELECT COUNT(distinct kokous.id), COUNT(lasnaolo.kokous) FROM kokous
LEFT OUTER JOIN lasnaolo ON lasnaolo.kokous=kokous.id                     
WHERE kokous.alkaa BETWEEN :alkaa AND :loppuu
AND kokous.ryhmaid=:ryhmaid
```

#### Läsnäolotilasto
```sql
SELECT sukunimi, etunimi, count(lasnaolo.kokous) AS lasna, ryhmassa.ohjaaja FROM lasnaolo
JOIN ryhmassa ON lasnaolo.ryhmassa=ryhmassa.id
JOIN henkilo ON ryhmassa.henkiloid=henkilo.id
JOIN kokous ON lasnaolo.kokous=kokous.id
WHERE kokous.ryhmaid=:ryhmaid AND
kokous.alkaa BETWEEN :alkaa AND :loppuu GROUP BY henkilo.id
ORDER BY lasna DESC
```

### Koko yhdistyksen tilasto

#### Roolit

- [x] Toimihenkilö näkee koko yhdistyksen tilastot

#### Kysely

```sql
SELECT ryhma.nimi, kokous.ryhmaid, COUNT(distinct kokous.id), COUNT(lasnaolo.kokous)
 FROM kokous
 LEFT OUTER JOIN lasnaolo ON lasnaolo.kokous=kokous.id
 JOIN ryhma ON kokous.ryhmaid=ryhma.id
 WHERE kokous.alkaa BETWEEN :alkaa AND :loppuu
 GROUP BY kokous.ryhmaid
 ORDER BY nimi
```
