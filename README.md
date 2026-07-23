# AI CCTV Surveillance System

## Setup
1. `pip install -r requirements.txt` (or install packages listed in main.py/detector imports)
2. Run `python export_model.py` once to generate the OpenVINO model folder
3. Start Django: `cd cctv_backend && python manage.py runserver 0.0.0.0:8000`
4. Start detector: `python main.py`