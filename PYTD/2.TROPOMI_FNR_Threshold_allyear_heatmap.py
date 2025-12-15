import pandas as pd
import numpy as np
import os
import warnings
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.spatial import KDTree
from matplotlib import font_manager

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

def find_closest_points_and_update_kdtree(df_ozone, df_FNR):
    updated_rows = []

    grouped_ozone = df_ozone.groupby(['month', 'day'])
    grouped_FNR   = df_FNR.groupby(['month', 'day'])

    for (month, day), ozone_group in grouped_ozone:
        if (month, day) in grouped_FNR.groups:
            fnr_group = grouped_FNR.get_group((month, day))

            tree = KDTree(fnr_group[['lat', 'lon']].values)

            distances, indices = tree.query(ozone_group[['lat', 'lon']].values)

            updated_group = ozone_group.copy()
            updated_group[['lat', 'lon']] = (fnr_group[['lat', 'lon']].iloc[indices.flatten()].values)

            updated_rows.append(updated_group)

    return pd.concat(updated_rows, ignore_index=True)

updated_df_ozone = find_closest_points_and_update_kdtree(
    merged_df_ozone, merged_df
)


merged_df11 = pd.merge(
    merged_df,
    updated_df_ozone,
    on=['lat', 'lon', 'month', 'day'])[["month","day","lat","lon","HCHO","NO2","ozone"]]

merged_df11['ozone'] = pd.to_numeric(merged_df11['ozone'], errors='coerce')
merged_df11['ozone'] = merged_df11['ozone'].replace(-999.0, np.nan)
merged_df11 = merged_df11.dropna(subset=['HCHO','NO2','ozone'])

merged_df11['FNR'] = merged_df11['HCHO'] / merged_df11['NO2']
merged_df11['O3_unit'] = merged_df11['ozone'] * 1.96 * 1e3
merged_df11 = merged_df11.dropna(subset=['FNR','O3_unit'])

merged_df_heatmap = merged_df11.copy()

max_value10m = float(FNR_threshold['Upper'].iloc[0])
max_value10p = float(FNR_threshold['Lower'].iloc[0])


x = merged_df_heatmap['HCHO']
y = merged_df_heatmap['NO2']
z = merged_df_heatmap['O3_unit']

plt.figure(figsize=(10, 8))

hb = plt.hexbin(
    x, y, C=z,
    gridsize=100,
    cmap='jet',
    reduce_C_function=np.mean,
    vmin=0, vmax=310
)

cbar = plt.colorbar(hb)
cbar.ax.set_xlabel('O$_3$ $(µg/m^3)$', labelpad=10, fontsize=15)
cbar.ax.tick_params(labelsize=15)

plt.xlabel('HCHO ($10^{15}$ molec/cm$^2$)', fontsize=20)
plt.ylabel('NO$_2$ ($10^{15}$ molec/cm$^2$)', fontsize=20)

x_line = np.linspace(0, 60)
plt.plot(x_line, x_line / max_value10p, 'k-', linewidth=1)
plt.plot(x_line, x_line / max_value10m, 'k-', linewidth=1)

font_properties = {'color': 'black', 'size': 20}

plt.text(0.5, 30, "VOC-limited" if max_value10m != 0 else "Transitional", **font_properties)
plt.text(25, 0.5, "NOx-limited", **font_properties)

plt.xlim(0, 55)
plt.ylim(0, 35)
plt.tick_params(axis='both', which='major', labelsize=15)
plt.title('TROPOMI SMA', loc='right', fontsize=20, fontweight='bold')

outfile = os.path.join(sub_outp_dir, "TROPOMI_FNR_heatmap_SMA.png")

plt.savefig(outfile, dpi=300, bbox_inches='tight')
plt.show()
plt.close()
