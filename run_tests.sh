rm -rf test-report
mkdir test-report
mkdir test-report/xml

python manage.py test story geo blog -d test-report/ --with-coverage --cover-package=geo --cover-package=story --cover-package=blog --with-xunit --xunit-file=test-report/xml/report.xml

