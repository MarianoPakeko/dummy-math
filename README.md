# 📐 Dummy Math: Visual & Intuitive Mathematics for Data Science

**Dummy Math** is an interactive educational project built with Python and Streamlit. Its goal is to bridge the gap between abstract mathematical notation and real-world spatial intuition.

Instead of static formulas, each chapter acts as a hands-on visual laboratory where learners can manipulate parameters and observe how mathematical concepts behave in real time—and how they directly power modern Data Science and Machine Learning algorithms.

---

## 🗂️ Interactive Chapters

### [01. The Circle and the Shadows (Trigonometry)](./01-trigonometria)
* **Visual Intuition:** Understanding radians as physical arcs and viewing **Sine**, **Cosine**, and **Tangent** as real-time shadows projected by a rotating radius.
* **Data Science Connection:** Modeling seasonality, cyclical patterns, and time-series decomposition.

### [02. The Giant Compressor (Logarithms)](./02-logaritmos)
* **Visual Intuition:** Turning massive multiplicative leaps into manageable linear steps—mirroring how human senses perceive sound and scale.
* **Data Science Connection:** Feature scaling, handling skewed financial distributions, and stabilizing variance.

### [03. The Magnifying Glass and the Blocks (Calculus)](./03-calculo)
* **Visual Intuition:** Zooming into a curve until it becomes a straight line (Derivatives) and stacking rectangles to fill the area beneath it (Integrals).
* **Data Science Connection:** Gradient Descent optimization and Area Under the Curve (ROC-AUC) evaluation.

### [04. The Shape Factory (Euler & Fourier)](./04-fourier)
* **Visual Intuition:** Combining simple rotating circles (epicycles) to draw complex closed geometries and clean noisy signals.
* **Data Science Connection:** Signal processing, Fast Fourier Transform (FFT), and frequency-domain analysis.

---

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Numerical Computing:** NumPy
* **Interactive Visualization:** Plotly / Matplotlib
* **Web Application Framework:** Streamlit

## 🚀 How to Run Locally
```bash
git clone https://github.com
cd dummy-math
pip install -r requirements.txt
streamlit run 01-trigonometria/app.py
```
