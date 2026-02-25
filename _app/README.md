# Private Cloud ROI & TCO Calculator

Built by Insight — a consultative tool for evaluating private cloud platforms and generating customer proposals.

## Quick Start (Docker — Recommended)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

### Launch
```bash
./launch.sh
```
The app will open automatically at http://localhost:8501

### Stop
```bash
docker-compose down
```

---

## Manual Setup (Development)

### Prerequisites
- Python 3.11+
- pip

### Install
```bash
pip install -r requirements.txt
```

### Run
```bash
streamlit run app.py
```

---

## How to Use

1. **Customer Manager** — Create or load a customer session
2. **Environment Analysis** — Upload RVTools or LiveOptics export
3. **Discovery Questionnaire** — Answer strategic direction questions
4. **VMware Renewal Analyzer** — Enter renewal details to calculate urgency
5. **Current State TCO** — Review and adjust cost assumptions
6. **Scenario Builder** — Enter vendor quotes and compare platforms
7. **Comparison & Recommendation** — Review recommendation and roadmap
8. **Export & Proposal** — Generate PDF proposal and Excel model

---

## Sample Data
- `sample_rvtools.xlsx` — Sample RVTools export (150 VMs)
- `sample_liveoptics.xlsx` — Sample LiveOptics export (150 VMs)

---

## Support
Contact the Hybrid Cloud COE for questions or enhancements.
```
