# 📂 Dataset Description – StegoAI (Advanced Steganalysis Dataset)

---

## 📌 Overview

This dataset is specifically designed for **PDF Steganalysis**, enabling detection of covert data hidden within document structures.

The dataset supports:

* **Binary Classification**

  * `0 → Clean`
  * `1 → Stego`

* **Forensic-level feature analysis**

* **Multi-technique steganography detection**

---

## 📊 Dataset Scale

| Property      | Value                          |
| ------------- | ------------------------------ |
| Dataset Type  | Structured Feature Dataset     |
| Domain        | Cyber Forensics / Steganalysis |
| Total Samples | ~19K+                          |
| Classes       | Clean / Stego                  |
| Feature Count | 21+                            |
| Label Type    | Binary                         |

---

## 🧪 Steganographic Dataset Generation

To simulate real-world attack scenarios, each clean PDF was transformed into multiple stego variants using **eight distinct steganographic techniques**:

### 🔐 Applied Techniques

| Code | Technique                 | Description                                      |
| ---- | ------------------------- | ------------------------------------------------ |
| T01  | Metadata Hiding           | Payload embedded in Title, Author, Keywords, XMP |
| T02  | Invisible Text Embedding  | White or tiny font hidden text                   |
| T03  | Text Spacing Manipulation | Encoding via spacing patterns                    |
| T04  | Zero-Width Unicode        | ZWSP, ZWNJ, ZWJ insertion                        |
| T05  | PDF Comments Injection    | Hidden data in comments                          |
| T06  | Unused Objects Embedding  | Extra PDF objects for payload                    |
| T07  | Stream Padding            | Junk bytes in streams                            |
| T08  | Image Steganography       | LSB-based hiding in images                       |

---

## ⚙️ Payload Variants

Each technique is applied with different embedding intensities:

* **v1 → Low Payload (stealthy)**
* **v2 → Medium Payload**
* **v3 → High Payload (detectable)**

### 📈 Expansion Strategy

Each clean PDF generates:

```
8 Techniques × 3 Variants = 24 Stego Files per Source
```

✔ Maintains **source traceability**
✔ Enables **controlled experimentation**

---

## 🧠 Feature Engineering

Each PDF is converted into a **high-dimensional forensic feature vector**.

### 🔑 Extracted Features

The dataset includes the following key attributes:

```
file_size, page_count, object_count, avg_objects_per_page,
orphan_object_depth, metadata_length, metadata_key_count,
metadata_value_entropy, zero_width_unicode_density,
invisible_text_ratio, avg_char_spacing_deviation,
whitespace_run_variance, comment_length_ratio,
xref_gap_score, padding_byte_ratio,
image_count, image_entropy_delta, image_size_anomaly,
page_object_distribution_entropy,
text_to_nontext_ratio, structural_complexity_score, label
```



---

## 🧩 Feature Categories

### 📁 1. Structural Features

* object_count
* avg_objects_per_page
* orphan_object_depth
* structural_complexity_score

### 🧾 2. Metadata Analysis

* metadata_length
* metadata_key_count
* metadata_value_entropy

### 🔍 3. Steganographic Indicators

* zero_width_unicode_density
* invisible_text_ratio
* comment_length_ratio
* padding_byte_ratio

### ✍️ 4. Text Behavior Features

* avg_char_spacing_deviation
* whitespace_run_variance
* text_to_nontext_ratio

### 🖼️ 5. Image-Based Features

* image_count
* image_entropy_delta
* image_size_anomaly

### 📊 6. Distribution & Complexity

* page_object_distribution_entropy
* xref_gap_score

---

## ⚖️ Data Distribution

* Balanced distribution between **Clean and Stego**
* Controlled generation ensures:

  * No bias toward specific technique
  * Uniform coverage across payload strengths

---

## 🧠 Learning Characteristics

This dataset captures:

* **Structural anomalies**
* **Entropy variations**
* **Hidden pattern distributions**
* **Encoding artifacts**

✔ Suitable for:

* Random Forest
* XGBoost
* LightGBM
* Deep hybrid models

---

## 🚧 Challenges

* Subtle difference between clean and low-payload stego files
* High intra-class similarity
* Feature overlap in advanced hiding techniques
* Requires **feature-sensitive models**

---

## 🔐 Strengths

✔ Multi-technique coverage
✔ Multi-intensity payload simulation
✔ Realistic forensic signals
✔ High feature richness
✔ Reproducible pipeline

---

## 🚀 Future Improvements

* Multi-format steganography (image, audio, video)
* Real-world adversarial samples
* Transformer-based feature extraction
* Graph-based PDF structure modeling

---

## 🧠 Conclusion

This dataset provides a **comprehensive, multi-dimensional representation of PDF steganography**, enabling robust detection systems for real-world cybersecurity applications.

It forms the backbone of the **StegoAI detection engine**, bridging **digital forensics and machine learning**.

---
