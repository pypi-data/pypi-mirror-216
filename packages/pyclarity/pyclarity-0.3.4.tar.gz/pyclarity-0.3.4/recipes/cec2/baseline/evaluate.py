import csv
import hashlib
import json
import logging
from pathlib import Path

import hydra
import numpy as np
from omegaconf import DictConfig
from scipy.io import wavfile
from tqdm import tqdm

from clarity.evaluator.haspi import haspi_v2_be

logger = logging.getLogger(__name__)


def read_csv_scores(file: Path):
    score_dict = {}
    with file.open("r", encoding="utf-8") as fp:
        reader = csv.reader(fp)
        _ = next(reader)
        for row in reader:
            score_dict[row[0] + "_" + row[1]] = float(row[2])
    return score_dict


@hydra.main(config_path=".", config_name="config")
def run_calculate_SI(cfg: DictConfig) -> None:
    with Path(cfg.path.scenes_listeners_file).open("r", encoding="utf-8") as fp:
        scenes_listeners = json.load(fp)
    with Path(cfg.path.listeners_file).open("r", encoding="utf-8") as fp:
        listener_audiograms = json.load(fp)
    Path(cfg.path.exp_folder).mkdir(parents=True, exist_ok=True)

    enhanced_folder = Path(cfg.path.exp_folder) / "enhanced_signals"

    if cfg.evaluate.cal_unprocessed_si:
        unproc_si_file = Path(cfg.path.exp_folder) / "si_unproc.csv"
        unproc_csv_lines = [["scene", "listener", "haspi"]]
        if unproc_si_file.exists():
            score_dict = read_csv_scores(unproc_si_file)
            ave_score = np.mean(list(score_dict.values()))
            logger.info(
                "si_unproc.csv exists, and the average HASPI scores for unprocessed "
                "scenes is %.4f",
                ave_score,
            )

    si_file = Path(cfg.path.exp_folder) / "si.csv"
    csv_lines = [["scene", "listener", "haspi"]]
    if si_file.exists():
        score_dict = read_csv_scores(si_file)
        ave_score = np.mean(list(score_dict.values()))
        logger.info("si.csv exists, and the average HASPI scores is %4f", ave_score)
        return

    for scene in tqdm(scenes_listeners):
        for listener in scenes_listeners[scene]:
            logger.info(f"Running SI calculation: scene {scene}, listener {listener}")
            if cfg.evaluate.set_random_seed:
                scene_md5 = int(hashlib.md5(scene.encode("utf-8")).hexdigest(), 16) % (
                    10**8
                )
                np.random.seed(scene_md5)

            # retrieve audiograms
            cfs = np.array(listener_audiograms[listener]["audiogram_cfs"])
            audiogram_left = np.array(
                listener_audiograms[listener]["audiogram_levels_l"]
            )
            audiogram_right = np.array(
                listener_audiograms[listener]["audiogram_levels_r"]
            )

            # retrieve signals
            fs_proc, proc = wavfile.read(
                enhanced_folder / f"{scene}_{listener}_HA-output.wav"
            )

            fs_ref_anechoic, ref_anechoic = wavfile.read(
                Path(cfg.path.scenes_folder) / f"{scene}_target_anechoic_CH1.wav"
            )

            fs_ref_target, ref_target = wavfile.read(
                Path(cfg.path.scenes_folder) / f"{scene}_target_CH1.wav"
            )

            assert fs_ref_anechoic == fs_ref_target == fs_proc

            proc = proc / 32768.0
            ref_anechoic = ref_anechoic / 32768.0
            ref_target = ref_target / 32768.0

            rms_target = np.mean(ref_target**2, axis=0) ** 0.5
            rms_anechoic = np.mean(ref_anechoic**2, axis=0) ** 0.5
            ref = ref_anechoic * rms_target / rms_anechoic

            si = haspi_v2_be(
                reference_left=ref[:, 0],
                reference_right=ref[:, 1],
                processed_left=proc[:, 0],
                processed_right=proc[:, 1],
                fs_signal=fs_ref_anechoic,
                audiogram_left=audiogram_left,
                audiogram_right=audiogram_right,
                audiogram_cfs=cfs,
            )
            logger.info(f"The HASPI score is {si}")
            csv_lines.append([scene, listener, str(si)])

            if cfg.evaluate.cal_unprocessed_si:
                if cfg.evaluate.set_random_seed:
                    scene_md5 = int(
                        hashlib.md5(scene.encode("utf-8")).hexdigest(), 16
                    ) % (10**8)
                    np.random.seed(scene_md5)

                _fs_unproc, unproc = wavfile.read(
                    Path(cfg.path.scenes_folder) / f"{scene}_mix_CH1.wav"
                )
                unproc = unproc / 32768.0
                si_unproc = haspi_v2_be(
                    reference_left=ref[:, 0],
                    reference_right=ref[:, 1],
                    processed_left=unproc[:, 0],
                    processed_right=unproc[:, 1],
                    fs_signal=fs_ref_anechoic,
                    audiogram_left=audiogram_left,
                    audiogram_right=audiogram_right,
                    audiogram_cfs=cfs,
                )
                logger.info(f"The unprocessed signal HASPI score is {si_unproc}")
                unproc_csv_lines.append([scene, listener, str(si_unproc)])

    with si_file.open("w", encoding="utf-8") as csv_f:
        csv_writer = csv.writer(
            csv_f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        for line in csv_lines:
            csv_writer.writerow(line)
    score_dict = read_csv_scores(si_file)
    ave_score = np.mean(list(score_dict.values()))
    logger.info("si.csv exists, and the average HASPI scores is %.4f", ave_score)

    if cfg.evaluate.cal_unprocessed_si:
        with unproc_si_file.open("w", encoding="utf-8") as csv_f:
            csv_writer = csv.writer(
                csv_f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            for line in unproc_csv_lines:
                csv_writer.writerow(line)
        score_dict = read_csv_scores(unproc_si_file)
        ave_score = np.mean(list(score_dict.values()))
        logger.info(
            "si_unproc.csv exists, and the average HASPI scores "
            "for unprocessed scenes is %.4f",
            ave_score,
        )


# pylint: disable=no-value-for-parameter
if __name__ == "__main__":
    run_calculate_SI()
