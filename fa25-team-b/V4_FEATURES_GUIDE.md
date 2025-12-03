# 🗺️ V4 Enhanced Map - Advanced Geospatial Visualizations

## 🎉 **What's New in V4**

V4 replaces the **8 overlapping demographic heatmaps** with **4 powerful new visualizations** that provide clearer, more actionable insights:

---

## ✨ **New Features**

### 1. **🥧 Pie Chart Markers**

**What it is:**
- Each property is represented by a **mini pie chart** showing demographic composition
- Marker size scales with application count
- Hover shows property name and application count
- Click for full details

**What it shows:**
- Exact demographic breakdown at each property
- Visual patterns of concentration
- Which properties attract diverse vs. homogeneous applicants

**How to use:**
- Zoom in to see individual pie charts clearly
- Larger markers = more applications
- Color segments match the demographic legend

**Advantages over heatmaps:**
- ✅ No overlay confusion
- ✅ See exact proportions at a glance
- ✅ Clearer geographic patterns
- ✅ Easier to identify specific properties

---

### 2. **🔀 Flow Lines**

**What it is:**
- Curved blue lines connecting **applicant origin cities** to **properties**
- Line thickness = number of applicants traveling that route
- Line opacity = connection strength

**What it shows:**
- **Movement patterns:** Where applicants are traveling from
- **Regional attraction:** Which properties draw from wider areas
- **Catchment zones:** Geographic reach of each property
- **Travel corridors:** Major application flow routes

**How to use:**
- Toggle "Applicant Flow Lines" layer in Layer Control (top-right)
- Look for thick lines = major routes
- Follow lines from clusters of origins to properties
- Identify properties with mostly local vs. distant applicants

**Key insights:**
- Properties with many flow lines = regional appeal
- Thick lines = well-established routes
- Long lines = applicants willing to relocate further
- Line clusters = popular origin-destination pairs

**Note:** Only shows flows with ≥3 applicants to reduce clutter

---

### 3. **📊 Diversity Index Heatmap**

**What it is:**
- Heatmap showing **demographic diversity** at each property
- Uses **Shannon Diversity Index** (0 = homogeneous, 1 = perfectly diverse)
- Color gradient: Red (low) → Yellow (medium) → Green (high)

**What it shows:**
- Which properties have balanced vs. skewed applicant demographics
- Geographic patterns of diversity
- Properties that attract broad vs. narrow demographics

**How to use:**
- Toggle "Diversity Index Heatmap" in Layer Control
- Look for green zones = high diversity properties
- Red zones = properties with homogeneous applicant pools
- Compare with flow lines to see diversity vs. geography

**Interpreting the index:**
- **0.0 - 0.3** (Red): Predominantly one demographic group
- **0.4 - 0.6** (Yellow): Mixed, with one or two dominant groups
- **0.7 - 1.0** (Green): Highly diverse, balanced representation

**Why it's useful:**
- Identifies potential access barriers
- Shows where outreach may be uneven
- Reveals properties successfully attracting diverse applicants

---

### 4. **🗾 Choropleth Map**

**What it is:**
- Shaded **Massachusetts town/county boundaries**
- Color intensity = number of applicants from that area
- Darker = more applicants originating from that location

**What it shows:**
- Regional demand patterns
- Which cities/counties generate most applications
- Geographic distribution of applicant pool
- Underserved vs. saturated regions

**How to use:**
- Toggle "Applicants by Town" in Layer Control
- Hover over regions to see applicant counts
- Compare shaded regions with property locations
- Identify mismatches between demand and supply

**Key insights:**
- Dark regions with few properties = underserved areas
- Light regions with many properties = potential oversupply
- Regional imbalances between applicants and available housing
- Identifies where new developments might be needed

**Note:** Currently uses county-level data. Can be enhanced with town-level GeoJSON for finer detail.

---

## 🔧 **Retained from V3**

**Price Heatmap** (unchanged)
- Shows property price concentration
- Green (low) → Red (high)

