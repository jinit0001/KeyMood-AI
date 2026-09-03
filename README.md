# Deep Emotion Detector

A Streamlit app that detects emotions in plain text and TXT, PDF, and DOCX files. It uses the public [`j-hartmann/emotion-english-distilroberta-base`](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base) model through Hugging Face Transformers.

## Requirements

- Python 3.10 or newer
- Internet access on the first run, so Hugging Face can download the model (about 330 MB)
- Windows, macOS, or Linux

## Install and Run

Open PowerShell, Command Prompt, or a terminal in the project directory.

### Windows with Conda

```powershell
conda create -n emotion-detector python=3.10 -y
conda activate emotion-detector
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app.py
```

### Windows with a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, run this once in PowerShell as an administrator:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) after Streamlit starts.

## First Run and Model Download

The model is public and does not require a Hugging Face token. The first text prediction downloads the model automatically and later runs use the local Hugging Face cache.

To download and test the model before starting the app:

```powershell
python -c "from transformers import pipeline; model = pipeline('sentiment-analysis', model='j-hartmann/emotion-english-distilroberta-base'); print(model('I am very happy today.'))"
```

If you see an authentication error, confirm that the code uses `j-hartmann/emotion-english-distilroberta-base`, not the restricted `arpanghoshal/EmoRoBERTa` model.

## Use the App

1. Choose `Plain text` or `Documents` in the sidebar.
2. Enter text or upload a TXT, PDF, or DOCX file.
3. Select `Find emotion`.
4. For TXT files, the processed text is saved in the `downloads` directory.

To allow uploads up to 1 GB:

```powershell
streamlit run app.py --server.maxUploadSize=1028
```

## Troubleshooting

Check that the correct environment is active:

```powershell
where python
python -c "import sys; print(sys.executable)"
```

Repair or update the installed packages:

```powershell
python -m pip install --upgrade --force-reinstall -r requirements.txt
python -m pip check
```

If port 8501 is already in use, start on another port:

```powershell
streamlit run app.py --server.port=8502
```

## Docker

The repository currently contains an empty `Dockerfile`, so Docker cannot build this app until that file is configured. The local Python instructions above are the supported way to run it.

For hosted deployment, the existing `Procfile` starts the app with `streamlit run app.py` after running `setup.sh`.
