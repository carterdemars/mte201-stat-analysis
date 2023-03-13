# MTE201: Statistical Analysis Course Project
## Variable Resistor Measurement Dashboard

To install all of the required packages to this environment, simply run:

```
pip install -r requirements.txt
```

Run this app locally:
```
python app.py
```
Open http://0.0.0.0:8050/ in your browser, you will see a live-updating dashboard.

# Background Info
Resistance (and therefore voltage at a constant current) varies linearly with wire length. The applications takes live voltage readings from an Arduino microcontroller and converts them to distance readings. The tool was calibrated to measure distances between 0 and 15cm. 
