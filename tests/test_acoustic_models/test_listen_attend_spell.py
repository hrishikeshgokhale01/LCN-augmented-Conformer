import unittest
import torch
import logging

from openspeech.models import ListenAttendSpellModel, ListenAttendSpellConfigs
from openspeech.tokenizers.ksponspeech.character import KsponSpeechCharacterTokenizer
from openspeech.utils import (
    DUMMY_INPUTS,
    DUMMY_INPUT_LENGTHS,
    DUMMY_TARGETS,
    DUMMY_TARGET_LENGTHS,
    build_dummy_configs,
)
from openspeech.criterion.label_smoothed_cross_entropy.label_smoothed_cross_entropy import (
    LabelSmoothedCrossEntropyLossConfigs,
    LabelSmoothedCrossEntropyLoss,
)

logger = logging.getLogger(__name__)


class TestListenAttendSpell(unittest.TestCase):
    def test_forward(self):
        configs = build_dummy_configs(
            model_configs=ListenAttendSpellConfigs(),
            criterion_configs=LabelSmoothedCrossEntropyLossConfigs(),
        )

        vocab = KsponSpeechCharacterTokenizer(configs)
        model = ListenAttendSpellModel(configs, vocab)

        criterion = LabelSmoothedCrossEntropyLoss(configs, num_classes=len(vocab), vocab=vocab)
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-04)

        for i in range(3):
            outputs = model(DUMMY_INPUTS, DUMMY_INPUT_LENGTHS)

            loss = criterion(outputs["logits"], DUMMY_TARGETS[:, 1:])
            loss.backward()
            optimizer.step()
            assert type(loss.item()) == float

    def test_beam_search(self):
        configs = build_dummy_configs(
            model_configs=ListenAttendSpellConfigs(),
            criterion_configs=LabelSmoothedCrossEntropyLossConfigs(),
        )

        vocab = KsponSpeechCharacterTokenizer(configs)
        model = ListenAttendSpellModel(configs, vocab)
        model.set_beam_decoder(beam_size=3)

        for i in range(3):
            prediction = model(DUMMY_INPUTS, DUMMY_INPUT_LENGTHS)["predictions"]
            assert isinstance(prediction, torch.Tensor)

    def test_training_step(self):
        configs = build_dummy_configs(
            model_configs=ListenAttendSpellConfigs(),
            criterion_configs=LabelSmoothedCrossEntropyLossConfigs(),
        )

        vocab = KsponSpeechCharacterTokenizer(configs)
        model = ListenAttendSpellModel(configs, vocab)

        for i in range(3):
            outputs = model.training_step(
                batch=(DUMMY_INPUTS, DUMMY_TARGETS, DUMMY_INPUT_LENGTHS, DUMMY_TARGET_LENGTHS), batch_idx=i
            )
            assert type(outputs["loss"].item()) == float

    def test_validation_step(self):
        configs = build_dummy_configs(
            model_configs=ListenAttendSpellConfigs(),
            criterion_configs=LabelSmoothedCrossEntropyLossConfigs(),
        )

        vocab = KsponSpeechCharacterTokenizer(configs)
        model = ListenAttendSpellModel(configs, vocab)

        for i in range(3):
            outputs = model.validation_step(
                batch=(DUMMY_INPUTS, DUMMY_TARGETS, DUMMY_INPUT_LENGTHS, DUMMY_TARGET_LENGTHS), batch_idx=i
            )
            assert type(outputs["loss"].item()) == float

    def test_test_step(self):
        configs = build_dummy_configs(
            model_configs=ListenAttendSpellConfigs(),
            criterion_configs=LabelSmoothedCrossEntropyLossConfigs(),
        )

        vocab = KsponSpeechCharacterTokenizer(configs)
        model = ListenAttendSpellModel(configs, vocab)

        for i in range(3):
            outputs = model.test_step(
                batch=(DUMMY_INPUTS, DUMMY_TARGETS, DUMMY_INPUT_LENGTHS, DUMMY_TARGET_LENGTHS), batch_idx=i
            )
            assert type(outputs["loss"].item()) == float


if __name__ == '__main__':
    unittest.main()
