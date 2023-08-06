import json
import logging
import math
import os

from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union
from pydantic import BaseModel, validator, root_validator, Field

import geopandas as gpd
import numpy as np
import subprocess

try:
    import ogr
except:
    from osgeo import ogr

log = logging.getLogger(__name__)



@dataclass
class Tile:
    name: str
    epsg: int
    count: int

@dataclass
class Services:
    sub: List[str] = field(default_factory=list)
    dst: List[str] = field(default_factory=list)
    parcel_id: str = field(default_factory=str)
    FOI: List[str] = field(default_factory=list)


@dataclass
class DataObject:
    tiles: List[Tile]
    services: Dict[str, Services]
    pixel: Dict[str, int]
    kult_conversion_table_name: Optional[str]
    conversion_table_original_column: Optional[str]
    conversion_table_target_column: Optional[str]
    classification_support_data: Optional[Path]
    min_parcel : int

    def get_service_info(self, service_name):
        for serivce_item_name, serive_attribute in self.services.items():
            if serivce_item_name == service_name:
                return serive_attribute

    def get_tile_info(self, tile_name):
        if self.tiles is not None:
            for tile_name_item in self.tiles:
                if tile_name_item.name == tile_name:
                    return tile_name_item
        else:
            return None

class DataObjectModel(BaseModel):
    tiles: Optional[List[Tile]]
    services: Dict[str, Services]
    pixel: Dict[str, int] =  Field({})
    kult_conversion_table_name : Optional[str]
    conversion_table_original_column: Optional[str]
    conversion_table_target_column: Optional[str]
    classification_support_data: Optional[Path]
    min_parcel: int = Field(2000)

    @validator('services', pre=True)
    def convert_to_services_objects(cls, value):
        return {k: Services(**v) for k, v in value.items()}

def open_json(path: Union[Path, str]):
    with open(path, 'r') as file:
        return json.load(file)

class Config(BaseModel):
    tiles: Optional[List]
    services: dict

def create_object(config_path):
    # Parsing the JSON data and creating the object
    parsed_object = DataObjectModel.parse_obj(open_json(config_path))
    data_object = DataObject(**parsed_object.dict())
    return data_object



#############################################################

def return_eodata_tilename(tilename):
    if "-" in tilename:
        eodata_tilename = tilename.split("-")[0]
        return eodata_tilename
    else:
        return tilename

def get_tile_list(tile_gpkgfilepath, gpkg_parcel_column):
    master_df = gpd.read_file(str(tile_gpkgfilepath))
    return master_df[gpkg_parcel_column].to_list()

def compile_service_project_env_time_sub_folder_relpath(parent_folder, service, project, environment, analysis_time, subfolder_type= None):
    if subfolder_type is not None:
        service_folder = parent_folder.joinpath(str(service).lower(), str(project).upper(), str(environment).upper(),
                                            str(analysis_time), str(subfolder_type).upper())
    else:
        service_folder = parent_folder.joinpath(str(service).lower(), str(project).upper(), str(environment).upper(),
                                            str(analysis_time))
    return service_folder


def compile_output_dir(parent_folder, service_name, environment, project, analysis_time, tilename, sub_dir=None):
    parent_output_folder = Path(parent_folder).joinpath("output")
    output_dir = compile_service_project_env_time_sub_folder_relpath(parent_output_folder, service_name, project, environment, analysis_time, sub_dir)
    output_dir_tile = output_dir.joinpath(tilename)
    return output_dir_tile

###############################################################################
def get_gpkg_epsg(gpkg_path):
    source = ogr.Open(str(gpkg_path), update=False)
    layer = source.GetLayer()
    epsg = layer.GetSpatialRef().GetAuthorityCode(None)
    source = None
    layer = None
    return epsg



def split_geodataframe(gdf, subtiles_count, min_rows = 2000):
    total_rows = len(gdf)
    if min_rows is None:
        min_rows = total_rows/subtiles_count
    max_rows_per_split = math.ceil(max(min_rows, total_rows/subtiles_count))
    splits = []
    for i in range(subtiles_count):
        start_idx = i * max_rows_per_split
        end_idx = min((i + 1) * max_rows_per_split, total_rows)
        split_gdf = gdf.iloc[start_idx:end_idx]
        splits.append(split_gdf)
    return splits


