import csv
import random
import os
import threading

class ContentLoader:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.filepath = os.path.join(base_dir, "..", "contentIds.csv")
        self.data = []
        self._load_csv()

    def _load_csv(self):
        try:
            with open(self.filepath, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                self.data = [
                    {k.strip(): v.strip() for k, v in row.items()}
                    for row in reader
                ]
                print("CSV LOADED SUCCESSFULLY:")
        except FileNotFoundError:
            print(f"ERROR: CSV file not found at path: {self.filepath}")
            self.data = []

    def get_random_movie_id(self):
        movie_ids = [row["movie_id"] for row in self.data if row.get("movie_id")]
        return random.choice(movie_ids) if movie_ids else None

    def get_random_series_id(self):
        series_ids = [row["series_id"] for row in self.data if row.get("series_id")]
        return random.choice(series_ids) if series_ids else None

    def get_random_live_id(self):
        live_ids = [row["channel_id"] for row in self.data if row.get("channel_id")]
        return random.choice(live_ids) if live_ids else None
    






class UserCredentialLoader:
    _lock = threading.Lock()
    _credentials = []
    _index = 0

    @classmethod
    def _load_credentials(cls):
        if cls._credentials:
            return  # Already loaded

        # 👇 Dynamically resolve the CSV path relative to this file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base_dir, "..","users.csv")  # Change path if needed

        try:
            with open(filepath, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                cls._credentials = [row for row in reader]
                print(f"[UserCredentialLoader] Loaded {len(cls._credentials)} users from CSV.")
        except FileNotFoundError:
            print(f"[UserCredentialLoader] ERROR: CSV file not found at path: {filepath}")
            cls._credentials = []

    @classmethod
    def get_next_credential(cls):
        cls._load_credentials()

        with cls._lock:
            if not cls._credentials:
                raise Exception("No credentials loaded. CSV may be empty or missing.")

            # Recycle = True → Loop around
            cred = cls._credentials[cls._index]
            cls._index = (cls._index + 1) % len(cls._credentials)
            return cred
        

import os
import csv
import threading

class DeviceIdLoader:
    _lock = threading.Lock()
    _device_ids = []
    _index = 0

    @classmethod
    def _load_device_ids(cls):
        if cls._device_ids:
            return

        base_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base_dir, "..", "deviceId.csv")

        abs_path = os.path.abspath(filepath)
        print(f"[DeviceIdLoader] Looking for CSV at: {abs_path}")

        try:
            with open(filepath, newline='') as csvfile:
                reader = csv.DictReader(csvfile)

                print(f"[DeviceIdLoader] CSV columns found: {reader.fieldnames}")

                # Accept either deviceId OR device_id
                valid_columns = ["deviceId", "device_id"]
                column = None

                for col in valid_columns:
                    if col in reader.fieldnames:
                        column = col
                        break

                if not column:
                    print("[DeviceIdLoader] ERROR: CSV missing required column 'deviceId' or 'device_id'")
                    cls._device_ids = []
                    return

                cls._device_ids = [
                    row[column].strip()
                    for row in reader
                    if row.get(column)
                ]

                print(f"[DeviceIdLoader] Successfully loaded {len(cls._device_ids)} device IDs.")

        except FileNotFoundError:
            print(f"[DeviceIdLoader] ERROR: CSV file NOT found at: {abs_path}")
            cls._device_ids = []

    @classmethod
    def get_next_device_id(cls):
        cls._load_device_ids()

        with cls._lock:
            if not cls._device_ids:
                raise Exception("No device IDs loaded from CSV.")

            device_id = cls._device_ids[cls._index]
            cls._index = (cls._index + 1) % len(cls._device_ids)
            return device_id
