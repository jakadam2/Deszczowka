from pathlib import Path
from tqdm import tqdm
import pandas as pd
import pupygrib
from itertools import product


class GribToCsv:
    def __init__(
        self,
        grib_dir: Path,
        csv_path: Path,
        des_long: float,
        des_lat: float,
        tol: float = 0.01
    ) -> None:
        self.grib_dir = grib_dir
        self.grib_paths = list(grib_dir.glob("*"))
        self.des_long = des_long
        self.des_lat = des_lat
        self.tol = tol
        self.csv_path = csv_path

    def convert(self):
        buffor = {'time': [], 'long': [], 'lat': [], 'values': []}
        for self.grib_path in tqdm(self.grib_paths):
            with open(self.grib_path, 'rb') as stream:
                for msg in pupygrib.read(stream):
                    long, lat = msg.get_coordinates()
                    time = msg.get_time()
                    values = msg.get_values()
                    x_range = list(range(values.shape[0]))
                    y_range = list(range(values.shape[1]))
                    for x, y in product(x_range, y_range):
                        if abs(long[x, y] - self.des_long) > self.tol or abs(lat[x, y] - self.des_lat) > self.tol:
                            continue
                        buffor['long'].append(long[x, y])
                        buffor['lat'].append(lat[x, y])
                        buffor['time'].append(time)
                        buffor['values'].append(values[x, y])

        df = pd.DataFrame(buffor)
        df['time'] = pd.to_datetime(df['time'])
        df.to_csv(self.csv_path, index=False)


if __name__ == "__main__":
    grib_dir = Path("/home/rusiek/Studia/viii_sem/Deszczowka/data")
    csv_file = Path("/home/rusiek/Studia/viii_sem/Deszczowka/tmp.csv")

    converter = GribToCsv(grib_dir, csv_file, des_long=8.69, des_lat=57.87)
    converter.convert()

    tmp_df = pd.read_csv(csv_file)
    print(tmp_df.head())
    print(tmp_df.columns)
    print(tmp_df.info())