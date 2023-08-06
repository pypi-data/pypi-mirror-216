import torch


def load_from_checkpoint(checkpoint_path):
    callback = torch.load(checkpoint_path)
    callback.epoch += 1
    model = callback.model
    optimizer = callback.optimizer
    return model, optimizer, callback
