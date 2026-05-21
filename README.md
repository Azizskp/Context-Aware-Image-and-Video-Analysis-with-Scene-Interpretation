# 🚀 Context-Aware Image and Video Analysis with Scene Interpretation

---

## 📌 Overview

This project is an AI-based system that performs object detection and contextual scene interpretation on images and videos using YOLOv8, OpenCV, and contextual reasoning techniques.

The system detects objects such as:
- 👤 People
- 🚗 Vehicles
- 🐶 Animals
- 🪑 Furniture

and generates meaningful scene descriptions like:
- 🚦 Heavy traffic scene
- 🐕 Person walking a dog
- 🍽️ Dining environment
- 👥 Crowded public area

The project also includes an experimental AI-enhanced semantic reasoning module using DeepSeek/OpenRouter APIs.

---

## ✨ Features

- ⚡ Real-time object detection using YOLOv8
- 🖼️ Image and video analysis
- 🧠 Context-aware scene interpretation
- 📦 Bounding box visualization
- 📊 Confidence score display
- 🌐 Flask-based web interface
- 🤖 AI-enhanced semantic reasoning (experimental)
- 💻 Browser-based output display

---

## 🛠️ Technologies Used

- 🐍 Python
- 🎯 YOLOv8
- 👁️ OpenCV
- 🌐 Flask
- 🎨 HTML/CSS
- 🤖 DeepSeek/OpenRouter API
- 🔢 NumPy

---

## ⚙️ How the Project Works

1. 📤 User uploads image or video
2. 👁️ OpenCV processes media input
3. 🎯 YOLOv8 detects objects
4. 🧠 Context module interprets scene
5. 📦 Bounding boxes and labels are generated
6. ✅ Final output is displayed

---

## 🧩 Example Scene Interpretations

| Detected Objects | Scene Interpretation |
|------------------|----------------------|
| 👤 Person + 🐶 Dog | Person walking a dog |
| 🚗 Cars + 🚌 Buses | Heavy traffic scene |
| 🪑 Chairs + 🍽️ Dining Table | Dining environment |
| 👥 Multiple People | Crowded public area |

---

## 📁 Project Structure

```text
context-segmentation/
│
├── context/
├── models/
├── video/
├── templates/
├── static/
├── uploads/
├── output/
├── app.py
├── main.py
├── main1.py
├── requirements.txt
└── README.md
```

---

## ⚡ Installation

### 📥 Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Context-Aware-Image-and-Video-Analysis-with-Scene-Interpretation.git
```

### 📂 Move Into Project Folder

```bash
cd Context-Aware-Image-and-Video-Analysis-with-Scene-Interpretation
```

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Project

### 🌐 Run Flask Web App

```bash
python app.py
```

### 💻 Run Main Local Processing

```bash
python main.py
```

### 🤖 Run AI-Enhanced Version

```bash
python main1.py
```

---

## 🗂️ Dataset

The YOLOv8 model used in this project is pre-trained on the COCO dataset.

---

## 🚀 Future Enhancements

- 📷 Real-time webcam integration
- 🏃 Activity recognition
- 🔄 Multi-object tracking
- ☁️ Cloud deployment
- 🧠 Advanced AI-based semantic reasoning

---

## 👨‍💻 Author

Aziz