def do_split_save_gpkg(input_gpkg, output_gpkg_basename, output_dir,
                       subtiles_count=14, min_parcels = None):

    logfilepath = output_dir.joinpath("tiling_log.txt")
    logfile = open(logfilepath, "w")
    logfile.write("--------------------------------\n")
    logfile.write("-SUBTILE PARCEL COUNT-\n")
    logfile.write("--------------------------------\n")

    gpkg_filename = Path(input_gpkg).name
    gpkg_ds = ogr.Open(str(input_gpkg))

    # Get the number of parcels
    layer_name = gpkg_ds.GetLayer().GetName()
    feature_count = gpkg_ds.GetLayer().GetFeatureCount()

    # Load the GeoPackage file into a GeoDataFrame
    gdf = gpd.read_file(input_gpkg, layer=layer_name)

    if min_parcels is None:
        # Divide the GeoDataFrame into n equal parts
        gdfs = np.array_split(gdf, subtiles_count)
    else:
        gdfs = split_geodataframe(gdf, subtiles_count, min_parcels)
    gpgk_paths = []
    # Write each subset of data to a new GeoPackage file
    parcel_count = 0
    for gdf_index, gdf_subset in enumerate(gdfs):

        number_of_parcels = len(gdf_subset)
        parcel_count += number_of_parcels

        if number_of_parcels !=0:
            output_file = output_dir.joinpath(output_gpkg_basename.replace(".gpkg", f"-{gdf_index + 1}.gpkg"))
            output_file.unlink(missing_ok=True)
            layer_name = gpkg_filename.replace(".gpkg", f"_{gdf_index+1}.gpkg")
            gdf_subset.to_file(output_file, layer=layer_name, driver='GPKG')
            gpgk_paths.append(output_file)
        else:
            output_file = output_dir.joinpath(output_gpkg_basename.replace(".gpkg", f"-{gdf_index + 1}_NODATA.txt"))
            output_file.unlink(missing_ok=True)
            output_file.write_text("No parcel")
            gpgk_paths.append(output_file)
        logfile.write(f"{output_file} -- {number_of_parcels} \n")
    logfile.write("--------------------------------\n")
    logfile.write(f"PARCEL COUNT = {parcel_count}\n")
    logfile.close()
    return gpgk_paths

class Merge():
    def __init__(self, project, environemt, yearmonth, service, bioregion, classification_support_data=None, sar_type= None):
        self.project = str(project).upper()
        self.environemt = str(environemt).upper()
        self.yearmonth = str(yearmonth)
        self.service = str(service).upper()
        self.sar_type = str(sar_type).upper()
        self.bioregion = str(bioregion).upper()
        self.year = self.yearmonth[0:4]
        self.classification_support_data = classification_support_data

    def get_config_path(self, parent_folder):
        config_path = parent_folder.joinpath("project_info", self.project, f"{self.bioregion}_config.json")
        if config_path.exists():
            log.info(f"{config_path} exists.")
            return config_path
        else:
            raise Exception(f"{config_path} doesnt exists.")

    def set_bioregion_path(self, parent_folder):
        gpkg_filepath = parent_folder.joinpath("tiles", self.project, f"{self.bioregion}_tiles.gpkg")
        if gpkg_filepath.exists():
            log.info(f"{gpkg_filepath} exists.")
            self.region_gpkg = gpkg_filepath
            return gpkg_filepath
        else:
            raise Exception(f"{gpkg_filepath} doesnt exists.")

    def set_epsg(self, template_gpkg):
        epsg = get_gpkg_epsg(template_gpkg)
        self.epsg = epsg


def create_submit_tile_instance(project, environment, yearmonth, service, bioregion, parent_folder, tile_name = None, tool_service = None, gpkg_parcel_column = "sitecode"):
    mi = Merge(project=project, environemt=environment, yearmonth=yearmonth, service=service, bioregion=bioregion, classification_support_data=None)
    mi.set_bioregion_path(parent_folder)

    config_path = mi.get_config_path(parent_folder)
    config = create_object(config_path)

    service_attributes = config.get_service_info(service)
    service_gpkg_dst = service_attributes.dst

    if len(service_gpkg_dst) == 1:
        dst_tool = service_gpkg_dst[0]
    else:
        if tool_service is None:
            raise Exception(f"tool_service is none")
        else:
            if tool_service in service_gpkg_dst:
                dst_tool = tool_service
            else:
                raise Exception(f"{tool_service} not in dst list")

    if tile_name is None:
        tilename_list = []
        tile_list = get_tile_list(mi.region_gpkg, gpkg_parcel_column)
        for tile_name in tile_list:
            eodata_tilename = return_eodata_tilename(tile_name)
            for service_gpkg_dst_item in service_gpkg_dst:
                if not service_gpkg_dst_item == tool_service:
                    continue
                output_dir = compile_output_dir(parent_folder, service_gpkg_dst_item, mi.environemt, mi.project,
                                                mi.yearmonth,
                                                eodata_tilename, sub_dir=None)
            output_dir_filelist = os.listdir(output_dir)
            output_dir_filelist = [i for i in output_dir_filelist if i.endswith('.gpkg')]
            output_dir_filelist_len = len(output_dir_filelist)

            for subtile_count in range(output_dir_filelist_len):
                tilename_list.append(f"{eodata_tilename}-{subtile_count + 1}")

    else:
        eodata_tilename = return_eodata_tilename(tile_name)
        for service_gpkg_dst_item in service_gpkg_dst:
            if not service_gpkg_dst_item == tool_service:
                continue
            output_dir = compile_output_dir(parent_folder, service_gpkg_dst_item, mi.environemt, mi.project,
                                            mi.yearmonth,
                                            eodata_tilename, sub_dir=None)
        output_dir_filelist =  os.listdir(output_dir)
        output_dir_filelist  = [i for i in output_dir_filelist if i.endswith('.gpkg')]
        output_dir_filelist_len = len(output_dir_filelist)

        tilename_list = []
        for subtile_count in range(output_dir_filelist_len):
            tilename_list.append(f"{eodata_tilename}-{subtile_count+1}")

    return tilename_list


