# 📐 Chapter 01: The Circle and the Shadows (Trigonometry)

## 🧠 The Core Intuition
Angles do not naturally belong in arbitrary degrees (360°); they belong in **radians**—measuring angles using the circle's own radius as a flexible ruler. 

When a radius of length `1` rotates inside a circle, it projects two continuous shadows and one tangent line:
* **Cosine ($\cos \theta$):** The horizontal shadow cast onto the ground (X-axis), moving smoothly between `-1` and `1`.
* **Sine ($\sin \theta$):** The vertical shadow cast onto the wall (Y-axis), moving smoothly between `-1` and `1`.
* **Tangent ($\tan \theta$):** The ratio between Sine and Cosine ($\sin \theta / \cos \theta$). Whenever Cosine reaches `0` (at $90^\circ$ and $270^\circ$), the tangent shoots toward infinity.

## 📊 Connection to Data Science
In Machine Learning and Time Series analysis, real-world phenomena like daily temperatures, website traffic, or retail sales follow repeating cycles. Converting time into Sine and Cosine waves allows algorithms to understand that **11:59 PM is right next to 12:01 AM**, preserving cyclical continuity.

## 🚀 Run the Interactive Lab
```bash
streamlit run app.py
```
