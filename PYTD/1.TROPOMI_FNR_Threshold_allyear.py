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

updated_df_ozone = find_closest_points_and_update_kdtree(merged_df_ozone,merged_df)

merged_df11 = pd.merge(
    merged_df,
    updated_df_ozone,
    on=['lat', 'lon', 'month', 'day'])[["month", "day", "lat", "lon","HCHO", "NO2", "ozone"]]


merged_df11['ozone'] = pd.to_numeric(merged_df11['ozone'], errors='coerce')
merged_df11['ozone'] = merged_df11['ozone'].replace(-999.0, np.nan)
merged_df11 = merged_df11.dropna(subset=['HCHO', 'NO2', 'ozone'])

merged_df11['FNR'] = merged_df11['HCHO'] / merged_df11['NO2']
merged_df11.loc[ (merged_df11['FNR'] <= 0) | (merged_df11['FNR'] >= 8),'FNR'] = np.nan

merged_df11['O3_unit'] = merged_df11['ozone'] * 1.96 * 1e3
merged_df11 = merged_df11.dropna(subset=['FNR', 'O3_unit'])


nbin = 200
bin_edges = np.linspace(0, 8, nbin + 1)
bin_arr = np.full(nbin, np.nan)

for i in range(nbin):
    mask = (
        (merged_df11['FNR'] >= bin_edges[i]) &
        (merged_df11['FNR'] <  bin_edges[i+1])
    )
    if mask.any():
        bin_arr[i] = merged_df11.loc[mask, 'O3_unit'].mean()

valid_mask = ~np.isnan(bin_arr)
x = bin_edges[:-1][valid_mask]
y = bin_arr[valid_mask]


p = np.polyfit(x, y, 3)
y_fit = np.polyval(p, x)

dp  = np.polyder(p)
d2p = np.polyder(dp)

roots = np.roots(dp)
valid_roots = [
    r.real for r in roots
    if np.isreal(r) and 0 <= r.real <= 8
]



for root in valid_roots:
    if np.polyval(d2p, root) < 0:
        idx = np.abs(x - root).argmin()

        center = round(x[idx], 1)
        left   = round(x[max(idx - 10, 0)], 1)
        right  = round(x[min(idx + 10, len(x) - 1)], 1)

        plt.figure(figsize=(8, 6))
        plt.plot(x, y_fit, color='black')
        plt.scatter(x, y, s=20, color='black')
        plt.axvline(center, color='black')

        rect = patches.Rectangle(
            (left, 0),
            right - left,
            200,
            color='gray',
            alpha=0.4
        )
        plt.gca().add_patch(rect)

        plt.text(
            4.3, 165,
            f"SMA {center} ({left}-{right})",
            fontsize=25
        )
        plt.xlabel('TROPOMI HCHO/NO$_2$', fontsize=22)
        plt.ylabel(r'Ground $O_3$ ($\mu g/m^3$)', fontsize=22)
        plt.xlim(0, 8)
        plt.ylim(20, 180)
        plt.title("SMA", loc='left', fontsize=22)
        plt.tick_params(axis='both', labelsize=15)

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                sub_outp_dir, "TROPOMI_FNR_Threshold_SMA.png"),dpi=300)
        plt.show()
        plt.close()


        FNR_df = pd.DataFrame({
            "Region": ["SMA"],
            "FNR Threshold": [center],
            "Lower": [left],
            "Upper": [right]
        })

        FNR_df.to_csv(
            os.path.join(
                sub_outp_dir,
                "GEMS_FNR_Threshold_SMA.txt"
            ),
            sep="\t",
            index=False
        )
