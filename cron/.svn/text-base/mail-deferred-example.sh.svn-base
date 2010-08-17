. /home/philipp/Documents/workspace/maptales/cron/settings.conf

# activate virtual environment
source $WORKON_HOME/bin/activate

cd $PROJECT_ROOT
python manage.py retry_deferred >> $PROJECT_ROOT/logs/cron_mail_deferred.log 2>&1
