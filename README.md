# pleasewright
git pull https://github.com/oabgnol63/pleasewright.git folder

# Prerun:
cd folder
python -m venv .env
.env/Scripts/Activate
pip install -r requirements.txt

# To run test_w1.py:
pytest -s -v test_w1.py -n 2

# To run test_w2.py:
pytest test_w2.py -s -v -n 4 --log-cli-level=INFO