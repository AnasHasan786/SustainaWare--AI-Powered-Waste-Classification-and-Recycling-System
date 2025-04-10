# **♻️ SustainaWare - AI-Powered Waste Classification & Recycling System**

An AI-powered platform that combines Object Detection, Natural Language Processing, and an intuitive frontend to help people identify, classify, and recycle waste efficiently.

## **📖 Table of Contents**

1. [🔍 Overview](#-overview)
2. [🌟 Key Features](#-key-features)
3. [🌱 Impact & Goals](#-impact--goals)
4. [📌 Methodology](#-methodology)
5. [📊 Dataset Details](#-dataset-details)
6. [🛠️ Tech Stack – The Power Behind SustainaWare](#️-tech-stack--the-power-behind-sustainaware)
7. [🏗️ System Architecture](#️-system-architecture)
8. [⚙️ Installation Guide](#️-installation-guide)
9. [🧪 How it Works](#-how-it-works)
10. [📈 Results and Model Evaluation](#-results-and-model-evaluation)
11. [🚀 Future Enhancements](#-future-enhancements)
12. [🧑‍💻 Author](#-author)
13. [📜 License](#-license)

## **🔍 Overview**

<p align="justify">SustainaWare is an <b>AI-powered waste classification and recycling assistance system</b> that leverages <b>deep learning, NLP, and a structured database</b> to improve waste management efficiency. It enables users to <b>automatically classify waste types, receive real-time recycling instructions, and interact via text-based queries</b> for better disposal and sustainability practices. This project integrates <b>YOLOv8 for waste classification</b>, a <b>FastAPI backend</b> for user management and waste tracking, and an <b>NLP-powered chatbot</b> to answer recycling-related questions.</p>

## **🌟 Key Features**

- **AI-Powered Waste Classification**: Uses YOLOv8 to detect and classify 8 different waste categories from images.
- **FastAPI Backend**: Manages user authentication, waste records, feedback collection, and recycling instructions.
- **NLP-Based Query System**: Allows users to ask text-based questions about waste management and receive AI-driven responses.
- **Dynamic User Interaction**: Users can upload images, receive real-time classification results, and get proper disposal guidelines.
- **Continuous Model Improvement**: Integrates user feedback to enhance classification accuracy and expand dataset quality.

## **🌱 Impact & Goals**  

- Promote responsible waste disposal to reduce pollution and improve recycling rates.  
- Enhance AI-driven waste classification for better automation in smart waste management.  
- Encourage sustainability by making waste disposal simple, accessible, and tech-driven.

## **📌 Methodology**

The proposed waste classification and recycling system follows a structured methodology that concatenates object detection, natural language processing, database management and an intuitive user interface to enhance waste management efficiency. The systematic methodology consists of the following stages:

**a) Data Collection:** The system uses an object detection dataset containing annotated images for 8 waste categories: Plastic Bottle, Glass Jar, Banana Peel, Paper, Aluminum Can, Cardboard, Food Waste, and Metal Scrap.

**b) Data Cleaning and Preprocessing:** The data gathered from Roboflow was already preprocessed eliminating the need for further transformations such as resizing or normalization.

**c) Data Splitting:** The dataset was divided into training (80%), validation (10%), and test (10%) sets to ensure model generalization and prevent overfitting.

**d) Model Training:** The YOLOv8 object detection model has been trained for 50 epochs with a batch size of 16 and an image resolutio of 640 x 640 pixels.

**e) Building the Backend API:** A FastAPI-based backend serves as the system's core, handling:

- User Authentication (Login / Signup)
- Image Classification (via YOLOv8)
- Query Response Handling (via NLP module)
- Recycling Guidance Handling (from the database)

**f) NLP-Based Query Module:** An open-source NLP model (DistilBERT and Sentence Transformer) handles text-based recycling queries. It uses cosine similarity and extractive QA models to respond accurately.

**g) Frontend Development:** A React.js frontend that enables users to interact with the system. Users can:-

- Upload images for classification
- View real-time classification results
- Submit queries
- Provide feedback on system responses

**h) Waste Classification Results:** In result, the system returns the classified waste category, estimated weight and with all other relevant info. It also returns the classification confidence of our YOLOv8 model. These details are fetched from the trained model and the backend database.

**i) Feedback Collection:** A feedback mechanism enables users to rate the accuracy of classifications and the usefulness of chatbot responses.

## **📊 Dataset Details**

The dataset used for this project was sourced from Roboflow, a well-established platform for sharing and managing computer vision datasets. It is specifically designed for object detection tasks and perfectly suited for our waste classification use case.

### **📁 Dataset Summary**

| Attribute         | Description                                             |
|-------------------|---------------------------------------------------------|
| **Source**        | Roboflow (Custom Object Detection Dataset)              |
| **Type**          | Annotated Images (YOLO Format - Bouding Boxes)          |
| **Total Images**  | 4, 592                                                  |
| **Classes**       | 8 Waste Categories                                      |
| **Image Format**  | JPEG/PNG with associated YOLO `.txt` annotation files   |
| **Annotations**   | Bounding boxes (YOLOv8 compatible format)               |

## **🛠️ Tech Stack – The Power Behind SustainaWare**

The project integrates multiple technologies across the machine learning, backend, frontend and database layers to create a complete AI-powered waste classification and recycling system. Here's a full breakdown:

### **🧠 Artificial Intelligence and Natural Language Processing**

| Technology                                  | Description                                                                                                          |
|---------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| YOLOv8 (You Only Look Once v8)              | State-of-the-art object detection model used to classify waste images into 8 categories.                             |
| Sentence Transformers (`all-MiniLM-L6-v2`)  | Pre-trained model used for semantic similarity matching and extracting relevant answers to user queries.             |
| DistilBERT                                  | Lightweight transformer model fine-tuned for extractive Question Answering (QA) on text-based recycling queries.     |
| Cosine Similarity                           | Similarity metric used to match user queries with the most relevant database entries.                                |

### **⚙️ Backend Development**

| Technology         | Description                                                                      |
|--------------------|----------------------------------------------------------------------------------|
| FastAPI            | High-performance Python web framework used to build the RESTful API.             |
| Uvicorn            | ASGI server for running the FastAPI app efficiently.                             |
| SQLAlchemy         | ORM (Object-Relational Mapper) to interact with the PostgreSQL database.         |
| Pydantic           | Used for data validation and enforcing type hints in request/response models.    |
| Python-dotenv      | Loads environment variables from .env files.                                     |
| Logging Module     | Enables detailed logging and debugging of API endpoints and user interactions.   |

### **🗂️ Database Layer**

| Technology            | Description
|-----------------------|---------------------------------------------------------------------------------------------------------|
| PostgreSQL            | Stores all persistent data including user records, waste classification logs, queries, and feedback.    |
| SQLAlchemy ORM        | Handles database schema, relationships, and migrations using Python classes.                            |

### **🌐 Frontend Development**

| Technology          | Description
|---------------------|-----------------------------------------------------------------------------------|
| React.js            | Frontend library for building a responsive and modular single-page application.   |
| Tailwind CSS        | Utility-first CSS framework for building custom and responsive UI components.     |
| Axios               | Handles API calls between React frontend and FastAPI backend.                     |
| React Router DOM    | Enables multi-page navigation and route protection based on user roles.           |

### **🔍 API Testing and Debugging**

| Tool                | Description
|---------------------|-----------------------------------------------------------------------------------|
| Restfox             | REST API client used for testing endpoints during development.                    |
| HTTP Status Codes   | Properly used for meaningful API responses (e.g. 200, 401, 500, etc.)             |

## **🏗️ System Architecture**

🖼️ Below is the visual representation of the SustainaWare System Architecture: 

<p align="center">
  <img src="https://i.imgur.com/oAtVUMn.png" alt="System Architecture" width="600">
</p>

## **⚙️ Installation Guide**

Follow the steps below to set up and run SustainaWare on your local machine.

### 1. Clone the Repository

```bash
https://github.com/AnasHasan786/SustainaWare--AI-Powered-Waste-Classification-and-Recycling-System.git
cd SustainaWare--AI-Powered-Waste-Classification-and-Recycling-System
```
### 2. Backend Setup
Navigate to the backend folder and set up a virtual environment

```bash
cd backend
python -m venv venv
```

Activate the virtual environment:

- On Windows:

```bash
venv/Scripts/activate
```

- On macOS/Linux:

```bash
source venv/bin/activate
```

Install the backend dependencies:

```bash
pip install -r requirements.txt
```
Create a .env in the backend as specified by the `.env_file_format` present in `backend/.env_file_format`.

Run the FastAPI development server:

```bash
fastapi dev main.py
```

The backend server will start on `http://127.0.0.1:8000/`

### 3. Frontend Setup

In a new terminal window, navigate to the frontend folder:

```bash
cd frontend
```

Install frontend dependencies and start the development server:

```bash
npm install
npm run dev
```

The frontend will typically be available at `http://localhost:5173/`

### 4. Access the Application

Once both servers are running, open your browser and visit the frontend URL (e.g. `http://localhost:5173/`) to use the application.

## **🧪 How it Works**

1. User uploads image via frontend.
2. Image is sent to the FastAPI backend.
3. YOLOv8 model detects and classifies the waste item.
4. Classification info + recycling guidance is fetched from DB.
5. User can also ask text-based recycling queries.
6. NLP model processes the text and return accurate response.
7. User gives feedback - stored in DB.

## **📈 Results and Model Evaluation**

- YOLOv8 (mAP@50): 93.1%
- YOLOv8 (mAP@50-95): 75.3%
- Precision: 93.2%
- Recall: 86.0%
- NLP Accuracy: 80.53% (using cosine similarity)

## **🚀 Future Enhancements**

To continuously improve the performance, scalability, and intelligence of the system, several future enhancements are planned:

- Integraton of Multimodal AI Capabilities
- Expansion of Waste Categories
- LLM-Based Contextual Understanding
- Mobile App Development

## **🧑‍💻 Author**

Anas Hasan
Final Year CSE-AIML Student
E-mail: anas.hassan9417@gmail.com
GitHub: [Check my Gihub profile](https://github.com/AnasHasan786)
LinkedIn: [Visit my LinkedIn profile](https://www.linkedin.com/in/anas-hasan-a5546524b/)

## **📜 License**

This project is **not open-source**.

All rights are reserved by the author. The code is made public **only for portfolio and demonstration purposes**. Unauthorized use, reproduction, or distribution of any part of this project is strictly prohibited.
