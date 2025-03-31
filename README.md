# ♻️ SustainaWare - AI-Powered Waste Classification & Recycling System

### **🔍 Overview**

SustainaWare is an **AI-powered waste classification and recycling assistance system** that leverages **deep learning, NLP, and a structured database** to improve waste management efficiency. It enables users to **automatically classify waste types, receive real-time recycling instructions, and interact via text-based queries** for better disposal and sustainability practices.

This project integrates **YOLOv8 for waste classification**, a **FastAPI backend** for user management and waste tracking, and an **NLP-powered chatbot** to answer recycling-related questions.

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



## 🛠️ Tech Stack – The Power Behind SustainaWare

SustainaWare isn’t just another waste management tool—it’s an **AI-driven ecosystem** that blends **computer vision, natural language processing, and smart database management** to create a seamless user experience.

### AI & Machine Learning
🚀 At its core, the system is powered by **YOLOv8**, a cutting-edge object detection model that classifies waste into **8 distinct categories** with precision. The training process wasn’t just about throwing data at a model; we **fine-tuned YOLOv8 over 50 epochs**, optimizing performance while keeping computational efficiency in check. The dataset? **Sourced from Roboflow**, ensuring high-quality labeled images for accurate detection.

💡 But classification alone isn’t enough—users often have **questions** about waste disposal. That’s where our **NLP-powered chatbot** steps in. Instead of relying on generic responses, we integrated **DistilBERT and Sentence Transformers**, enabling the chatbot to **understand and process user queries intelligently**. Whether it's _"Can I recycle this plastic?"_ or _"How do I dispose of electronic waste?"_, the system provides **context-aware answers** using **cosine similarity and QA models**.

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

# 🏗️ System Architecture

## 📌 Overview
The **SustainaWare** system is designed for **waste classification and recycling guidance** using a **multi-stage AI-powered pipeline**. The architecture consists of three major layers:

1️⃣ **Frontend (User Interaction)** → React.js-based interface  
2️⃣ **Backend (FastAPI + ML Models)** → Core logic handling classification, NLP queries, and data management  
3️⃣ **Database (PostgreSQL)** → Storing waste records, user interactions, and feedback  

The architecture ensures **real-time classification, intelligent query handling, and continuous learning** through user feedback.

---

## 🖼️ System Architecture Diagram

```mermaid
graph TD;
    A[User] -->|Uploads Image or Queries| B[Frontend (React.js)]
    B -->|Send Image to API| C[FastAPI Backend]
    B -->|Send Text Query| G[NLP Query Module]
    
    subgraph "🔹 Image Classification"
        C -->|Process Image| D[YOLOv8 Model]
        D -->|Classified Waste| E[PostgreSQL Database]
        E -->|Send Classification Result| B
    end
    
    subgraph "🔹 Query Handling"
        G -->|Check Similarity| H[SentenceTransformer]
        G -->|Generate Response if Needed| I[DistilBERT QA Model]
        H -->|Matched Topic| B
        I -->|Dynamically Generate Answer| B
    end
    
    subgraph "🔹 User Feedback & Learning"
        B -->|Submit Feedback| J[Feedback Module]
        J -->|Store Feedback| E
        J -->|Update Model Periodically| D
    end





