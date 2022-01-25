git clone https://github.com/henry512/group-r5-api-books.git api-books
cd api-books
git checkout main
git pull
docker build -t api-books:latest .
cd ..