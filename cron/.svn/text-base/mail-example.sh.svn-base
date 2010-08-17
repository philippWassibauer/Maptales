. /home/philipp/Documents/workspace/maptales/cron/settings.conf

# activate virtual environment
echo $WORKON_HOME/bin/activate
source $WORKON_HOME/bin/activate

cd $PROJECT_ROOT
python manage.py send_mail >> $PROJECT_ROOT/logs/cron_mail.log 2>&1