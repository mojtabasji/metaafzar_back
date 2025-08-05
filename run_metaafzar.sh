
python manage.py migrate
python manage.py collectstatic --noinput
# create a superuser if it doesn't exist with password 'admin'
echo "from django.contrib.auth import get_user_model; from django.contrib.auth.hashers import make_password; User = get_user_model(); User.objects.get_or_create(username='$DJ_USERNAME', email='$DJ_EMAIL', is_superuser=True, is_staff=True, defaults={'password': make_password('$DJ_PASSWORD')})" | python manage.py shell
python manage.py runserver 0.0.0.0:8930
