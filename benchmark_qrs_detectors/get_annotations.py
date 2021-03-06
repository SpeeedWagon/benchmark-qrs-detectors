#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This script gets beats annotations of specialists from the chosen dataset. Obtained results (localisations of QRS for
 each record of the entire dataset) are saved in json files."""

import json
import os
import math
from typing import List
import numpy as np

from .dataset_helper import *

data_path = 'data'

# annotations corresponding to beats so related to QRS complexes' localisations
mit_beat_labels = ['N', 'L', 'R', 'B', 'A', 'a', 'J', 'S', 'V', 'r', 'F', 'e', 'j', 'n', 'E', '/', 'f', 'Q', '?']


def get_annotations_mit_bih_arrhythmia() -> Generator[Tuple[str, List[int]], None, None]:
    """
    read annotations of records from MIT BIH Arrhythmia Database and select those related to beat information.

    :return: ID and localisations of QRS complexes for each record
    :rtype: tuple(str, dict(str, ndarray))
    """
    records_list = pd.read_csv(f'{data_path}/mit-bih-arrhythmia-database/RECORDS', names=['id'])
    for record_id in records_list['id']:
        annotation = wfdb.rdann(f'{data_path}/mit-bih-arrhythmia-database/{record_id}', 'atr')
        annot_serie = pd.Series(annotation.symbol, index=annotation.sample, name="annotations")
        qrs_annotations = annot_serie.iloc[:].loc[annot_serie.isin(mit_beat_labels)]
        frames_annotations_list = qrs_annotations.index.tolist()
        yield record_id, frames_annotations_list


def get_annotations_mit_bih_noise() -> Generator[Tuple[str, List[int]], None, None]:
    """
    read annotations of records from MIT BIH Noise Stress Test Database and select those related to beat information.

    :return: ID and localisations of QRS complexes for each record
    :rtype: tuple(str, dict(str, ndarray))
    """
    records_list = pd.read_csv(f'{data_path}/mit-bih-noise-stress-test-database/RECORDS', names=['id'])
    for record_id in records_list['id'][:-3]:
        annotation = wfdb.rdann(f'{data_path}/mit-bih-noise-stress-test-database/{record_id}', 'atr')
        annot_serie = pd.Series(annotation.symbol, index=annotation.sample, name="annotations")
        qrs_annotations = annot_serie.iloc[:].loc[annot_serie.isin(mit_beat_labels)]
        frames_annotations_list = qrs_annotations.index.tolist()
        yield record_id, frames_annotations_list


def get_annotations_european_stt() -> Generator[Tuple[str, List[int]], None, None]:
    """
    read annotations of records from European STT Database and select those related to beat information.

    :return: ID and localisations of QRS complexes for each record
    :rtype: tuple(str, dict(str, ndarray))
    """
    records_list = pd.read_csv(f'{data_path}/european-stt-database/RECORDS', names=['id'])
    for record_id in records_list['id']:
        annotation = wfdb.rdann(f'{data_path}/european-stt-database/{record_id}', 'atr')
        annot_serie = pd.Series(annotation.symbol, index=annotation.sample, name="annotations")
        qrs_annotations = annot_serie.iloc[:].loc[annot_serie.isin(mit_beat_labels)]
        frames_annotations_list = qrs_annotations.index.tolist()
        yield record_id, frames_annotations_list


def get_annotations_mit_bih_supraventricular_arrhythmia() -> Generator[Tuple[str, List[int]], None, None]:
    """
    read annotations of records from MIT BIH Supraventricular Arrhythmia Database and select those related to beat
    information.

    :return: ID and localisations of QRS complexes for each record
    :rtype: tuple(str, dict(str, ndarray))
    """
    records_list = pd.read_csv(f'{data_path}/mit-bih-supraventricular-arrhythmia-database/RECORDS', names=['id'])
    for record_id in records_list['id']:
        annotation = wfdb.rdann(f'{data_path}/mit-bih-supraventricular-arrhythmia-database/{record_id}', 'atr')
        annot_serie = pd.Series(annotation.symbol, index=annotation.sample, name="annotations")
        qrs_annotations = annot_serie.iloc[:].loc[annot_serie.isin(mit_beat_labels)]
        frames_annotations_list = qrs_annotations.index.tolist()
        yield record_id, frames_annotations_list


def get_annotations_mit_bih_long_term() -> Generator[Tuple[str, List[int]], None, None]:
    """
    read annotations of records from MIT BIH Long Term ECG Database and select those related to beat information.

    :return: ID and localisations of QRS complexes for each record
    :rtype: tuple(str, dict(str, ndarray))
    """
    records_list = pd.read_csv(f'{data_path}/mit-bih-long-term-ecg-database/RECORDS', names=['id'])
    for record_id in records_list['id']:
        annotation = wfdb.rdann(f'{data_path}/mit-bih-long-term-ecg-database/{record_id}', 'atr')
        annot_serie = pd.Series(annotation.symbol, index=annotation.sample, name="annotations")
        qrs_annotations = annot_serie.iloc[:].loc[annot_serie.isin(mit_beat_labels)]
        frames_annotations_list = qrs_annotations.index.tolist()
        yield record_id, frames_annotations_list

def get_bidmc_hr_values(sample_name):
    with open(f'{data_path}/bidmc-ppg-and-respiration-database/bidmc_csv/{sample_name}_Numerics.csv') as f:
        return [float(line.split(",")[1]) for line in f.readlines()[1:]]

def get_annotations_bidmc_ppg_and_respiration() -> Generator[Tuple[str, List[int]], None, None]:
    records_list = pd.read_csv(f'{data_path}/bidmc-ppg-and-respiration-database/RECORDS', names=['id'])
    for record_id in records_list['id']:        
        sample_name = record_id.replace("bidmc", "bidmc_")
        hr_values = get_bidmc_hr_values(sample_name)
        hr_avg = np.average([x for x in hr_values if not math.isnan(x)])
        total_peaks = int(round(hr_avg / 60 * len(hr_values)))
        fake_peaks = [0] * total_peaks
        yield record_id, np.asarray(fake_peaks)


# generator of annotations' readers
dataset_annot_generators = {
    'mit-bih-arrhythmia': get_annotations_mit_bih_arrhythmia(),
    'mit-bih-noise-stress-test-e24': get_annotations_mit_bih_noise(),
    'mit-bih-noise-stress-test-e18': get_annotations_mit_bih_noise(),
    'mit-bih-noise-stress-test-e12': get_annotations_mit_bih_noise(),
    'mit-bih-noise-stress-test-e06': get_annotations_mit_bih_noise(),
    'mit-bih-noise-stress-test-e00': get_annotations_mit_bih_noise(),
    'mit-bih-noise-stress-test-e_6': get_annotations_mit_bih_noise(),
    'european-stt': get_annotations_european_stt(),
    'mit-bih-supraventricular-arrhythmia': get_annotations_mit_bih_supraventricular_arrhythmia(),
    'mit-bih-long-term-ecg': get_annotations_mit_bih_long_term(),
    'bidmc-ppg-and-respiration': get_annotations_bidmc_ppg_and_respiration()
}


def write_annotations_json(dataset: str, dict_annotations: Dict[str, List[int]]) -> None:
    """
    write localisations of beat annotations from a dictionary in a json file.

    :param dataset: name of the studied dataset
    :type dataset: str
    :param dict_annotations: localisations of beat annotations for each record of the dataset
    :type dict_annotations: dict(str, list(int)
    """
    os.makedirs(f'output/annotations', exist_ok=True)
    with open(f'output/annotations/{dataset}.json', 'w') as outfile:
        json.dump(dict_annotations, outfile)

