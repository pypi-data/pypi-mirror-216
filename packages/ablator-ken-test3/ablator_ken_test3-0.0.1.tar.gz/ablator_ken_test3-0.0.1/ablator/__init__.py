from ablator.analysis.plot.cat_plot import ViolinPlot
from ablator.analysis.plot.main import PlotAnalysis
from ablator.analysis.results import Results
from ablator.analysis.plot.num_plot import LinearPlot
from ablator.config.main import ConfigBase, configclass
from ablator.config.types import (Annotation, Derived, Dict, Enum, List,
                                  Literal, Optional, Stateful, Stateless,
                                  Tuple, Type)
from ablator.main.configs import (ModelConfig, Optim, ParallelConfig,
                                  RunConfig, TrainConfig)
from ablator.main.model.wrapper import ModelWrapper
from ablator.main.mp import ParallelTrainer
from ablator.main.proto import ProtoTrainer
from ablator.modules.optimizer import OPTIMIZER_CONFIG_MAP, OptimizerConfig
from ablator.modules.scheduler import SCHEDULER_CONFIG_MAP, SchedulerConfig
import os
from . import download_rlone

# 检查rclone是否已经存在，如果不存在则下载
if not os.path.exists(os.path.join(os.path.dirname(__file__), 'rclone')):
    download_rlone('1.55.0', os.path.dirname(__file__))