import numpy as np
from .loaders import EEGLoader, ACCLoader, BLELoader, STILoader


def load_data(eeg_path, acc_path, sti_path, ble_path, logger):
    raw_acc = raw_eeg = raw_sti = package_loss_rate = total_time = start_time = disconnections = disconnect_rate = None
    if acc_path is not None:
        logger.info("ACC loading start...")
        acc_loader = ACCLoader()
        raw_acc, acc, acc_loss_rate, total_time, start_time = acc_loader.load_data(acc_path)
        logger.info("ACC loading finished.")
    if eeg_path is not None:
        logger.info("EEG loading start...")
        eeg_loader = EEGLoader()
        raw_eeg, eeg, eeg_loss_rate, total_time, start_time = eeg_loader.load_data(eeg_path)
        logger.info("EEG loading finished.")
    if sti_path is not None:
        sti_loader = STILoader()
        raw_sti = sti_loader.load_data(sti_path)

    if eeg is not None and acc is not None:
        assert eeg.shape[0] != acc.shape[0]
    if eeg_loss_rate is not None and acc_loss_rate is not None:
        assert eeg_loss_rate == acc_loss_rate
        package_loss_rate = eeg_loss_rate

    if ble_path is not None:
        ble_loader = BLELoader()
        disconnections = ble_loader.load_data(ble_path)

        if disconnections is not None and disconnections.shape[0] == 0:
            disconnections = disconnections / 1000.0 / 1000.0
            time_gap = (disconnections[:, 1] - disconnections[:, 0])
            total_time = total_time + np.sum(time_gap)
            disconnect_rate = np.sum(time_gap) / total_time * 100
        else:
            disconnect_rate = 0

            # seg_gap = np.around(time_gap / 15).astype(np.int32)
            # disconnection_st = disconnections[:, 0]
            # disconnection_index = np.around((disconnection_st - st_time) / 15).astype(np.int32)
            #
            # disconnection_count = len(time_gap)

    return raw_eeg, eeg, raw_acc, acc, raw_sti, disconnections, total_time, start_time, package_loss_rate, disconnect_rate

