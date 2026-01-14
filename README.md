## Project Overview

The project performs the following tasks:

- Counts the number of public washrooms in each park
- Calculates washroom density per hectare and per square meter
- Identifies parks with no washrooms
- Visualizes parks, transit lines, stations, and washrooms on a map
- Generates bar plots of top parks by washroom count
- Exports results to CSV and GeoJSON for reporting

**Tools Used:** Python, GeoPandas, Matplotlib, Contextily

---

## Files in this Repository

### **Code**
- `script.py` – The main Python script that performs the analysis, generates maps and plots, and exports results.

### **Data**
All GeoJSON files used for the analysis:

- `data/local-area-boundary.geojson` – Boundary of the local Vancouver area
- `data/parks-polygon-representation.geojson` – Polygon representation of parks
- `data/public-washrooms.geojson` – Point data for public washrooms
- `data/rapid-transit-lines.geojson` – Rapid transit lines in Vancouver
- `data/rapid-transit-stations.geojson` – Skytrain station locations

### **Outputs**
- `vancouver_map.png` – Final map showing parks, transit lines, stations, and public washrooms
- `parks_washroom_analysis_m2.csv` – Table with each park’s name, area (m²), washroom count, and density (pw/m²)
- `parks_with_no_washrooms.geojson` – GeoJSON file containing parks that have no public washrooms

---


