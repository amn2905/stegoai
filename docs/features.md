# 🧠 Feature Engineering Documentation – StegoAI

---

## 📌 Overview

This document explains the **forensic features** used in the StegoAI system for detecting hidden data in PDF files.

Each PDF is transformed into a **structured feature vector**, capturing anomalies introduced by steganographic techniques such as metadata manipulation, invisible text insertion, and structural tampering.

---

## 🧩 Feature Categories

Features are grouped into six major categories:

1. Structural Features
2. Metadata Features
3. Steganographic Indicators
4. Text Behavior Features
5. Image-Based Features
6. Complexity & Distribution Metrics

---

## 📁 1. Structural Features

### `file_size`

* Total size of the PDF file (in KB/MB)
* 📌 Larger sizes may indicate embedded payloads

---

### `page_count`

* Number of pages in the document
* 📌 Helps normalize other features

---

### `object_count`

* Total number of PDF objects
* 📌 Stego PDFs often contain extra objects

---

### `avg_objects_per_page`

* Object density per page
* 📌 Abnormally high → injected content

---

### `orphan_object_depth`

* Objects not referenced in main structure
* 📌 Strong indicator of hidden payload storage

---

### `structural_complexity_score`

* Composite measure of PDF structure complexity
* 📌 Higher values → suspicious manipulation

---

## 🧾 2. Metadata Features

### `metadata_length`

* Length of metadata fields
* 📌 Payload often injected here

---

### `metadata_key_count`

* Number of metadata keys
* 📌 Unusual increase → manipulation

---

### `metadata_value_entropy`

* Entropy of metadata values
* 📌 High entropy → encoded/hidden data

---

## 🔐 3. Steganographic Indicators

### `zero_width_unicode_density`

* Density of invisible Unicode characters (ZWSP, ZWNJ, ZWJ)
* 📌 Direct indicator of covert embedding

---

### `invisible_text_ratio`

* Ratio of invisible/hidden text
* 📌 Used in white-text attacks

---

### `comment_length_ratio`

* Length of comments vs total content
* 📌 Payload hidden in comments

---

### `padding_byte_ratio`

* Extra bytes added in streams
* 📌 Detects junk/padding injection

---

## ✍️ 4. Text Behavior Features

### `avg_char_spacing_deviation`

* Variation in character spacing
* 📌 Used in spacing-based encoding

---

### `whitespace_run_variance`

* Variability in whitespace sequences
* 📌 Hidden patterns in spacing

---

### `text_to_nontext_ratio`

* Ratio of text vs non-text content
* 📌 Imbalance may indicate manipulation

---

## 🖼️ 5. Image-Based Features

### `image_count`

* Number of images in PDF
* 📌 More images → possible payload carriers

---

### `image_entropy_delta`

* Entropy difference in images
* 📌 LSB steganography alters entropy

---

### `image_size_anomaly`

* Deviation in image size patterns
* 📌 Abnormal size → hidden data

---

## 📊 6. Distribution & Complexity

### `page_object_distribution_entropy`

* Distribution randomness of objects across pages
* 📌 High entropy → unnatural structure

---

### `xref_gap_score`

* Irregularities in cross-reference table
* 📌 Broken structure = manipulation

---

## 🧠 Feature Importance (Intuition)

Most impactful features for detection:

* `metadata_value_entropy`
* `padding_byte_ratio`
* `xref_gap_score`
* `zero_width_unicode_density`
* `structural_complexity_score`

These features directly correlate with **steganographic artifacts**.

---

## ⚙️ Feature Engineering Strategy

The system follows a **forensic-first approach**:

1. Extract raw PDF structure
2. Compute statistical + entropy-based metrics
3. Detect anomalies in:

   * structure
   * metadata
   * text patterns
   * embedded objects
4. Convert into ML-ready feature vector

---

## 🚀 Why These Features Work

Steganography introduces:

* Redundancy
* Structural imbalance
* Statistical irregularities

These features capture those changes, enabling models like:

* Random Forest
* XGBoost
* LightGBM

to distinguish **Clean vs Stego PDFs** effectively.

---

## 🔮 Future Enhancements

* Byte-level sequence modeling
* Graph-based PDF structure analysis
* Deep learning feature extraction
* Transformer-based anomaly detection

---

## 🧠 Final Note

Feature engineering is the **core strength** of StegoAI.
Rather than relying on raw data, the system leverages **domain-specific forensic signals** to achieve robust and scalable steganalysis.

---
