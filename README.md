# AI Powered Financial Data Insights Tool

Developed and deployed an AI-driven financial insights platform that allows users to explore and query companies' 10-K reports with natural language questions.

# Project Overview

This repository contains a full-stack AI solution leveraging **Streamlit**, **Langchain**, **OpenAI GPT models**, and **HuggingFace embeddings**.  
It enables understanding complex financial documents and provides interactive, AI-generated answers about revenue, risks, trends, and more.

## Files

### 1. `src/app.py`  
Main Streamlit app that serves the user interface, including company selection and question input.

### 2. `src/rag_chain.py`  
Core backend logic to retrieve relevant document chunks using FAISS vector store and generate answers with OpenAI models.

### 3. `src/ingest.py`  
Scripts to preprocess and ingest 10-K financial reports into vector stores.

### 4. `src/prompts.py`  
Prompt engineering templates for the AI question answering.

### 5. `requirements.txt`  
Specifies all Python dependencies needed to run this application.

## Installation

### Clone the repo
git clone https://github.com/gannavarapu-priya/
cd your-repo-name
