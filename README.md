# uumami_gallery
## Neuralblender scrapper
``` 
cd scrapper
docker build --tag uumami_gallery:scrapper .
docker run -it -e PASS=""  -e EMAIL="" -v /home/uumami/github/uumami_gallery/scrapper/images:/app uumami_gallery:scrapper
```

## Web/blog dash app


![image description](/home/uumami/github/uumami_gallery/scrapper/images/John von Neumann.png)