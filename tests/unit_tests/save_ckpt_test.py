import unittest
import os
from super_gradients.training import SgModel
from super_gradients.training.datasets.dataset_interfaces.dataset_interface import ClassificationTestDatasetInterface
from super_gradients.training.metrics import Accuracy, Top5


class SaveCkptListUnitTest(unittest.TestCase):
    def setUp(self):
        # Define Parameters
        train_params = {"max_epochs": 4, "lr_decay_factor": 0.1, "lr_updates": [4], "lr_mode": "step",
                        "lr_warmup_epochs": 0, "initial_lr": 0.1, "loss": "cross_entropy", "optimizer": "SGD",
                        "criterion_params": {}, "optimizer_params": {"weight_decay": 1e-4, "momentum": 0.9},
                        "save_ckpt_epoch_list": [1, 3],
                        "loss": "cross_entropy", "train_metrics_list": [Accuracy(), Top5()],
                        "valid_metrics_list": [Accuracy(), Top5()],
                        "loss_logging_items_names": ["Loss"], "metric_to_watch": "Accuracy",
                        "greater_metric_to_watch_is_better": True}

        # Define Model
        model = SgModel("save_ckpt_test", model_checkpoints_location='local')

        # Connect Dataset
        dataset = ClassificationTestDatasetInterface()
        model.connect_dataset_interface(dataset, data_loader_num_workers=8)

        # Build Model
        model.build_model("resnet18_cifar", load_checkpoint=False)

        # Train Model (and save ckpt_epoch_list)
        model.train(training_params=train_params)

        dir_path = model.checkpoints_dir_path
        self.file_names_list = [dir_path + f'/ckpt_epoch_{epoch}.pth' for epoch in train_params["save_ckpt_epoch_list"]]

    def test_save_ckpt_epoch_list(self):
        self.assertTrue(os.path.exists(self.file_names_list[0]))
        self.assertTrue(os.path.exists(self.file_names_list[1]))


if __name__ == '__main__':
    unittest.main()
