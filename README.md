# LuxsoftTest

Welcome to the LuxsoftTest!

## The code
Here you can find the code in The TestProject folder. It is modulized in 3 parts:
*gihub helpers to provide github api operations
*file helpers to provide file operations
*wokflows to provide the tests

## Virtual environment
As a virtual environment I used the pipenv tool. You can find the Pipfile and Pipfile.lock files in the root TestProject folder.

## Docker
Also you can find the docker-file in the root folder to build the docker image.

## Service information
Pystet is already configured by the pytest.ini file. You can find the configuration in the TestProject root folder to run the tests by just "pytest --user=XXX --url=XXX --token=XXX" command.

## How to use
The better approach is to download docker image using "docker pull zanevskiromandocker/luxsoft_test:latest" and run the container. You can find the docker hub repository here: https://hub.docker.com/repository/docker/zanevskiromandocker/luxsoft_test. Just run the container with the following command: "docker run -it zanevskiromandocker/luxsoft_test:latest pytest --user=<Past the user name from the letter> --url=https://api.github.com --token=<Past the token from the letter>". But in that case, you should take care about report interception. 

By the way. You can just run the container, and then run the tests by the following command: "pytest --user=<Past the user name from the letter> --url=https://api.github.com --token=<Past the token from the letter>" and then you can find the reports in the TestProject/reports folder.
You can see the created repos links in the console output. Or you can find them in Test account repositories(sample: https://github.com/RZBotTester?tab=repositories).

## Reports
As mentioned above, reports are generated in the TestProject/reports folder. You can find the html report and the xml report there.
*Xml report is used by CI/CD tools to provide the test results.
*Html report is used by the developers to see the test results in the more readable format.
