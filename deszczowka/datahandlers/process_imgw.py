from pathlib import Path
import pandas as pd


class IMGWProcessor:
    def __init__(
        self,
        input_dir: Path,
        output_path: Path,
        id: str
    ) -> None:
        self.input_dir = input_dir
        self.input_paths = list(input_dir.glob("*"))
        self.output_path = output_path
        self.id = id

    def process(self):
        df_output = pd.DataFrame(columns=['time', 'rainfall[10m]'])
        for input_path in self.input_paths:
            df = pd.read_csv(input_path, names=['station_id', 'type_id', 'time', 'rainfall[10m]'], sep=';')
            df = df[df['station_id'] == self.id]
            df['time'] = pd.to_datetime(df['time'])
            df_output = pd.concat([df_output, df[['time', 'rainfall[10m]']]], ignore_index=True)
        df_output.to_csv(self.output_path, index=False)


if __name__ == "__main__":
    grib_dir = Path("/home/rusiek/Studia/viii_sem/Deszczowka/imgw")
    csv_file = Path("/home/rusiek/Studia/viii_sem/Deszczowka/tmp.csv")

    converter = IMGWProcessor(grib_dir, csv_file, id=249170080)
    converter.process()

    tmp_df = pd.read_csv(csv_file)
    print(tmp_df.head())
    print(tmp_df.columns)
    print(tmp_df.info())