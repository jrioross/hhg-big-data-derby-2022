import numpy as np
import pandas as pd
import utm
import math
from tqdm.auto import tqdm
tqdm.pandas()

def tqdm_pandas(t):
    from pandas.core.frame import DataFrame
    def inner(df, func, *args, **kwargs):
        t.total = groups.size // len(groups)
        def wrapper(*args, **kwargs):
            t.update(1)
            return func(*args, **kwargs)
        result = df.transform(wrapper, *args, **kwargs)
        t.close()
        return result
    DataFrame.progress_transform = inner

def get_speed(points):
    speed = [0]
    points = points.values
    for i in range(1, len(points)):
        speed.append(4 * np.linalg.norm(np.array(points[i]) - np.array(points[i-1])))
    return speed

def getAngle(a, b, c, thresh=5):
    ang = 180 - math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    if ang < -180:
        ang += 360
    if ang > 180:
        ang -= 360
    if abs(ang) > thresh:
        return np.nan
    return ang

def get_turning_angle(points):
    turning_angle = [0]
    for i in range(1, len(points.values) - 1):
        turning_angle.append(getAngle(points.values[i-1], points.values[i], points.values[i+1]))
    turning_angle.append(0)
    return turning_angle

def lateral_distance(p1, p2, p3):
    return round(np.cross(p2-p1, p1-p3) / np.linalg.norm(p2-p1), 2)

def longitudinal_distance(p1, p2, p3):
    return round(np.dot(p2-p1, p3-p2) / np.linalg.norm(p2-p1), 2)

def get_lateral_distances(points):
    return [[lateral_distance(point1[0], point1[1], point2[1]) for point2 in points.values] for point1 in points.values]

def get_longitudinal_distances(points):
    return [[longitudinal_distance(point1[0], point1[1], point2[1]) for point2 in points.values] for point1 in points.values]

def get_position(longitudinal_distances):
    position = (np.array(longitudinal_distances) >= 0).sum()
    return np.nan if position == 0 else position

def get_speed_and_position_columns(df):

    df = (df.sort_values(['track_id', 
                         'race_date', 
                         'race_number', 
                         'program_number', 
                         'trakus_index'])
            .reset_index(drop=True)
        )

    # convert lat/lon to UTM coordinates (meters)
    df['xy'] = (np.array(
                        utm.from_latlon(df['latitude'].values, 
                                        df['longitude'].values
                                        )
                                        [:2]
                        )
                        .T
                        .tolist()
            )

    # get speeds and add column to df
    df['speed'] = (df.groupby(['track_id', 
                              'race_date', 
                              'race_number', 
                              'program_number']
                            )
                    ['xy']
                    .progress_transform(get_speed)
                )

    # get turning angles and add column to df
    df['turning_angle'] = (df.groupby(['track_id', 
                                      'race_date', 
                                      'race_number', 
                                      'program_number']
                                    )
                              ['xy']
                              .progress_transform(get_turning_angle)
                        )

    # prepare df to compare subsequent trakus id lat/lon and thus get distances between points
    # (could also be done with .shift())

    ## copy df
    df_prev = df[['track_id', 
                  'race_date', 
                  'race_number', 
                  'trakus_index', 
                  'program_number', 
                  'xy']].copy()
    ## add one to index in anticipation of merge
    df_prev['trakus_index'] = df_prev['trakus_index'] + 1

    ## merge with offset indices
    df = pd.merge(df, 
                  df_prev, 
                  on=['track_id', 
                      'race_date', 
                      'race_number', 
                      'program_number', 
                      'trakus_index'], 
                  suffixes=['', '_prev'], 
                  how='left'
                )

    # create column with lat/lon pairs (list of lat/lon arrays)
    df['xy_pair'] = df.progress_apply(lambda row: [np.array(row['xy_prev']), 
                                                   np.array(row['xy'])], 
                                     axis=1
                                     )

    # get lateral distances and add column to df
    df['lateral_distances'] = (df.groupby(['track_id', 
                                          'race_date', 
                                          'race_number', 
                                          'trakus_index']
                                        )
                                 ['xy_pair']
                                 .progress_transform(get_lateral_distances)
                            )

    # get lateral distances and add column to df
    df['longitudinal_distances'] = (df.groupby(['track_id', 
                                                'race_date', 
                                                'race_number', 
                                                'trakus_index']
                                            )
                                      ['xy_pair']
                                      .progress_transform(get_longitudinal_distances)
                                )
    # get position and add column to df
    df['position'] = df['longitudinal_distances'].progress_apply(get_position)

    return df
