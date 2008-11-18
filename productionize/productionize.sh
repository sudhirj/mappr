rm -r ../static-production
mkdir ../static-production
mkdir ../static-production/images
cp ../static/images/* ../static-production/images/
python packager.py