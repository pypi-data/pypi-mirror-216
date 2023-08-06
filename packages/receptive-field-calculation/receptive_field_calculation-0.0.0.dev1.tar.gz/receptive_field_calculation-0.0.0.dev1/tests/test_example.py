"""
  Basic boilerplate to illustrate setting up unit tests.
"""

from rf_calc import search_rf
import torch

def test_conv1d_3_1_1():
  layer = torch.nn.Conv1d(2, 2, 3, 1, 1, 1)
  rf = search_rf(layer, (2, 20))
  assert rf == 3

def test_convtanspose1d_4_2_1():
  layer = torch.nn.ConvTranspose1d(2, 2, 4, 2, 1)
  rf = search_rf(layer, (2, 20))
  assert rf == 2

def test_complex():
  up = torch.nn.ConvTranspose1d(2, 2, 4, 2, 1)
  conv = torch.nn.Conv1d(2, 2, 3, 1, 1, 1)
  rf = search_rf(lambda x: conv(up(x)), (2, 20))
  assert rf == 4
