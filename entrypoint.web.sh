#!/bin/bash

python3 install/install.py

exec streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0