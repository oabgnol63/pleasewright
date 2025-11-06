# pleasewright
git pull https://github.com/oabgnol63/pleasewright.git folder

# Prerun:
cd folder
python -m venv .env
.env/Scripts/Activate
pip install -r requirements.txt

# To run test_w1.py:
pytest -s -v test_w1.py -n 2

# To run test_w2.py: (api test)
pytest test_w2.py -sv -n 4 --log-cli-level=INFO

# To run test_w2_2.py: (tags test)
pytest test_w2_2.py -sv --log-cli-level=INFO -m smoke/regression
trace: playwright show-trace trace.zip
video: pytest test_w2_2.py -sv --log-cli-level=INFO -m smoke/regression --record-video on/failure --slow 500
dataset: pytest test_w2_2.py -sv --log-cli-level=INFO -k "test_multi_login"
auth: pytest test_w2_2.py -sv --log-cli-level=INFO -k "test_http_auth"