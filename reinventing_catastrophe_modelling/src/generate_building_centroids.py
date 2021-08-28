from typing import Dict, Sequence, Any
from joblib import Parallel, delayed

import osmnx as ox
import geopandas as gpd

from config.model_settings import DataConfig, OSMConfig


class GenerateBuildingCentroids:
    def __init__(self, countries: Sequence, tags: Dict[str, Any]):
        self.countries = countries
        self.tags = tags

    @classmethod
    def from_dataclass_config(
        cls, data_config: DataConfig, osm_config: OSMConfig
    ) -> "GenerateBuildingCentroids":
        countries = []
        for country in data_config.COUNTRY_CODES:
            country_info = data_config.COUNTRY_BOUNDING_BOXES.get(country, "WO")
            countries.append(country_info)

        return cls(countries=countries, tags=osm_config.TAG)

    def execute(self):
        Parallel(n_jobs=-1, backend="multiprocessing", verbose=5)(
            delayed(self.execute_for_country)(country) for country in self.countries
        )

    def execute_for_country(self, country: str):
        self.get_representative_building_point

    def _get_boundaries_from_place(self) -> gpd.GeoDataFrame:
        return ox.geometries.geometries_from_place(self.country[0], self.tags)

    def get_representative_building_point(self) -> gpd.GeoDataFrame:
        building_footprints = self._get_boundaries_from_place()
        building_footprints.centroid_geometry = building_footprints.representative_point()
        return building_footprints
