# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import os
import shutil
import subprocess
from tests.test_esub import run_exec_example


def test_esub_slurm_jobarray():

    # create directory for test output
    cwd = os.getcwd()
    path_testdir = 'esub_test_dir_submit_slurm'
    path_logdir = f'{cwd}/esub_test_dir_submit_slurm_log'
    if not os.path.isdir(path_testdir):
        os.mkdir(path_testdir)

    extra = '--test --main_memory=50000 --main_time_per_index=100 '\
            '--main_scratch=100000 --watchdog_memory=2400 --watchdog_time=50 '\
            '--watchdog_scratch=90000 --merge_time=30 --merge_memory=98000 '\
            '--merge_scratch=100000 --n_jobs=2 --main_n_cores_per_job=5 ' \
            '--system=slurm --merge_n_cores=10 --watchdog_n_cores=50 ' \
            '--max_njobs=100000 --keep_submit_files ' \
            '--additional_slurm_args=\"-C knl,--exclusive\"'
    # test with no tasks provided
    run_exec_example(path_testdir, path_logdir, mode='jobarray',
                     extra_esub_args=extra,
                     tasks_string='"1 > 3"')

    # remove directory for test output
    shutil.rmtree(path_testdir)

    # check that log directory was created and remove it then
    assert os.path.isdir(path_logdir)
    shutil.rmtree(path_logdir)
    subprocess.call('rm submit*.slurm', shell=1)


def test_esub_mpi():

    # create directory for test output
    cwd = os.getcwd()
    path_testdir = 'esub_test_dir_mpi_slurm'
    path_logdir = f'{cwd}/esub_test_dir_mpi_slurm_log'
    if not os.path.isdir(path_testdir):
        os.mkdir(path_testdir)

    extra = '--test --main_memory=50000 --main_time_per_index=100 '\
            '--main_scratch=100000 --watchdog_memory=2400 --watchdog_time=50 '\
            '--watchdog_scratch=90000 --merge_time=30 --merge_memory=98000 '\
            '--merge_scratch=100000 --n_jobs=2 --main_n_cores_per_job=5 ' \
            '--system=slurm --merge_n_cores=10 --watchdog_n_cores=50 ' \
            '--max_njobs=100000 --keep_submit_files ' \
            '--additional_slurm_args=\"-C knl,--exclusive\"'

    # test with no tasks provided
    run_exec_example(path_testdir, path_logdir, mode='mpi',
                     extra_esub_args=extra,
                     tasks_string='"1 > 3"')

    # remove directory for test output
    shutil.rmtree(path_testdir)

    # check that log directory was created and remove it then
    assert os.path.isdir(path_logdir)
    shutil.rmtree(path_logdir)
    subprocess.call('rm submit*.slurm', shell=1)
