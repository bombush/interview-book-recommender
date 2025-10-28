#!/bin/bash

aws s3 cp s3://amzn-s3-bookrecommender/Ratingss.csv /app/Downloads/Ratings.csv
aws s3 cp s3://amzn-s3-bookrecommender/Bookss.csv /app/Downloads/Books.csv
exec streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0