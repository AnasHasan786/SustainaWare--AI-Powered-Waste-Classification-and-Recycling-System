# **♻️ SustainaWare - AI-Powered Waste Classification & Recycling System**

### **🔍 Overview**

<p align="justify">SustainaWare is an <b>AI-powered waste classification and recycling assistance system</b> that leverages <b>deep learning, NLP, and a structured database</b> to improve waste management efficiency. It enables users to <b>automatically classify waste types, receive real-time recycling instructions, and interact via text-based queries</b> for better disposal and sustainability practices. This project integrates <b>YOLOv8 for waste classification</b>, a <b>FastAPI backend</b> for user management and waste tracking, and an <b>NLP-powered chatbot</b> to answer recycling-related questions.</p>

### **🚀 Why SustainaWare?**

Improper waste disposal leads to **environmental damage, pollution, and recycling inefficiencies.** SustainaWare provides an **automated, AI-driven solution** that assists individuals, businesses, and organizations in making informed waste disposal decisions.

### **🌟 Key Features**

- **AI-Powered Waste Classification**: Uses **YOLOv8** to detect and classify **8 different waste categories** from images.
- **FastAPI Backend**: Manages user authentication, waste records, feedback collection, and recycling instructions.
- **NLP-Based Query System**: Allows users to ask **text-based questions** about waste management and receive AI-driven responses.
- **Dynamic User Interaction**: Users can **upload images, receive real-time classification results, and get proper disposal guidelines.**
- **Continuous Model Improvement**: Integrates **user feedback** to enhance classification accuracy and expand dataset quality.

### 🌱 Impact & Goals  
📌 **Promote responsible waste disposal** to reduce pollution and improve recycling rates.  
📌 **Enhance AI-driven waste classification** for better automation in smart waste management.  
📌 **Encourage sustainability** by making waste disposal **simple, accessible, and tech-driven.**  

---

## 🛠️ Tech Stack – The Power Behind SustainaWare

SustainaWare isn’t just another waste management tool—it’s an **AI-driven ecosystem** that blends **computer vision, natural language processing, and smart database management** to create a seamless user experience.

### AI & Machine Learning
<p>🚀 At its core, the system is powered by <b>YOLOv8</b>, a cutting-edge object detection model that classifies waste into <b>8 distinct categories</b> with precision. The training process wasn’t just about throwing data at a model; we <b>fine-tuned YOLOv8 over 50 epochs</b>, optimizing performance while keeping computational efficiency in check. The dataset? <b>Sourced from Roboflow</b>, ensuring high-quality labeled images for accurate detection.</p>

<p>💡 But classification alone isn’t enough—users often have <b>questions</b> about waste disposal. That’s where our <b>NLP-powered chatbot</b> steps in. Instead of relying on generic responses, we integrated <b>DistilBERT and Sentence Transformers</b>, enabling the chatbot to <b>understand and process user queries intelligently</b>. Whether it's _"Can I recycle this plastic?"_ or _"How do I dispose of electronic waste?"_, the system provides <b>context-aware answers</b> using <b>cosine similarity and QA models</b>.</p>

### Backend – The Brain of SustainaWare
🖥️ Driving this AI powerhouse is our **FastAPI-based backend**, a **lightweight yet high-performance API layer** that efficiently handles:
- **User Authentication** – Secure login and access management.
- **Image Classification** – Instant processing of uploaded images.
- **Waste Records & Recycling Data** – A structured repository of user inputs and recycling guidelines.

🗄️ Speaking of structured data, we needed a **robust database** to store everything from **waste types and user feedback to recycling instructions**. That’s why we chose **PostgreSQL**, a rock-solid relational database, paired with **SQLAlchemy** for smooth ORM-based interactions.

### Frontend – A Seamless User Experience
🎨 On the **frontend**, we crafted a **dynamic and user-friendly React.js interface**. Users can:
- **Upload waste images** and get instant classification.
- **Chat with the AI assistant** for recycling guidance.
- **Receive real-time feedback** on waste disposal methods.

The frontend is styled with **Tailwind CSS**, ensuring a **clean, modern, and responsive UI**, while **Axios** bridges the communication between the frontend and backend.

### Development & Testing
🛠️ But what’s development without **efficient testing and version control**? Throughout the project, we leveraged:
- **Git** – For version tracking and smooth collaboration.
- **Restfox.dev** – For API testing, ensuring smooth debugging and performance optimization.

---

# 🏗️ System Architecture

## 📌 Overview
The **SustainaWare** system is designed for **waste classification and recycling guidance** using a **multi-stage AI-powered pipeline**. The architecture consists of three major layers:

1️⃣ **Frontend (User Interaction)** → React.js-based interface  
2️⃣ **Backend (FastAPI + ML Models)** → Core logic handling classification, NLP queries, and data management  
3️⃣ **Database (PostgreSQL)** → Storing waste records, user interactions, and feedback  

The architecture ensures **real-time classification, intelligent query handling, and continuous learning** through user feedback.

## 🌍 SustainaWare System Architecture

SustainaWare is an **AI-powered waste classification system** that processes **both images and text queries** to provide **accurate waste management insights**. It integrates multiple components to ensure a seamless user experience, efficient data processing, and continuous model improvements.  

### 🚀 **How It Works? (Step-by-Step Flow)**  

🧑‍💻 **1. User Interaction** 

🔹 The user **uploads an image** or **sends a text query** via the frontend.  
🔹 They can also access the **Dashboard** to view real-time **waste statistics**.  

🌐 **2. Frontend (React.js) → Backend (FastAPI)**  

🔹 The **frontend sends API requests** to the backend.  
🔹 The backend decides whether the request is **image-based** (processed by YOLOv8) or **text-based** (handled by the NLP module).  

🖼️ **3. Image Processing (YOLOv8 Model)**  

🔹 If an **image** is uploaded, the backend **routes it to YOLOv8** for classification.  
🔹 The **classification results** are stored in the PostgreSQL **database** and sent back to the user.  

🧠 **4. Text Processing (NLP Query Module)**  

🔹 If a **text query** is received, the backend **routes it to the NLP module**.  
🔹 **Sentence Transformer** checks for similarity with existing waste records.  
🔹 If needed, **DistilBERT/Gemini** generates an informative response.  
🔹 The processed answer is returned to the user.  

📊 **5. Dashboard (Waste Statistics & Insights)** 

🔹 Users can view **real-time waste classification analytics**.  
🔹 The backend fetches **waste data from PostgreSQL** and processes it for the dashboard.  

💡 **6. Feedback System & Model Retraining**  

🔹 Users can **submit feedback** about classification accuracy.  
🔹 Feedback is stored in the database and used for **continuous model improvement**.  

### 🏗️ **System Components**  

| 🏢 Component  | 🔥 Functionality |
|--------------|----------------|
| 🎨 **Frontend (React.js)** | User Interface, API Requests, Dashboard Display |
| 🚀 **Backend (FastAPI)** | Routes Queries, Processes Data, Connects Components |
| 🖼️ **YOLOv8 Model** | Classifies Waste from Images |
| 🧠 **NLP Query Module** | Text Processing, Similarity Search, Response Generation |
| 🛢️ **PostgreSQL Database** | Stores Waste Data, User Queries, Feedback |
| 📊 **Dashboard** | Displays Waste Statistics and Insights |
| 🔄 **Feedback System** | Collects User Feedback, Triggers Model Retraining |

### 📌 **System Architecture Diagram**  

🖼️ Below is the visual representation of the **SustainaWare System Architecture**: 

<p align="center">
  <img src="https://i.imgur.com/oAtVUMn.png" alt="System Architecture" width="600">
</p>