class Tiles():
    row : str
    col : str
    width : str
    height : str
    x_offset : str
    y_offset : str
    xmin : str
    xmax : str
    ymin : str
    ymax : str
    pixel_size : str
    tile_folder: Path
    tile_multiband_composite: Path


def setup_tiles(aoi_xmin, aoi_xmax, aoi_ymin, aoi_ymax, pixel_size, tiles_parentdir, max_tile_size = 3000):

    if not Path(tiles_parentdir).exists():
        os.makedirs(tiles_parentdir)

    # Calculate xmax and ymin based on the pixel size and number of columns and rows
    num_cols = math.ceil((aoi_xmax - aoi_xmin) / pixel_size)
    num_rows = math.ceil((aoi_ymax - aoi_ymin) / pixel_size)
    # Returns a dictionary of tile infos that can be used to cut a large raster into smaller tiles.
    # Each item in the dictionary has properties:
    # row, column, width_pixels, height_pixels, x_offset_pixels, y_offset_pixels, ulx_coordinate, uly_coordinate
    n_tile_cols = math.ceil(num_cols / max_tile_size)
    n_tile_rows = math.ceil(num_rows / max_tile_size)
    log.debug(f"ntiles: {n_tile_rows}, {n_tile_cols}")

    last_col = n_tile_cols - 1
    last_row = n_tile_rows - 1
    tile_infos = []
    for tile_row in range(n_tile_rows):
        tile_height = max_tile_size
        y_offset = tile_row * tile_height
        # Last row is a special case - tile height must be adjusted.
        if tile_row == last_row:
            tile_height = num_rows - (max_tile_size * tile_row)
        log.debug(f"tile_height {tile_height}")
        for tile_col in range(n_tile_cols):
            tile_width = max_tile_size
            x_offset = tile_col * tile_width
            # Last column is a special case - tile width must be adjusted.
            if tile_col == last_col:
                tile_width = num_cols - (max_tile_size * tile_col)

            # tile_ulx and tile_uly are the absolute coordinates of the upper left corner of the tile.
            tile_ulx = aoi_xmin + x_offset * pixel_size
            tile_uly = aoi_ymax - y_offset * pixel_size
            tile_lrx = tile_ulx + tile_width * pixel_size
            tile_lry = tile_uly - tile_height * pixel_size

            tile_work_dir = tiles_parentdir.joinpath("tile_{:03d}_{:03d}".format(
                tile_row + 1, tile_col + 1))
            tile_work_dir.mkdir(parents=True, exist_ok=True)

            tile_multiband_composite = tile_work_dir.joinpath("tile_{:03d}_{:03d}.tif".format(tile_row + 1, tile_col + 1))

            tile_info = Tiles(
                row= tile_row,
                col= tile_col,
                width= tile_width,
                height= tile_height,
                x_offset= x_offset,
                y_offset= y_offset,
                xmin= tile_ulx,
                xmax= tile_lrx,
                ymin= tile_lry,
                ymax= tile_uly,
                pixel_size= pixel_size,
                tile_folder= tile_work_dir,
                tile_multiband_composite = tile_multiband_composite
            )
            tile_infos.append(tile_info)
    return tile_infos

def cut_composite_totile_function(input_data):
    src_filepath = input_data[0]
    tile_extent_path_dict_json = input_data[1]

    tile_infos = json.loads(tile_extent_path_dict_json)

    for tile_name, tile_info in tile_infos.items():
        tile_composite_filepath = Path(tile_info['tile_folder']).joinpath(Path(src_filepath).name)
        if tile_composite_filepath.exists(): continue
        cmd_gdal = ["gdal_translate",
                    "-of", "GTiff",
                    "-co", "COMPRESS=DEFLATE",
                    "-co", "BIGTIFF=YES",
                    "-co", "TILED=YES",
                    "-eco", "-projwin",
                    "{}".format(tile_info['ulx']), "{}".format(tile_info['uly']),
                    "{}".format(tile_info['lrx']), "{}".format(tile_info['lry']),
                    str(src_filepath), str(tile_composite_filepath)]
        cmd_output = subprocess.run(cmd_gdal, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log.debug(f"exit code {cmd_output.returncode} --> {cmd_gdal}")
