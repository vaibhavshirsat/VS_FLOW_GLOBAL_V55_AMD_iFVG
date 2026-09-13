# VS FLOW GLOBAL V55 — AMD + iFVG

Base: existing VS FLOW GLOBAL V55 architecture.
Additive module: AMD + iFVG Global Scanner.

## Included
- Global assets / indices / crypto / FX / commodities / rates
- Existing VS FLOW V55 modules preserved
- AMD + iFVG scanner
- Multi-timeframe AMD+iFVG sequence: HTF Bias → AMD → Sweep → MSS/BOS → Displacement → iFVG → Retest

## Run locally (Windows)
```bat
python -m pip install -r requirements.txt
python -m streamlit run VS_FLOW_GLOBAL_V55_AMD_iFVG.py
```

Optional logo: place the existing `vs_flow_logo.png` beside the Python file.
