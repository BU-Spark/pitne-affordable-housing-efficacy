#!/bin/bash
# Helper script to run the data pipeline with proper PYTHONPATH

set -e  # Exit on error

echo "=== Running Data Pipeline ==="

echo "Step 1: Pulling data from Google Drive..."
PYTHONPATH=. python scripts/04_pull_all.py

echo ""
echo "Step 2: Cleaning application data..."
PYTHONPATH=. python scripts/06_clean_applications_pipeline.py

echo ""
echo "Step 3: Generating static visualizations (charts, graphs, trait analysis)..."
python scripts/popularity_graph_generation.py --input data/processed/applications_clean.parquet --outdir visuals

echo ""
echo "Step 4: Generating age-restricted property analysis..."
python scripts/age_analysis.py --input data/processed/applications_clean.parquet --outdir "visuals/Age Restricted Analysis"

echo ""
echo "Step 5: Generating enhanced interactive map..."
python scripts/folium_map_generation.py --input data/processed/applications_clean.parquet --outdir visuals

echo ""
echo "=== Pipeline Complete! ==="
echo ""
echo "Generated outputs:"
echo "  - Cleaned data: data/processed/applications_clean.parquet"
echo "  - Interactive map: visuals/applications_map_enhanced.html"
echo "  - Static charts: visuals/*.png"
echo "  - Age analysis: visuals/Age Restricted Analysis/*.png"
echo "  - Analysis CSVs: visuals/*.csv"
echo ""
echo "Open visuals/applications_map_enhanced.html in your browser to explore the interactive map!"
