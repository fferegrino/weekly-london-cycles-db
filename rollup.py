import polars as pl
from datetime import date, timedelta

start_date = date(2022, 4, 25)
end_date = date.today()
beginning_of_week = date.today() - timedelta(days=date.today().weekday())

date_glob_pattern = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]*"

cycle_data = pl.read_csv(
    f"./london-cycles-db/data/{date_glob_pattern}",
    try_parse_dates=True,
    dtypes={"lat": pl.Float32, "lon": pl.Float32, "bikes": int, "empty_docks": int, "docks": int},
)


while start_date < beginning_of_week:
    end_date = start_date + timedelta(days=7)
    interval_data = cycle_data.filter((cycle_data["query_time"] >= start_date) & (cycle_data["query_time"] < end_date))
    interval_data.sort(["query_time", "place_id"]).write_csv(
        f"./data/{start_date}_{end_date}.csv"
    )
    start_date += timedelta(days=7)
