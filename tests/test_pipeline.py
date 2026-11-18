import json
from pathlib import Path
import joblib
import pandas as pd


def test_metrics_are_sane():
    m = json.loads(Path('artifacts/metrics.json').read_text())
    assert m['student_id'] == 'FA23-BDS-007'
    assert m['training_rows'] >= 100
    assert 0.5 <= m['accuracy'] <= 1.0


def test_model_predicts():
    bundle = joblib.load('artifacts/model.joblib')
    row = pd.DataFrame([{f: 0.0 for f in bundle['features']}])
    p = bundle['model'].predict_proba(row)[:, 1]
    assert 0.0 <= p[0] <= 1.0