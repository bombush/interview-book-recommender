# interview-book-recommender
Solution to an interview task

## Basic architecture
`recommender.py` contains the core recommendation algorithm.
The app uses two different frontends: a CLI version and a web-based version built on Streamlit.

## Online version
Available at ``http://alb-book-recommender-1285925029.eu-north-1.elb.amazonaws.com/``

## How to run locally

### Manually
#### CLI version
```sh
python3 install.py
python3 main.cli.py
```

#### Web version (will be available on `localhost:8501`)
```sh
python3 install.py
streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
```

### Docker
Choose which VERSION of the image you want to build.

#### CLI
```sh
docker build -t book-recommender-cli -f .\docker\Dockerfile.cli .
docker run -ti book-recommender-cli
```

#### WEB
```sh
docker build -t book-recommender-web -f .\docker\Dockerfile.web .
docker run -ti book-recommender-web
```

#### AWS
There is also a version of the web interface for deployment to AWS

```sh
docker build -t book-recommender-aws -f .\docker\Dockerfile.aws .
docker run -ti book-recommender-aws
```

## Possible future improvements:
- Use the same algorithm for finding book variants to analyze in CLI and Streamlit. (Streamlit frontend was quite heavily vibe coded)

- Basic data cleanup:
    - look for duplicates and average them. 
    - clean out missing fields 
    - remove implicit ratings. Implicit ratings are shown with value 0 in the dataset and only skew the rating averages towards lower values. There is probably way of using the implicit data for further analysis, but they are not useful for simple correlation based on user ratings. I left the implicit ratings in as even now, the dataset is quiete small and there are many books that don't have enough data to meet the minimum ratings requirement.

- More sophisticated data quality fixes:
    - There are typos of two kinds in the data: mangled non-ANSI characters and superfluous spaces (e.g. J.R.R. Tolkien != J. R. R. Tolkien when comparing Author-Name). Some of them might be fixable using some heuristic (e.g. normalizing to always including a space after an initial with a dot), others might need human intervention.
    - Work-Id pairings: many duplicities in the dataset are caused by the books having been reissued under different name or with different ISBN. In addition to causing duplicates, it also dilutes ratings for the books. (e.g. "The Fellowship of the Ring" should be grouped under the same Work-Id as "Lord of the Rings (Book1)"). We can use some heuristic (title similarity, Author-Name similarity) to find possible duplicates, but ensuring the editions are grouped correctly would require human intervention or cross referencing with some trustworthy open book database.

- Region-based rating
    - The dataset contains Users.csv which is not used for this task but contains users' country names. We could add more weight to ratings from the same country as the user's.

- Improvements for cloud hosting:
    - Download dataset to S3 as a build step in AWS. The data is included in the Docker image at this point, which is not ideal.

- checkout code from repository on AWS or make sure that all CRLF endings are changed to LF if developing on windows machine. Add dos2unix call as part of the build process.