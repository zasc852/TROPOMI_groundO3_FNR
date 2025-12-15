import os
import warnings
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib.colors as mcolors
import geopandas as gpd
import numpy as np
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from shapely.ops import unary_union
import shapely

warnings.filterwarnings("ignore", category=RuntimeWarning)

WORKDIR   = os.environ["WORKDIR"]
OUTDIR    = os.environ["OUTDIR"]
FONT_PATH = os.environ["FONT_PATH"]

O3_FILE      = os.environ["O3_FILE"]
TROPOMI_FILE = os.environ["TROPOMI_FILE"]

os.chdir(WORKDIR)

sub_outp_dir = os.path.join(OUTDIR, "SMA")
os.makedirs(sub_outp_dir, exist_ok=True)

font_manager.fontManager.addfont(FONT_PATH)
font_name = font_manager.FontProperties(fname=FONT_PATH).get_name()
plt.rcParams["font.family"] = font_name

merged_df_ozone = pd.read_csv(O3_FILE, encoding="utf-8")
merged_df = pd.read_csv(TROPOMI_FILE, encoding="utf-8")
FNR_threshold = pd.read_csv(os.path.join(OUTDIR, "SMA", "GEMS_FNR_Threshold_SMA.txt"), sep='\t',encoding="utf-8")

shpfile_path = os.path.join(WORKDIR, "DATA", "SHP")  
shp_file = "gadm41_KOR_1.shp"                        
shp_index =[10,15,7] 
scatter_size = 300


required_cols = {"Lower", "Upper"}
missing = required_cols - set(FNR_threshold.columns)
if missing:
    raise ValueError(f"Threshold file missing columns: {missing}\nColumns={FNR_threshold.columns.tolist()}")

max_value10p_values = float(FNR_threshold["Lower"].iloc[0]) 
max_value10m_values = float(FNR_threshold["Upper"].iloc[0])  
low_thr, high_thr = sorted([max_value10p_values, max_value10m_values])

merged_df_ozone['ozone'] = pd.to_numeric(merged_df_ozone['ozone'], errors='coerce')
merged_df_ozone['ozone'] = merged_df_ozone['ozone'].replace(-999.0, np.nan)
merged_df_ozone = merged_df_ozone.dropna(subset=['ozone'])

merged_df_ozone['O3_unit'] = merged_df_ozone['ozone'] * 1.96 * 1e3
merged_df_ozone = merged_df_ozone.dropna(subset=['O3_unit'])

merged_df = merged_df.dropna(subset=["HCHO", "NO2", "lon", "lat"])
merged_df["HCHO"] = pd.to_numeric(merged_df["HCHO"], errors="coerce")
merged_df["NO2"]  = pd.to_numeric(merged_df["NO2"], errors="coerce")
merged_df = merged_df.dropna(subset=["HCHO", "NO2"])
merged_df = merged_df[merged_df["NO2"] != 0]

merged_df["FNR"] = merged_df["HCHO"] / merged_df["NO2"]


shapefile_path = os.path.join(shpfile_path, shp_file)
gdf = gpd.read_file(shapefile_path)

polygon_1 = gdf.geometry.iloc[15]
polygon_2 = gdf.geometry.iloc[10]
polygon_3 = gdf.geometry.iloc[7]
combined_polygon = unary_union([polygon_1, polygon_2, polygon_3])

minx, miny, maxx, maxy = combined_polygon.bounds

mask_bbox = (
    (merged_df['lon'] >= minx) &
    (merged_df['lon'] <= maxx) &
    (merged_df['lat'] >= miny) &
    (merged_df['lat'] <= maxy)  
)
df_bbox = merged_df.loc[mask_bbox]
points = shapely.points(df_bbox['lon'].to_numpy(), df_bbox['lat'].to_numpy())
mask_within = shapely.contains(combined_polygon, points)  # ✅ combined_polygon 사용
merged_df11= df_bbox.loc[mask_within].copy()

merged_df_avg = merged_df11.groupby(["lon", "lat"], as_index=False)["FNR"].mean()
merged_df_avg["FNR"] = pd.to_numeric(merged_df_avg["FNR"], errors="coerce")
merged_df_avg = merged_df_avg.dropna(subset=["FNR"])



