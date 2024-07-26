FROM gradle:jdk17-jammy
WORKDIR /log-injection
ENV USER=gradle

COPY . .
CMD ["./gradlew", "bootRun", "--debug", "--stacktrace"]