**Enhanced Popups** (improved)
- Now shows diversity index
- Still includes: applications, price, distance stats, demographics

**Interactive Controls** (unchanged)
- Search, MiniMap, Fullscreen, Measure, Locate

---

## 📊 **Technical Specs**

| Feature | Details |
|---------|---------|
| **File size** | 395 KB (35% smaller than V3!) |
| **Pie charts** | 109 properties visualized |
| **Flow lines** | 125 significant connections shown |
| **Diversity calculation** | Shannon Entropy Index (normalized 0-1) |
| **Choropleth** | MA counties (upgradeable to towns) |
| **Performance** | Faster rendering than V3 |

---

## 🎮 **How to Use the V4 Map**

### **Opening the Map**
```bash
open visuals/applications_map_v4_enhanced.html
# or double-click the file
```

### **Workflow 1: Understand Movement Patterns**
1. Enable "Applicant Flow Lines" layer
2. Zoom to a region of interest
3. Follow lines from origins to properties
4. Identify major travel corridors
5. Note properties with mostly local vs. distant flows

### **Workflow 2: Analyze Diversity**
1. Enable "Diversity Index Heatmap"
2. Look for green (diverse) vs. red (homogeneous) zones
3. Click pie chart markers to see exact breakdowns
4. Compare diversity with geographic location
5. Identify patterns: Are diverse properties in specific areas?

### **Workflow 3: Regional Supply/Demand Analysis**
1. Enable "Applicants by Town" choropleth
2. Note dark-shaded regions (high applicant count)
3. Look at property locations (pie charts)
4. Identify mismatches:
   - Dark region, few properties = underserved
   - Light region, many properties = potential oversupply

### **Workflow 4: Individual Property Deep Dive**
1. Zoom to a specific property
2. Examine pie chart (demographic mix)
3. Check popup for diversity index + distance
4. Enable flow lines to see where applicants come from
5. Check choropleth to understand regional context

---

## 📈 **Key Insights You Can Now See**

### **Demographic Patterns**
- Properties with balanced (green) vs. concentrated (red) diversity
- Geographic clustering of similar demographic patterns
- Specific properties attracting diverse applicants

### **Movement Dynamics**
- Major applicant flow corridors
- Properties serving primarily local vs. regional populations
- Travel distance patterns (short vs. long commutes)
- Origin cities with highest application volumes

### **Regional Imbalances**
- Areas with high applicant demand but few properties
- Regions with many properties but low applicant concentration
- Geographic gaps in affordable housing supply

### **Accessibility Patterns**
- Which properties attract the widest geographic reach
- Regional clustering of applicant origins
- Barriers to access (indicated by low diversity or few flows)

---

## 🆚 **V3 vs V4 Comparison**

| Feature | V3 | V4 |
|---------|----|----|
| **Demographic viz** | 8 overlapping heatmaps | Pie chart markers |
| **Clarity** | Fuzzy, hard to read | Clear, precise |
| **Movement patterns** | None | Flow lines |
| **Diversity analysis** | Manual inspection | Diversity index |
| **Regional context** | None | Choropleth map |
| **File size** | 609 KB | 395 KB ✅ |
| **Render speed** | Slower | Faster ✅ |
| **Insights** | Limited | Comprehensive ✅ |

**Bottom line:** V4 is clearer, faster, and more insightful!

---

## 🔮 **Future Enhancements**

### **Easy Additions:**
- [ ] Animated flow lines (using AntPath plugin)
- [ ] Town-level choropleth (needs proper MA towns GeoJSON)
- [ ] Filter flow lines by demographic
- [ ] Color code flow lines by distance
- [ ] Add applicant origin markers with demographic pies

### **Advanced Features:**
- [ ] Isochrone maps (travel time zones)
- [ ] Voronoi diagrams (property catchment areas)
- [ ] Time-series animation (if submission dates added)
- [ ] 3D visualization (property height = applications)
- [ ] Network graph analysis of flows

---

