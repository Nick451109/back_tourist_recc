# back_tourist_recc
AI backend project for tourists recommendations

## Create virtual env
python3 -m venv ambiente_virt

## Activate virtual env
source ambiente_virt/bin/activate

## Migrations
python manage.py makemigrations
python manage.py migrate

## Install requirements
pip install -r requirements.txt

## Create super user
python3 manage.py createsuperuser
