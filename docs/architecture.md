# System Architecture

The StegAnalysis framework follows a modular pipeline:

### 1. Input Layer

* Accepts PDF files for analysis

### 2. Preprocessing

* File parsing
* Metadata extraction
* Structure normalization

### 3. Feature Extraction

* Byte-level patterns
* Entropy analysis
* Object structure anomalies

### 4. Detection Engine

* Machine learning models
* Anomaly detection

### 5. Output Layer

* Classification result (Cover / Stego)
* Detection confidence score

This modular design ensures scalability for future multi-format support.
