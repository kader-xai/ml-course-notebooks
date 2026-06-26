# ML Course Notebooks

Runnable Google Colab notebooks accompanying my video courses.

| Course | Episodes | Open in Colab |
|---|---|---|
| **Machine Learning with scikit-learn** — Linear Regression → Stacking | 14 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kader-xai/ml-course-notebooks/blob/main/scikit_learn_course.ipynb) |
| **PyTorch From Scratch: Build Your Own GPT** — one tensor → a tiny GPT | 19 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kader-xai/ml-course-notebooks/blob/main/pytorch_course.ipynb) |
| **Practical Machine Learning with TensorFlow** — NLP & Transformers | 28 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kader-xai/ml-course-notebooks/blob/main/tensorflow_course.ipynb) |
| **Hugging Face, Hands-On** — `pipeline()` → fine-tune → quantize → ship | 20 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kader-xai/ml-course-notebooks/blob/main/hugging_face_course.ipynb) |
| **How Neural Networks Actually Learn** — gradients → Adam → schedules → BatchNorm | 18 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kader-xai/ml-course-notebooks/blob/main/optimization_course.ipynb) |
| **XGBoost for Cyber Defense** — phishing · malware · IDS · DLP · UEBA · SHAP · SOC | 18 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kader-xai/ml-course-notebooks/blob/main/xgboost_security_course.ipynb) |

Click a badge to launch the notebook in Colab — no setup, runs in the browser.

- **scikit-learn**: every cell is self-contained and runs as-is (scikit-learn ships with Colab).
- **PyTorch**: PT01–PT14 run standalone; the GPT build (PT15–PT19) is shown modular as in the videos, and the final cell consolidates it into one runnable tiny char-GPT you can train and sample.
- **TensorFlow**: one cell per episode following Collect → Preprocess → Build → Train → Evaluate → Save → Deploy → Predict, with a deep NLP / Transformer track (TF11–TF20).
- **Hugging Face**: each `HF##` section is self-contained — run its `pip install` cell, then the cells below. Quantization (HF09) and Diffusers (HF15) want a GPU runtime (*Runtime → Change runtime type → GPU*).
- **Optimization**: each `OP##` section is the video's Act-2 walkthrough — the real computation behind that episode's figure. Most are self-contained NumPy demos; OP16/OP18 use PyTorch and are faithful skeletons. Run the install cell first.
- **XGBoost for Cyber Defense**: every `SEC##` section was executed and its printed output captured verbatim — the code reproduces the real metrics/figures. Seeded in-code security datasets (no downloads); security-honest metrics (PR-AUC, precision, recall, FPR @ threshold). Run the install cell, then any section top-to-bottom. Episode thumbnails: [`thumbnails/xgboost_security/`](thumbnails/xgboost_security/).