colors = ["darkorange", "yellow", "royalblue"] 
boundaries = [0, low_thr, high_thr, 13]
boundaries_ticks = [low_thr, high_thr]

cmap = mcolors.ListedColormap(colors)
norm = mcolors.BoundaryNorm(boundaries, cmap.N, clip=True)

shapefile_path = os.path.join(shpfile_path, shp_file)
if not os.path.exists(shapefile_path):
    raise FileNotFoundError(f"Shapefile not found: {shapefile_path}")

shapefile_data = gpd.read_file(shapefile_path)
if shapefile_data.crs is None:
    raise ValueError("The shapefile does not have a CRS defined.")

fig, ax = plt.subplots(
    figsize=(10, 10),
    subplot_kw={"projection": ccrs.PlateCarree()}
)

ax.set_xlim(126.0, 127.9)
ax.set_ylim(36.8, 38.4)

if shp_index is None:
    geoms = shapefile_data.geometry.values
else:
    geoms = [shapefile_data.geometry.iloc[i] for i in shp_index]

ax.add_geometries(
    geoms,
    crs=ccrs.PlateCarree(),
    facecolor="none",
    edgecolor="black",
    linewidth=1
)

ax.coastlines(resolution="10m", color="black", linewidth=1)

gl = ax.gridlines(
    crs=ccrs.PlateCarree(),
    draw_labels=True,
    linewidth=1,
    color="gray",
    alpha=0.5,
    linestyle="--"
)
gl.top_labels = False
gl.right_labels = False
gl.bottom_labels = True
gl.left_labels = True
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

sc_fnr = ax.scatter(
    merged_df_avg["lon"],
    merged_df_avg["lat"],
    c=merged_df_avg["FNR"],
    s=scatter_size,
    marker=",",
    cmap=cmap,
    norm=norm,
    transform=ccrs.PlateCarree()
)

cb_fnr = plt.colorbar(
    sc_fnr,
    ax=ax,
    orientation="horizontal",
    pad=0.05
)
cb_fnr.ax.tick_params(labelsize=15)
cb_fnr.set_ticks(boundaries_ticks)

cb_ax = cb_fnr.ax
if high_thr == 0.0:
    cb_ax.text(0.15, 0.45, "Transitional", fontsize=20,
               va="center", ha="left", transform=cb_ax.transAxes)
    cb_ax.text(0.65, 0.45, "NOx-limited", fontsize=20,
               va="center", ha="left", transform=cb_ax.transAxes)
else:
    cb_ax.text(0.07, 0.45, "VOC-limited", fontsize=20,
               va="center", ha="left", transform=cb_ax.transAxes)
    cb_ax.text(0.41, 0.45, "Transitional", fontsize=20,
               va="center", ha="left", transform=cb_ax.transAxes)
    cb_ax.text(0.75, 0.45, "NOx-limited", fontsize=20,
               va="center", ha="left", transform=cb_ax.transAxes)

df_mean_o3 = merged_df_ozone.groupby(
    ["lon", "lat"], as_index=False
).mean(numeric_only=True)

sc_o3 = ax.scatter(
    df_mean_o3["lon"],
    df_mean_o3["lat"],
    c=df_mean_o3["O3_unit"],
    s=150,
    marker="o",
    cmap="jet",
    vmin=85,
    vmax=120,
    edgecolor="black",
    transform=ccrs.PlateCarree(),
    zorder=3
)


cbar_ax_o3 = fig.add_axes([
    0.9,  
    0.265,  
    0.02,  
    0.615   
])
cb_o3 = plt.colorbar(
    sc_o3,
    cax=cbar_ax_o3,
    orientation="vertical"
)

cb_o3.set_label("O$_3$ ($\mu g/m^3$)", fontsize=15, labelpad=10)
cb_o3.ax.tick_params(labelsize=13)

ax.set_title(
    "FNR–Ozone Formation Sensitivity Regions in SMA",
    fontsize=23,
)
plt.subplots_adjust(left=0.12)  # 왼쪽 O₃ colorbar 공간 확보

out_png = os.path.join(sub_outp_dir,"FNR_O3_Formation_Sensitivity_SMA.png")
plt.savefig(out_png, dpi=300, bbox_inches="tight")
plt.show()
plt.close()

