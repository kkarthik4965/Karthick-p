#!/usr/bin/env bash
# Starts backend (port 8000) and frontend (port 8501). Run from project root.
uvicorn legalEaseAPI.main:app --reload --port 8000 &
BACK=$!
trap "kill $BACK" EXIT
streamlit run frontend/app.py