## 🐛 **Known Limitations**

1. **Choropleth granularity:** Uses county-level data
   - **Solution:** Add proper MA towns GeoJSON file
   - **Impact:** Low - still shows regional patterns

2. **Flow line clutter:** Only shows flows ≥3 applicants
   - **Why:** Too many lines makes map unreadable
   - **Workaround:** Lower threshold if desired (edit script)

3. **Pie chart size:** Very small for low-application properties
   - **Why:** Size scales with application count
   - **Workaround:** Zoom in to see details

4. **Mobile performance:** May be slow on old devices
   - **Why:** Complex visualizations
   - **Solution:** Use desktop for best experience

---

## 💡 **Interpretation Tips**

### **Reading Pie Charts:**
- **Solid color:** Homogeneous applicant pool
- **Many colors:** Diverse mix
- **Size matters:** Larger = more popular
- **Zoom level:** Zoom in to see small properties

### **Reading Flow Lines:**
- **Thick lines:** Major routes, many applicants
- **Thin lines:** Smaller flows
- **Long lines:** Applicants traveling far
- **Short lines:** Local demand
- **Converging lines:** Regional hub properties

### **Reading Diversity Heatmap:**
- **Green clusters:** Areas attracting diverse applicants
- **Red clusters:** Homogeneous regions
- **Gradual transitions:** Natural geographic patterns
- **Sharp boundaries:** Potential policy/access barriers

### **Reading Choropleth:**
- **Dark towns:** High applicant generation
- **Light towns:** Low applicant origination
- **Compare with properties:** Supply/demand balance

---

## 🚀 **How to Regenerate V4 Map**

```bash
# If data updates:
PYTHONPATH=. python scripts/04_pull_all.py
PYTHONPATH=. python scripts/06_clean_applications_pipeline.py

# Generate V4 map:
python scripts/analyze_property_popularityV4.py \
  --input data/processed/applications_clean.parquet \
  --outdir visuals

# Open:
open visuals/applications_map_v4_enhanced.html
```

---

## 📚 **Formulas & Calculations**

### **Shannon Diversity Index**
```
H = -Σ(p_i × ln(p_i))

where:
  p_i = proportion of demographic category i
  H = raw entropy (0 to ln(n))

Normalized: H / ln(n) to scale 0-1
```

**Example:**
- Property with 50% White, 50% Black: H ≈ 1.0 (max diversity)
- Property with 90% White, 10% Black: H ≈ 0.47 (low diversity)
- Property with 100% White: H = 0.0 (no diversity)

### **Flow Line Threshold**
```
flow_count ≥ 3 applicants

Why 3? Balances:
  - Showing meaningful patterns
  - Avoiding visual clutter
  - Including local connections
```

---

## 🎯 **Best Practices**

1. **Start with layers OFF:** Enable one at a time to understand each
2. **Compare layers:** Toggle between choropleth and flow lines
3. **Zoom strategically:** Zoom out for regional patterns, in for details
4. **Use popups:** Click properties for exact numbers
5. **Legend reference:** Keep diversity index legend visible
6. **Screenshot insights:** Capture specific patterns for reports

---

## 📞 **Questions & Customization**

**Want to adjust thresholds?**
- Edit `scripts/analyze_property_popularityV4.py`
- Line ~430: `significant_flows = applicant_origins[applicant_origins["flow_count"] >= 3]`
- Change `>= 3` to different threshold

**Want different colors?**
- Diversity gradient: Line ~470
- Flow line color: Line ~444
- Pie chart colors: Already match DEMO_COLS

**Want town-level choropleth?**
- Download proper MA towns GeoJSON
- Place in `data/cache/ma_towns.geojson`
- Script will auto-use it

---

**V4 represents a major leap forward in geospatial analysis capabilities. The combination of pie charts, flow lines, diversity index, and choropleth provides a comprehensive understanding of affordable housing application patterns that wasn't possible with overlapping heatmaps.**

**Enjoy exploring your data! 🎉**
