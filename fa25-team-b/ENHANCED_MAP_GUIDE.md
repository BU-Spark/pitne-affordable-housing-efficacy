# 🗺️ Enhanced Geospatial Analysis Map - User Guide

## Overview

The enhanced property popularity analysis (V3) provides comprehensive geospatial visualization of CHAPA affordable housing applications with advanced features for exploring demographic patterns, prices, and applicant behaviors.

---

## 🚀 How to Run

```bash
# Make sure property geocoding is complete first
python scripts/geocode_properties_for_map.py

# Run the enhanced analysis
python scripts/analyze_property_popularityV3.py \
  --input data/processed/applications_clean.parquet \
  --outdir visuals
```

**Outputs:**
- `visuals/applications_map_enhanced.html` — Interactive map (open in browser)
- `visuals/property_demand_with_geo.csv` — Property-level data with coordinates
- `visuals/*.png` — Static charts (bar, pareto, price analysis, etc.)

---

## 🎯 Key Features

### 1. **Accurate Property Locations**
**What changed from V2:**
- ❌ V2: Used median applicant coordinates (where applicants live)
- ✅ V3: Uses geocoded property coordinates (where properties actually are)

**Impact:** Map now shows true property locations in Massachusetts!

---

### 2. **8 Demographic Heatmaps**

Each race category has its own toggleable heatmap:

| Layer | Color | Description |
|-------|-------|-------------|
| Asian | Amber | Applicant concentration (Asian) |
| Black/African American | Teal | Applicant concentration (Black/African American) |
| Hispanic/Latine | Violet | Applicant concentration (Hispanic/Latine) |
| White | Blue | Applicant concentration (White) |
| Native American/Alaskan Native | Red | Applicant concentration (Native American) |
| White (MENA) | Cyan | Applicant concentration (White - Middle East/North Africa) |
| Prefer not to say | Gray | Applicants who chose not to answer |
| Unknown | Slate | Unknown demographic data |

**How to use:**
1. Open Layer Control (top-right)
2. Check/uncheck demographic heatmaps
3. Overlay multiple heatmaps to compare patterns

**Heatmap weighting:** `demographic_share × application_count`
(Shows both concentration AND volume)

---

### 3. **Price Heatmap**

**Visual gradient:**
- 🟢 Green → Low-priced properties
- 🟡 Yellow → Mid-range
- 🟠 Orange → Higher-priced
- 🔴 Red → Highest-priced

**Use cases:**
- Identify price clustering patterns
- Find low-cost property concentration areas
- Compare price vs. demand geographically

---

### 4. **Overall Demand Heatmap**

Shows total application concentration regardless of demographics or price.

**Use cases:**
- Identify high-demand geographic areas
- Spot regional imbalances
- Guide future development locations

---

### 5. **Applicant Origins Layer**

Blue circle markers show where applicants are coming from (aggregated by city).

**Marker size:** Proportional to number of applicants from that location

**How to use:**
1. Toggle "Applicant Origins" in Layer Control
2. View alongside property markers to see:
   - How far applicants travel
   - Geographic mismatch between supply and demand
   - Potential underserved areas

---

### 6. **Distance Metrics**

Every property popup shows:
- **Median distance:** Typical travel distance for applicants
- **Average distance:** Mean travel distance
- **Distance range:** Min–Max distance traveled

**Calculated using:** Haversine formula (accurate great-circle distance in miles)

**Insights:**
- Properties with high median distance indicate regional gaps
- Low distance = local demand
- High variance = property attracts from diverse locations

---

### 7. **🔍 Interactive Filtering Panel**

Located in top-right corner.

#### **Filters Available:**

**Applications Filter**
- Range: 0–100+ applications
- Purpose: Focus on high-demand or low-demand properties

**Price Filter**
- Range: $0–$500K+
- Purpose: Analyze affordability tiers

**Distance Filter**
- Range: 0–100+ miles
- Purpose: Find properties with local vs. regional appeal

#### **How to Use:**
1. Adjust sliders to set criteria
2. Click "Apply Filters"
3. See count of matching properties
4. Click "Reset" to clear all filters

**Note:** Current implementation shows filter results count. Full dynamic marker filtering would require map refresh (future enhancement).

---

### 8. **Property Search**

**Location:** Top of map (search icon)

**How to use:**
1. Type property name (e.g., "Groton")
2. Select from dropdown
3. Map auto-zooms to property
4. Click marker for full details

---

### 9. **Enhanced Popups**

Each property marker shows:

**Property Info:**
- Name
- Total applications (highlighted in teal)
- Maximum resale price

**Distance Stats:**
- Median applicant distance
- Average distance
- Distance range

**Demographics Table:**
- All race categories with % breakdown
- Color-coded dots matching heatmap colors
- Only shows categories with >0% representation

---

## 🎮 Map Controls

### Standard Controls

| Control | Location | Purpose |
|---------|----------|---------|
| **Layer Control** | Top-right | Toggle heatmaps, markers, layers |
| **MiniMap** | Bottom-left | Overview navigator |
| **Fullscreen** | Top-left | Expand to full screen |
| **Measure Tool** | Top-left | Measure distances in miles |
| **Locate** | Top-left | Find your current location |
| **Search** | Top | Search for properties |
| **Filter Panel** | Top-right | Filter by apps/price/distance |

### Zoom & Pan
- **Scroll wheel:** Zoom in/out
- **Click + drag:** Pan the map
- **Double-click:** Zoom in
- **Shift + drag:** Zoom to area

---

