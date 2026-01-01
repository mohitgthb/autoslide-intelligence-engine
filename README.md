# AutoSlide Intelligence Engine

## Overview
AutoSlide Intelligence Engine is an AI-powered system that evaluates the quality of pathology slide images by combining deep learning and classical computer vision techniques.

## Features
- Tile-based processing for large images
- Custom-trained blur detection model
- Tissue coverage estimation using OpenCV
- Stain quality scoring via color analysis
- Explainable heatmaps for visual interpretation
- Automated quality decision (ACCEPT / REVIEW / REJECT)

## Tech Stack
- Python, FastAPI
- PyTorch
- OpenCV, NumPy
- REST APIs

## Pipeline
Upload Image → Tiling → Blur Inference → Tissue & Stain Analysis → Quality Aggregation → Decision

## Future Work
- Support for whole-slide image formats (SVS, TIFF)
- Model retraining with real clinical data
- Web dashboard using MERN stack
- Cloud deployment and scaling