## 📊 Data Quality

### Geocoding Success Rate
- **109/113 properties geocoded (96.5%)**
- Failed properties (4):
  - None (null value)
  - '6 Safford Street, 3' (incomplete address)
  - '1301 Albion Road - Second time' (ambiguous)
  - '63 Central St., 101' (incomplete)

### Distance Calculations
- **1,730/1,740 applications** have valid applicant coordinates (99.4%)
- Median distance across all properties: **12.3 miles**
- Average distance: **19.2 miles**

---

## 🎨 Visual Design

### Color Scheme

**Demand/Applications:**
- Warm gradient: Yellow → Amber → Orange → Dark Orange

**Price:**
- Cool-to-warm: Green → Yellow → Orange → Red

**Demographics:**
- Each race has distinct, accessible color
- Colors match stacked bar chart for consistency

**Applicant Origins:**
- Cool blue gradient (distinguishes from properties)

---

## 💡 Analysis Workflows

### Workflow 1: Find High-Demand, Low-Price Properties
1. Enable "Price Heatmap" (toggle ON)
2. Enable "Overall Demand Heatmap" (toggle ON)
3. Look for areas with:
   - High demand intensity (dark orange/red)
   - Low price intensity (green/yellow)

### Workflow 2: Identify Racial Concentration Patterns
1. Enable only Black/African American heatmap
2. Note concentration areas
3. Enable only Hispanic/Latine heatmap
4. Compare patterns
5. Repeat for other demographics

### Workflow 3: Analyze Applicant Travel Distance
1. Enable "Applicant Origins" layer
2. Select a property marker (e.g., top property)
3. Check distance stats in popup
4. Visually compare property location to applicant origin clusters

### Workflow 4: Find Underserved Regions
1. Enable "Applicant Origins" layer
2. Look for blue clusters (many applicants)
3. Toggle off to see property markers
4. Identify areas with many applicants but few nearby properties

---

## 🔧 Technical Details

### Performance Optimizations

1. **MarkerCluster:** Properties cluster at low zoom levels
2. **Lazy heatmaps:** Only render when toggled on
3. **LinearColormap:** Faster than step-based colormaps
4. **Pre-aggregated data:** Demographics calculated once
5. **Efficient popups:** Minimal DOM elements

### File Sizes
- Enhanced map: ~584 KB (vs. 278 KB for V2)
- Includes all property data for filtering
- Loads instantly on modern browsers

### Browser Compatibility
- ✅ Chrome, Firefox, Edge, Safari (latest)
- ✅ Mobile browsers (responsive controls)
- ❌ IE11 (not supported)

---

## 🐛 Known Limitations

1. **Filter panel:** Shows matching count but doesn't hide markers dynamically
   - **Workaround:** Note filtered property names and search manually
   - **Future:** Implement dynamic marker toggling

2. **No bedroom data:** Dataset lacks bedroom counts
   - **Future:** Add when data becomes available

3. **Applicant flow lines:** Not yet implemented
   - **Future:** Add Polylines from origin cities to properties

4. **Large clusters:** High-demand areas show large cluster numbers
   - **Workaround:** Zoom in to expand clusters

---

## 📈 Future Enhancements

### Planned Features
- [ ] Dynamic marker filtering (hide/show based on filters)
- [ ] Flow lines from applicant origins to properties
- [ ] Bedroom heatmap (when data available)
- [ ] Export filtered property list to CSV
- [ ] Time-series animation (if submission dates added)
- [ ] Custom demographic combinations filter
- [ ] Distance bands visualization (concentric circles)

---

## 🆘 Troubleshooting

### Map doesn't load
- **Check:** Browser console for errors (F12)
- **Fix:** Ensure `applications_map_enhanced.html` is in `visuals/`

### No properties showing
- **Check:** Layer Control — ensure "Properties (clustered)" is ON
- **Fix:** Toggle layer off and on

### Heatmaps look wrong
- **Check:** Multiple heatmaps overlapping
- **Fix:** Toggle off all heatmaps except one to see each clearly

### Popups are cut off
- **Fix:** Click popup, it will auto-reposition

### Geocoding failed for many properties
- **Check:** Internet connection during geocoding
- **Re-run:** `python scripts/geocode_properties_for_map.py`

---

## 📚 Related Files

- `scripts/analyze_property_popularityV3.py` — Main analysis script
- `scripts/geocode_properties_for_map.py` — Property geocoding
- `cleaners/applicant_property_geocoding.py` — Geocoding logic
- `data/cache/property_coordinates.parquet` — Cached coordinates
- `visuals/property_demand_with_geo.csv` — Property data export

---

## 🙏 Acknowledgments

Built on:
- **Folium** (interactive maps)
- **OpenStreetMap** (base tiles)
- **Nominatim** (geocoding)
- **Leaflet.js** (mapping library)

---

## 📝 Changelog

### V3 (Current)
- ✅ Fixed property coordinates bug (now uses actual property locations)
- ✅ Added 8 demographic heatmaps
- ✅ Added price heatmap
- ✅ Added applicant origins layer
- ✅ Added distance calculations (median/avg/min/max)
- ✅ Added search functionality
- ✅ Added filter panel (price/apps/distance)
- ✅ Enhanced popups with demographics + distance
- ✅ Performance optimizations

### V2 (Previous)
- Bar charts, pareto, price analysis
- Basic folium map (with incorrect coordinates)
- Single demographic layer (≥30% Black)
- Basic heatmap

---

**Questions or issues?** Contact the team or file an issue in the project repo.
